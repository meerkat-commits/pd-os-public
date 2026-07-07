from __future__ import annotations

import argparse
import urllib.error
from datetime import date
from pathlib import Path

from pd_os.paths import ensure_base_folders, repo_root_from_here
from pd_os.automation import (
    run_daily_automation,
    run_weekly_automation,
    sync_granola_to_people,
    write_daily_digest,
    write_weekly_rollup,
)
from pd_os.dashboard import serve_dashboard
from pd_os.critique_dashboard import serve_critique_dashboard
from pd_os.granola_api import GranolaAuthError
from pd_os.jira_import import JiraImportError, import_cowork_export
from pd_os.jira_sync import (
    JiraAuthError,
    credential_debug_info,
    discover_and_update_config,
    format_discover_table,
    format_preview_markdown,
    list_boards,
    load_config,
    preview_board,
    sync_project_velocity,
    test_auth,
)
from pd_os.workflows import (
    write_commitments_digest,
    write_project_hygiene,
    write_stakeholder_draft,
    write_stakeholder_drafts_from_commitments,
)
from pd_os.people import (
    MeetingMeta,
    append_meeting_log,
    ensure_person_file,
    guess_meeting_date_from_filename,
    extract_signals,
)
from pd_os.transcripts import parse_transcript, read_transcript_file, unique_speakers
from pd_os.nightly_screenshots import DEFAULT_PROJECT_SLUG, run_capture
from pd_os.figjam_sync import write_pending_sync
from pd_os.paths import repo_root_from_here

try:
    from pd_os.calibration import readiness_report, run_calibration_reminder

    _HAS_CALIBRATION = True
except ImportError:
    _HAS_CALIBRATION = False


def cmd_init(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    ensure_base_folders(root)
    print(f"Initialized PM-OS folders under: {root / 'data'}")
    return 0


def _ingest_one(transcript_path: Path, meeting_title: str | None, meeting_date: str | None, only: str | None) -> int:
    root = repo_root_from_here()
    paths = ensure_base_folders(root)

    transcript_path = transcript_path.expanduser().resolve()
    text = read_transcript_file(transcript_path)
    utterances = parse_transcript(text)

    parsed_meeting_date: date
    if meeting_date:
        parsed_meeting_date = date.fromisoformat(meeting_date)
    else:
        parsed_meeting_date = guess_meeting_date_from_filename(transcript_path) or date.today()

    meta = MeetingMeta(title=meeting_title or transcript_path.stem, meeting_date=parsed_meeting_date)

    speakers = unique_speakers(utterances)
    if only:
        only_set = {s.strip() for s in only.split(",") if s.strip()}
        speakers = [s for s in speakers if s in only_set]

    if not speakers:
        print("No speakers found (format expected: 'Name: text').")
        return 2

    updated = 0
    for person in speakers:
        person_file = ensure_person_file(paths.people, person)
        signals = extract_signals(person, utterances)
        append_meeting_log(person_file, meta, signals)
        updated += 1

    print(f"Updated {updated} people file(s) in: {paths.people}")
    return 0


def cmd_ingest_transcript(args: argparse.Namespace) -> int:
    return _ingest_one(
        transcript_path=Path(args.transcript_path),
        meeting_title=args.meeting_title,
        meeting_date=args.meeting_date,
        only=args.only,
    )


def _newest_file_in_dir(directory: Path, suffixes: set[str]) -> Path | None:
    if not directory.exists() or not directory.is_dir():
        return None
    candidates: list[Path] = []
    for p in directory.iterdir():
        if not p.is_file():
            continue
        if p.suffix.lower() in suffixes:
            candidates.append(p)
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def cmd_ingest_latest(args: argparse.Namespace) -> int:
    search_dir = Path(args.dir).expanduser().resolve()
    suffixes = {s.strip().lower() for s in args.suffixes.split(",") if s.strip()}
    newest = _newest_file_in_dir(search_dir, suffixes)
    if newest is None:
        print(f"No transcripts found in {search_dir} with suffixes: {sorted(suffixes)}")
        return 2

    rc = _ingest_one(
        transcript_path=newest,
        meeting_title=args.meeting_title,
        meeting_date=args.meeting_date,
        only=args.only,
    )

    if rc == 0 and args.move_processed:
        root = repo_root_from_here()
        paths = ensure_base_folders(root)
        processed_dir = paths.inbox_transcripts / "processed"
        processed_dir.mkdir(parents=True, exist_ok=True)

        dest = processed_dir / newest.name
        # Avoid overwriting: add a numeric suffix.
        if dest.exists():
            stem, suf = newest.stem, newest.suffix
            i = 2
            while True:
                candidate = processed_dir / f"{stem}__{i}{suf}"
                if not candidate.exists():
                    dest = candidate
                    break
                i += 1
        newest.replace(dest)
        print(f"Moved processed transcript to: {dest}")

    return rc


def cmd_sync_granola(args: argparse.Namespace) -> int:
    try:
        updated = sync_granola_to_people(time_range=args.time_range)
        print(f"Updated {updated} person-meeting entries from Granola into data/people/")
        return 0
    except GranolaAuthError as e:
        print(f"Granola auth error: {e}")
        return 2


def cmd_daily_digest(args: argparse.Namespace) -> int:
    digest_path = write_daily_digest(time_range=args.time_range)
    print(f"Wrote daily digest: {digest_path}")
    return 0


def cmd_weekly_rollup(args: argparse.Namespace) -> int:
    rollup_path = write_weekly_rollup(time_range=args.time_range)
    print(f"Wrote weekly rollup: {rollup_path}")
    return 0


def cmd_run_daily(args: argparse.Namespace) -> int:
    try:
        result = run_daily_automation(
            digest_time_range=args.time_range,
            stakeholder_drafts=args.stakeholder_drafts,
        )
        print(f"Updated {result['entries']} person-meeting entries from Granola")
        print(f"Wrote daily digest: {result['digest_path']}")
        print(f"Wrote commitments tracker: {result['commitments_path']}")
        print(f"Wrote project hygiene: {result['hygiene_path']}")
        for p in result["draft_paths"]:
            print(f"Wrote stakeholder draft context: {p}")
        return 0
    except GranolaAuthError as e:
        print(f"Granola auth error: {e}")
        return 2


def cmd_run_weekly(args: argparse.Namespace) -> int:
    try:
        result = run_weekly_automation(stakeholder_drafts=args.stakeholder_drafts)
        print(f"Updated {result['entries']} person-meeting entries from Granola")
        print(f"Wrote weekly rollup: {result['rollup_path']}")
        print(f"Wrote commitments tracker: {result['commitments_path']}")
        print(f"Wrote project hygiene: {result['hygiene_path']}")
        for p in result["draft_paths"]:
            print(f"Wrote stakeholder draft context: {p}")
        return 0
    except GranolaAuthError as e:
        print(f"Granola auth error: {e}")
        return 2


def cmd_commitments_digest(args: argparse.Namespace) -> int:
    path = write_commitments_digest(time_range=args.time_range)
    print(f"Wrote commitments tracker: {path}")
    return 0


def cmd_project_hygiene(args: argparse.Namespace) -> int:
    path = write_project_hygiene(stale_days=args.stale_days)
    print(f"Wrote project hygiene: {path}")
    return 0


def cmd_stakeholder_draft(args: argparse.Namespace) -> int:
    try:
        path = write_stakeholder_draft(
            person=args.person,
            purpose=args.purpose,
            time_range=args.time_range,
        )
        print(f"Wrote stakeholder draft context: {path}")
        return 0
    except FileNotFoundError as e:
        print(str(e))
        return 2


def cmd_stakeholder_drafts(args: argparse.Namespace) -> int:
    paths = write_stakeholder_drafts_from_commitments(
        time_range=args.time_range,
        purpose=args.purpose,
        max_people=args.max_people,
    )
    if not paths:
        print("No people with commitments in this window.")
        return 0
    for p in paths:
        print(f"Wrote stakeholder draft context: {p}")
    return 0


def cmd_calibration_remind(args: argparse.Namespace) -> int:
    if not _HAS_CALIBRATION:
        print(
            "calibration-remind is local-only (pd_os/calibration.py is not in the shared repo)."
        )
        return 2
    if args.readiness:
        report = readiness_report()
        print(f"Summaries ready: {report['ready_count']}/{report['total']}")
        if report["ready"]:
            print("\nReady:")
            for name in report["ready"]:
                print(f"  - {name}")
        if report["missing"]:
            print("\nMissing:")
            for name in report["missing"]:
                print(f"  - {name}")
        return 0

    result = run_calibration_reminder(
        slot=args.slot,
        force=args.force,
        notify=not args.no_notify,
    )
    if not result.get("ok"):
        print(result.get("error", "calibration reminder failed"))
        return 2
    if result.get("skipped"):
        print(f"Skipped: {result.get('reason')} (days_until={result.get('days_until', '?')})")
        return 0
    print(f"[{result.get('phase_id')}] {result.get('title')}")
    print(result.get("body", ""))
    if result.get("notified"):
        print("\n(macOS notification sent)")
    return 0


def cmd_dashboard(args: argparse.Namespace) -> int:
    serve_dashboard(host=args.host, port=args.port, open_browser=args.open)
    return 0


def cmd_critique_dashboard(args: argparse.Namespace) -> int:
    serve_critique_dashboard(host=args.host, port=args.port, open_browser=args.open)
    return 0


def cmd_jira_discover(args: argparse.Namespace) -> int:
    try:
        if args.apply:
            path, notes = discover_and_update_config(args.project)
            print(f"Updated {path}")
            for line in notes:
                print(f"  - {line}")
            return 0

        site = DEFAULT_JIRA_SITE
        if args.project:
            try:
                site = load_config(args.project).site
            except FileNotFoundError:
                pass

        boards = list_boards(site=site, name_contains=args.query or "")
        print(format_discover_table(boards, site=site))
        if args.project:
            print(f"\nTo auto-fill {args.project}/jira.json: add --apply")
        return 0
    except JiraAuthError as e:
        print(str(e))
        return 1
    except (FileNotFoundError, RuntimeError) as e:
        print(str(e))
        return 2


def cmd_jira_auth(args: argparse.Namespace) -> int:
    """Test Jira credentials and preview configured board(s)."""
    try:
        if args.debug:
            info = credential_debug_info()
            print("Jira credential check (no secrets shown):")
            print(f"  email: {info['email']}")
            print(f"  token length: {info['token_length']} chars (typical: ~24)")
            print(f"  site: {info['site']}")
            if info.get("token_length_suspicious"):
                print(
                    "  ⚠ Token length looks wrong — you likely pasted something other than\n"
                    "    the API token string. Create one at id.atlassian.com → Security →\n"
                    "    API tokens → Create API token. Copy ONLY the single line shown once."
                )
            elif info["token_length"] < 20:
                print("  ⚠ Token looks too short — may be truncated when pasted")
            print()

        config = load_config(args.project)
        user = test_auth(site=config.site)
        print(f"OK — signed in as {user.get('displayName')} ({user.get('emailAddress', '')})")

        boards = [b for b in config.boards if b.id is not None]
        if args.board_id:
            from pd_os.jira_sync import BoardConfig

            boards = [
                BoardConfig(
                    id=args.board_id,
                    name=f"Board {args.board_id}",
                    pillar="",
                    manager="",
                )
            ]

        if not boards:
            print("No board ids in jira.json yet. Add FXAI 13805 or run jira-discover --apply")
            return 0

        for board in boards:
            assert board.id is not None
            issues = preview_board(board.id, site=config.site, limit=args.limit)
            md = format_preview_markdown(user=user, board=board, issues=issues, site=config.site)
            if args.write_preview:
                out = (
                    repo_root_from_here()
                    / "data"
                    / "projects"
                    / args.project
                    / "metrics"
                    / "preview.md"
                )
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(md, encoding="utf-8")
                print(f"Wrote {out}")
            print()
            print(md)

        return 0
    except JiraAuthError as e:
        print(str(e))
        return 1
    except (FileNotFoundError, RuntimeError) as e:
        print(str(e))
        return 2


def cmd_jira_import(args: argparse.Namespace) -> int:
    try:
        root = repo_root_from_here()
        default_file = (
            root
            / "data"
            / "projects"
            / args.project
            / "metrics"
            / "inbox"
            / "cowork-export.json"
        )
        path = Path(args.file).expanduser() if args.file else default_file
        snapshot = import_cowork_export(path, project_slug=args.project, archive=not args.no_archive)
        totals = snapshot.get("totals") or {}
        written = snapshot.get("_written") or {}
        print(f"Imported from {path.name} ({snapshot.get('source')})")
        print(f"  Issues: {totals.get('issues_on_boards', 0)}")
        print(f"  Completed ({snapshot.get('window_days')}d): {totals.get('completed_in_window', 0)}")
        print(f"  Wrote {written.get('markdown', 'metrics/latest.md')}")
        return 0
    except (FileNotFoundError, JiraImportError) as e:
        print(str(e))
        return 2


def cmd_jira_sync(args: argparse.Namespace) -> int:
    try:
        snapshot = sync_project_velocity(args.project)
        totals = snapshot.get("totals") or {}
        print(f"Jira sync complete for {args.project}")
        print(f"  Completed ({snapshot.get('window_days')}d): {totals.get('completed_in_window', 0)}")
        print(f"  Active pipeline: {totals.get('active_pipeline', 0)}")
        print(f"  Est. weekly throughput: {totals.get('weekly_velocity_estimate', 0)} issues/week")
        if snapshot.get("skipped_boards"):
            for note in snapshot["skipped_boards"]:
                print(f"  Note: {note}")
        print(f"  Wrote metrics/latest.md")
        return 0
    except JiraAuthError as e:
        print(str(e))
        return 1
    except (FileNotFoundError, RuntimeError) as e:
        print(str(e))
        return 2


def cmd_nightly_nova_screenshots(args: argparse.Namespace) -> int:
    try:
        only = [s.strip() for s in args.only.split(",") if s.strip()] if args.only else None
        out_dir = run_capture(
            project_slug=args.project,
            dry_run=args.dry_run,
            only=only,
            reset_profiles=args.reset_profiles,
            include_manual=args.include_manual,
            include_best_effort=args.include_best_effort,
        )
        if not args.dry_run and args.sync_figjam:
            root = repo_root_from_here()
            pending = write_pending_sync(out_dir, root=root, slug=args.project)
            print(f"FigJam pending sync: {pending}")
        if not args.dry_run:
            print(out_dir)
        return 0
    except (RuntimeError, ValueError, urllib.error.URLError) as e:
        print(str(e))
        return 1


DEFAULT_JIRA_SITE = "https://mozilla-hub.atlassian.net"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="pdos", description="PD-OS: knowledge/projects/people context system")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="Create base folder structure under <root>/data")
    p_init.add_argument("--root", default=str(repo_root_from_here()), help="Repo root (default: this repo)")
    p_init.set_defaults(func=cmd_init)

    p_ingest = sub.add_parser("ingest-transcript", help="Parse a transcript and append signals into data/people")
    p_ingest.add_argument("transcript_path", help="Path to transcript .txt/.md")
    p_ingest.add_argument("--meeting-title", default=None, help="Human title for the meeting log entry")
    p_ingest.add_argument("--meeting-date", default=None, help="ISO date YYYY-MM-DD (defaults: inferred or today)")
    p_ingest.add_argument(
        "--only",
        default=None,
        help="Comma-separated speaker names to update (exact match), e.g. 'Jane Doe,John Smith'",
    )
    p_ingest.set_defaults(func=cmd_ingest_transcript)

    p_latest = sub.add_parser(
        "ingest-latest",
        help="Ingest the newest transcript from a directory (default: ~/Downloads)",
    )
    p_latest.add_argument("--dir", default="~/Downloads", help="Directory to scan for transcripts")
    p_latest.add_argument("--suffixes", default=".vtt,.txt,.md,.pdf", help="Comma-separated allowed suffixes")
    p_latest.add_argument("--meeting-title", default=None, help="Human title for the meeting log entry")
    p_latest.add_argument("--meeting-date", default=None, help="ISO date YYYY-MM-DD (defaults: inferred or today)")
    p_latest.add_argument(
        "--only",
        default=None,
        help="Comma-separated speaker names to update (exact match), e.g. 'Jane Doe,John Smith'",
    )
    p_latest.add_argument(
        "--move-processed",
        action="store_true",
        help="Move the ingested transcript into data/inbox/transcripts/processed/ to avoid reprocessing",
    )
    p_latest.set_defaults(func=cmd_ingest_latest)

    p_sync_granola = sub.add_parser("sync-granola", help="Sync Granola meeting notes into data/people/ (API key required)")
    p_sync_granola.add_argument("--time-range", default="last_24h", choices=["last_24h", "last_week"])
    p_sync_granola.set_defaults(func=cmd_sync_granola)

    p_daily = sub.add_parser("daily-digest", help="Write digest from updated data/people/ (default: last 24h)")
    p_daily.add_argument("--time-range", default="last_24h", choices=["last_24h", "today"])
    p_daily.set_defaults(func=cmd_daily_digest)

    p_weekly = sub.add_parser("weekly-rollup", help="Write weekly rollup from data/people/")
    p_weekly.add_argument("--time-range", default="last_week", choices=["last_week"])
    p_weekly.set_defaults(func=cmd_weekly_rollup)

    p_run_daily = sub.add_parser(
        "run-daily",
        help="Daily automation: sync Granola (last 24h) + write daily digest",
    )
    p_run_daily.add_argument("--time-range", default="last_24h", choices=["last_24h", "today"])
    p_run_daily.add_argument(
        "--stakeholder-drafts",
        action="store_true",
        help="Also write stakeholder draft context files for people with recent commitments",
    )
    p_run_daily.set_defaults(func=cmd_run_daily)

    p_run_weekly = sub.add_parser(
        "run-weekly",
        help="Weekly automation: sync Granola (last week) + write weekly rollup",
    )
    p_run_weekly.add_argument(
        "--stakeholder-drafts",
        action="store_true",
        help="Also write stakeholder draft context files for people with commitments last week",
    )
    p_run_weekly.set_defaults(func=cmd_run_weekly)

    p_commitments = sub.add_parser("commitments-digest", help="Write commitments tracker from data/people/")
    p_commitments.add_argument("--time-range", default="last_24h", choices=["last_24h", "today", "last_week"])
    p_commitments.set_defaults(func=cmd_commitments_digest)

    p_hygiene = sub.add_parser("project-hygiene", help="Scan data/projects/ for missing or stale artifacts")
    p_hygiene.add_argument("--stale-days", type=int, default=14, help="Flag decisions.md older than N days")
    p_hygiene.set_defaults(func=cmd_project_hygiene)

    p_stakeholder = sub.add_parser("stakeholder-draft", help="Assemble draft message context for one person")
    p_stakeholder.add_argument("--person", required=True, help='Display name, e.g. "Example Stakeholder"')
    p_stakeholder.add_argument("--purpose", default="follow-up", help="Short label: follow-up, nudge, recap, etc.")
    p_stakeholder.add_argument("--time-range", default="last_24h", choices=["last_24h", "today", "last_week"])
    p_stakeholder.set_defaults(func=cmd_stakeholder_draft)

    p_stakeholders = sub.add_parser(
        "stakeholder-drafts",
        help="Assemble draft context for each person with commitments in the window",
    )
    p_stakeholders.add_argument("--time-range", default="last_24h", choices=["last_24h", "today", "last_week"])
    p_stakeholders.add_argument("--purpose", default="follow-up")
    p_stakeholders.add_argument("--max-people", type=int, default=8)
    p_stakeholders.set_defaults(func=cmd_stakeholder_drafts)

    p_cal = sub.add_parser(
        "calibration-remind",
        help="Calibration timeline reminder (macOS notification); requires CALIBRATION_CALL_DATE in env",
    )
    p_cal.add_argument("--slot", default="morning", choices=["morning", "afternoon"])
    p_cal.add_argument("--force", action="store_true", help="Send even if this phase already fired")
    p_cal.add_argument("--no-notify", action="store_true", help="Print only; do not show macOS notification")
    p_cal.add_argument("--readiness", action="store_true", help="Show who has performance summaries on disk")
    p_cal.set_defaults(func=cmd_calibration_remind)

    p_dashboard = sub.add_parser("dashboard", help="Open local web UI (artifacts, agents, changelog)")
    p_dashboard.add_argument("--host", default="127.0.0.1")
    p_dashboard.add_argument("--port", type=int, default=8765)
    p_dashboard.add_argument("--open", action="store_true", help="Open browser on start")
    p_dashboard.set_defaults(func=cmd_dashboard)

    p_critique = sub.add_parser(
        "critique-dashboard",
        help="Critique prep only — form + principles (team slice)",
    )
    p_critique.add_argument("--host", default="127.0.0.1")
    p_critique.add_argument("--port", type=int, default=8767)
    p_critique.add_argument("--open", action="store_true", help="Open browser on start")
    p_critique.set_defaults(func=cmd_critique_dashboard)

    p_jira_discover = sub.add_parser(
        "jira-discover",
        help="List Jira agile boards (optionally auto-fill project jira.json)",
    )
    p_jira_discover.add_argument(
        "--project",
        default="2026-06-ai-velocity-mandate",
        help="Project slug under data/projects/ (for --apply and site lookup)",
    )
    p_jira_discover.add_argument("--query", default="", help="Case-insensitive board name filter")
    p_jira_discover.add_argument(
        "--apply",
        action="store_true",
        help="Set board ids in jira.json from discover_name_contains",
    )
    p_jira_discover.set_defaults(func=cmd_jira_discover)

    p_jira_auth = sub.add_parser(
        "jira-auth",
        help="Test Jira login and preview board issues (reads ~/.config/pd-os/env)",
    )
    p_jira_auth.add_argument(
        "--project",
        default="2026-06-ai-velocity-mandate",
        help="Project slug under data/projects/",
    )
    p_jira_auth.add_argument("--board-id", type=int, default=None, help="Preview one board by id")
    p_jira_auth.add_argument("--limit", type=int, default=15, help="Max issues in preview")
    p_jira_auth.add_argument(
        "--debug",
        action="store_true",
        help="Print safe credential diagnostics (email, token length)",
    )
    p_jira_auth.add_argument(
        "--write-preview",
        action="store_true",
        help="Write metrics/preview.md",
    )
    p_jira_auth.set_defaults(func=cmd_jira_auth)

    p_jira_import = sub.add_parser(
        "jira-import",
        help="Import Jira export from Claude Co-work → metrics/latest.md (no API token)",
    )
    p_jira_import.add_argument(
        "--project",
        default="2026-06-ai-velocity-mandate",
        help="Project slug under data/projects/",
    )
    p_jira_import.add_argument(
        "--file",
        default=None,
        help="Path to JSON or markdown export (default: .../metrics/inbox/cowork-export.json)",
    )
    p_jira_import.add_argument(
        "--no-archive",
        action="store_true",
        help="Do not copy import file to inbox archive",
    )
    p_jira_import.set_defaults(func=cmd_jira_import)

    p_jira_sync = sub.add_parser(
        "jira-sync",
        help="Sync Jira board metrics into data/projects/<slug>/metrics/",
    )
    p_jira_sync.add_argument(
        "--project",
        default="2026-06-ai-velocity-mandate",
        help="Project slug under data/projects/",
    )
    p_jira_sync.set_defaults(func=cmd_jira_sync)

    p_nightly = sub.add_parser(
        "nightly-nova-screenshots",
        help="Capture Nova punch-QA screenshots from Firefox Nightly (macOS)",
    )
    p_nightly.add_argument(
        "--project",
        default=DEFAULT_PROJECT_SLUG,
        help="Project slug under data/projects/",
    )
    p_nightly.add_argument("--dry-run", action="store_true", help="Print plan without capturing")
    p_nightly.add_argument(
        "--only",
        default=None,
        help="Comma-separated shot ids (e.g. chrome,new-tab)",
    )
    p_nightly.add_argument(
        "--reset-profiles",
        action="store_true",
        help="Reset cached Firefox profiles before capture",
    )
    p_nightly.add_argument(
        "--include-best-effort",
        action="store_true",
        help="Include best-effort shots (e.g. tab-grouping) in addition to automated tier",
    )
    p_nightly.add_argument(
        "--include-manual",
        action="store_true",
        help="Include manual-tier shots (chrome-dark, tab-grouping-collapsed)",
    )
    p_nightly.add_argument(
        "--sync-figjam",
        action="store_true",
        help="Write FigJam pending upload manifest after capture",
    )
    p_nightly.set_defaults(func=cmd_nightly_nova_screenshots)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

