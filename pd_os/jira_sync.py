"""Jira board sync for project velocity metrics (Atlassian Cloud REST API)."""

from __future__ import annotations

import base64
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from pd_os.paths import ensure_base_folders, repo_root_from_here


class JiraAuthError(RuntimeError):
    pass


DEFAULT_SITE = "https://mozilla-hub.atlassian.net"

DEFAULT_STATUS_GROUPS: dict[str, list[str]] = {
    "done": ["Done", "Closed", "Resolved", "Complete", "Released"],
    "in_design": [
        "In Design",
        "Design",
        "Design Review",
        "UX Review",
        "Ready for Design",
        "Design In Progress",
    ],
    "ready_for_eng": [
        "Ready for Development",
        "Ready for Dev",
        "Ready for Engineering",
        "Dev Ready",
        "To Do",
    ],
    "in_progress_eng": [
        "In Progress",
        "In Development",
        "In Review",
        "Code Review",
        "In QA",
    ],
}


def _load_local_env() -> None:
    """Load ~/.config/pd-os/env (export KEY=value lines) if present."""
    env_path = Path.home() / ".config" / "pd-os" / "env"
    if not env_path.is_file():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if not key:
            continue
        # Jira creds: always prefer ~/.config/pd-os/env over stale shell exports
        if key.startswith("JIRA_") or key.startswith("ATLASSIAN_"):
            os.environ[key] = val
        elif key not in os.environ:
            os.environ[key] = val


def _credentials() -> tuple[str, str]:
    _load_local_env()
    email = (
        os.environ.get("JIRA_EMAIL", "").strip()
        or os.environ.get("ATLASSIAN_EMAIL", "").strip()
    )
    token = (
        os.environ.get("JIRA_API_TOKEN", "").strip()
        or os.environ.get("ATLASSIAN_API_TOKEN", "").strip()
    )
    if not email or not token:
        raise JiraAuthError(
            "Missing Jira credentials. Either:\n"
            "  1. Run: ./setup/bin/jira-credentials.sh\n"
            "  2. Or export JIRA_EMAIL and JIRA_API_TOKEN\n"
            "API token: https://id.atlassian.com/manage-profile/security/api-tokens"
        )
    return email, token


def credential_debug_info() -> dict[str, Any]:
    """Safe diagnostics — never includes the token itself."""
    _load_local_env()
    email = (
        os.environ.get("JIRA_EMAIL", "")
        or os.environ.get("ATLASSIAN_EMAIL", "")
    )
    token = (
        os.environ.get("JIRA_API_TOKEN", "")
        or os.environ.get("ATLASSIAN_API_TOKEN", "")
    )
    return {
        "email": email.strip(),
        "token_length": len(token.strip()),
        "token_had_outer_whitespace": token != token.strip(),
        "token_length_suspicious": len(token.strip()) < 16 or len(token.strip()) > 80,
        "site": DEFAULT_SITE,
        "configured": bool(email.strip() and token.strip()),
    }


def _auth_header() -> str:
    email, token = _credentials()
    raw = f"{email}:{token}".encode("utf-8")
    return "Basic " + base64.b64encode(raw).decode("ascii")


def jira_request(path: str, *, site: str = DEFAULT_SITE, params: dict[str, str] | None = None) -> Any:
    base = site.rstrip("/")
    url = f"{base}{path}"
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"

    req = urllib.request.Request(url)
    req.add_header("Authorization", _auth_header())
    req.add_header("Accept", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            return json.loads(resp.read().decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = (e.read() or b"").decode("utf-8", errors="replace")
        except Exception:
            pass
        if e.code in (401, 403):
            raise JiraAuthError(
                f"Jira rejected credentials (HTTP {e.code}).\n"
                "Checklist:\n"
                "  1. JIRA_EMAIL must match your Atlassian profile email exactly\n"
                "     → https://id.atlassian.com/manage-profile/profile-and-visibility\n"
                "  2. Create a NEW API token (copy immediately, no spaces)\n"
                "     → https://id.atlassian.com/manage-profile/security/api-tokens\n"
                "  3. Re-run: ./setup/bin/jira-credentials.sh\n"
                "  4. Debug: python3 -m pd_os.cli jira-auth --debug\n"
                + (f" API said: {body[:200]}" if body else "")
            ) from e
        raise RuntimeError(f"Jira API error HTTP {e.code}: {body[:500]}") from e


def _parse_jira_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    for fmt in (
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
    ):
        try:
            dt = datetime.strptime(value.replace("+0000", "+00:00"), fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue
    return None


def _status_bucket(status_name: str, groups: dict[str, list[str]]) -> str:
    normalized = status_name.strip().lower()
    for bucket, names in groups.items():
        for name in names:
            if name.strip().lower() == normalized:
                return bucket
    return "other"


@dataclass
class BoardConfig:
    id: int | None
    name: str
    pillar: str
    manager: str
    discover_name_contains: str = ""
    project_key: str = ""
    board_url: str = ""


@dataclass
class JiraProjectConfig:
    site: str
    boards: list[BoardConfig]
    status_groups: dict[str, list[str]] = field(default_factory=lambda: dict(DEFAULT_STATUS_GROUPS))
    team_members: list[str] = field(default_factory=list)
    velocity_window_days: int = 14


def project_slug_dir(slug: str) -> Path:
    root = repo_root_from_here()
    paths = ensure_base_folders(root)
    return paths.projects / slug


def config_path(slug: str) -> Path:
    return project_slug_dir(slug) / "jira.json"


def load_config(slug: str) -> JiraProjectConfig:
    path = config_path(slug)
    if not path.is_file():
        raise FileNotFoundError(f"No Jira config at {path}. Copy jira.example.json → jira.json and fill board IDs.")

    raw = json.loads(path.read_text(encoding="utf-8"))
    boards: list[BoardConfig] = []
    for b in raw.get("boards", []):
        board_id = b.get("id")
        boards.append(
            BoardConfig(
                id=int(board_id) if board_id is not None else None,
                name=b.get("name", "Unnamed board"),
                pillar=b.get("pillar", ""),
                manager=b.get("manager", ""),
                discover_name_contains=b.get("discover_name_contains", ""),
                project_key=b.get("project_key", ""),
                board_url=b.get("board_url", ""),
            )
        )

    groups = raw.get("status_groups") or DEFAULT_STATUS_GROUPS
    merged = {**DEFAULT_STATUS_GROUPS, **groups}

    return JiraProjectConfig(
        site=raw.get("site", DEFAULT_SITE).rstrip("/"),
        boards=boards,
        status_groups=merged,
        team_members=list(raw.get("team_members", [])),
        velocity_window_days=int(raw.get("velocity_window_days", 14)),
    )


def save_config(slug: str, config: JiraProjectConfig) -> Path:
    path = config_path(slug)
    payload = {
        "site": config.site,
        "velocity_window_days": config.velocity_window_days,
        "status_groups": config.status_groups,
        "team_members": config.team_members,
        "boards": [
            {
                "id": b.id,
                "name": b.name,
                "pillar": b.pillar,
                "manager": b.manager,
                "discover_name_contains": b.discover_name_contains,
                "project_key": b.project_key,
                "board_url": b.board_url,
            }
            for b in config.boards
        ],
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def list_boards(*, site: str = DEFAULT_SITE, name_contains: str = "") -> list[dict[str, Any]]:
    """List agile boards (paginated). Optional case-insensitive name filter."""
    needle = name_contains.strip().lower()
    results: list[dict[str, Any]] = []
    start_at = 0
    max_results = 50

    while True:
        data = jira_request(
            "/rest/agile/1.0/board",
            site=site,
            params={"startAt": str(start_at), "maxResults": str(max_results)},
        )
        for board in data.get("values", []):
            name = board.get("name", "")
            if needle and needle not in name.lower():
                continue
            results.append(
                {
                    "id": board.get("id"),
                    "name": name,
                    "type": board.get("type"),
                    "project_key": (board.get("location") or {}).get("projectKey", ""),
                }
            )
        if data.get("isLast", True):
            break
        start_at += max_results

    return results


def discover_and_update_config(slug: str) -> tuple[Path, list[str]]:
    """Match boards by discover_name_contains and write IDs into jira.json."""
    config = load_config(slug)
    notes: list[str] = []

    for board in config.boards:
        if board.id is not None:
            notes.append(f"Kept existing id for {board.name!r}: {board.id}")
            continue
        needle = board.discover_name_contains or board.name
        matches = list_boards(site=config.site, name_contains=needle)
        if not matches:
            notes.append(f"No Jira board matched {needle!r} for {board.name!r}")
            continue
        if len(matches) > 1:
            names = ", ".join(f"{m['id']}:{m['name']}" for m in matches[:5])
            notes.append(f"Multiple matches for {needle!r} — using first ({names})")
        chosen = matches[0]
        board.id = int(chosen["id"])
        if not board.project_key and chosen.get("project_key"):
            board.project_key = chosen["project_key"]
        notes.append(f"Set {board.name!r} → board id {board.id} ({chosen['name']})")

    path = save_config(slug, config)
    return path, notes


def _fetch_board_issues(board_id: int, *, site: str, max_issues: int = 500) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    start_at = 0
    page_size = 50
    fields = "summary,status,assignee,updated,created,resolutiondate,issuetype,priority,labels"

    while len(issues) < max_issues:
        data = jira_request(
            f"/rest/agile/1.0/board/{board_id}/issue",
            site=site,
            params={
                "startAt": str(start_at),
                "maxResults": str(min(page_size, max_issues - len(issues))),
                "fields": fields,
            },
        )
        batch = data.get("issues", [])
        if not batch:
            break
        issues.extend(batch)
        if start_at + len(batch) >= data.get("total", 0):
            break
        start_at += len(batch)

    return issues


def _summarize_board(
    board: BoardConfig,
    issues: list[dict[str, Any]],
    *,
    status_groups: dict[str, list[str]],
    window_days: int,
) -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    window_start = now - timedelta(days=window_days)

    buckets: dict[str, int] = {k: 0 for k in list(status_groups) + ["other"]}
    by_assignee: dict[str, dict[str, int]] = {}
    completed_in_window = 0
    updated_in_window = 0
    issue_rows: list[dict[str, Any]] = []

    for issue in issues:
        fields = issue.get("fields") or {}
        status_name = (fields.get("status") or {}).get("name", "Unknown")
        bucket = _status_bucket(status_name, status_groups)
        buckets[bucket] = buckets.get(bucket, 0) + 1

        assignee = fields.get("assignee") or {}
        assignee_name = assignee.get("displayName") or "Unassigned"
        by_assignee.setdefault(assignee_name, {k: 0 for k in buckets})
        by_assignee[assignee_name][bucket] = by_assignee[assignee_name].get(bucket, 0) + 1

        resolution_dt = _parse_jira_datetime(fields.get("resolutiondate"))
        updated_dt = _parse_jira_datetime(fields.get("updated"))

        if bucket == "done" and resolution_dt and resolution_dt >= window_start:
            completed_in_window += 1
        if updated_dt and updated_dt >= window_start:
            updated_in_window += 1

        issue_rows.append(
            {
                "key": issue.get("key"),
                "summary": fields.get("summary"),
                "status": status_name,
                "bucket": bucket,
                "assignee": assignee_name,
                "updated": fields.get("updated"),
                "resolutiondate": fields.get("resolutiondate"),
            }
        )

    active_design = buckets.get("in_design", 0)
    active_eng = buckets.get("in_progress_eng", 0) + buckets.get("ready_for_eng", 0)
    throughput_ratio = round(completed_in_window / max(active_design + active_eng, 1), 2)

    return {
        "board_id": board.id,
        "board_name": board.name,
        "pillar": board.pillar,
        "manager": board.manager,
        "project_key": board.project_key,
        "issue_count": len(issues),
        "window_days": window_days,
        "completed_in_window": completed_in_window,
        "updated_in_window": updated_in_window,
        "status_buckets": buckets,
        "by_assignee": by_assignee,
        "throughput_ratio": throughput_ratio,
        "issues": issue_rows,
    }


def test_auth(*, site: str = DEFAULT_SITE) -> dict[str, Any]:
    """Verify credentials via /rest/api/3/myself."""
    return jira_request("/rest/api/3/myself", site=site)


def preview_board(
    board_id: int,
    *,
    site: str = DEFAULT_SITE,
    limit: int = 15,
) -> list[dict[str, Any]]:
    """Return a short list of issues for terminal preview."""
    issues = _fetch_board_issues(board_id, site=site, max_issues=limit)
    rows: list[dict[str, Any]] = []
    for issue in issues:
        fields = issue.get("fields") or {}
        assignee = (fields.get("assignee") or {}).get("displayName") or "Unassigned"
        status = (fields.get("status") or {}).get("name") or "?"
        rows.append(
            {
                "key": issue.get("key"),
                "summary": fields.get("summary"),
                "status": status,
                "assignee": assignee,
                "updated": fields.get("updated"),
            }
        )
    return rows


def format_preview_markdown(
    *,
    user: dict[str, Any],
    board: BoardConfig | None,
    issues: list[dict[str, Any]],
    site: str,
) -> str:
    lines = [
        "# Jira connection OK",
        "",
        f"- **Signed in as:** {user.get('displayName')} ({user.get('emailAddress', 'email hidden')})",
        f"- **Site:** {site}",
        "",
    ]
    if board and board.id is not None:
        lines.extend(
            [
                f"## {board.name} (board {board.id})",
                "",
                f"Project: **{board.project_key or '—'}** · Pillar: {board.pillar}",
                "",
            ]
        )
        if not issues:
            lines.append("_No issues returned (empty board or no access)._")
        else:
            lines.append("| Key | Status | Assignee | Summary |")
            lines.append("|-----|--------|----------|---------|")
            for row in issues:
                summary = (row.get("summary") or "").replace("|", "\\|")[:80]
                lines.append(
                    f"| {row.get('key')} | {row.get('status')} | {row.get('assignee')} | {summary} |"
                )
        lines.append("")
    return "\n".join(lines)


def sync_project_velocity(slug: str, *, skip_unconfigured: bool = True) -> dict[str, Any]:
    config = load_config(slug)
    configured = [b for b in config.boards if b.id is not None]
    missing = [b.name for b in config.boards if b.id is None]

    if not configured:
        raise RuntimeError(
            f"No board IDs in jira.json. Run jira-discover --apply or set id manually."
        )
    if missing and not skip_unconfigured:
        raise RuntimeError(
            f"Board IDs missing for: {', '.join(missing)}. "
            f"Run: python3 -m pd_os.cli jira-discover --project {slug}"
        )

    board_summaries: list[dict[str, Any]] = []
    skipped_notes = [f"Skipped (no id): {name}" for name in missing] if missing else []

    for board in configured:
        assert board.id is not None
        issues = _fetch_board_issues(board.id, site=config.site)
        board_summaries.append(
            _summarize_board(
                board,
                issues,
                status_groups=config.status_groups,
                window_days=config.velocity_window_days,
            )
        )

    total_completed = sum(b["completed_in_window"] for b in board_summaries)
    total_active = sum(
        b["status_buckets"].get("in_design", 0)
        + b["status_buckets"].get("ready_for_eng", 0)
        + b["status_buckets"].get("in_progress_eng", 0)
        for b in board_summaries
    )

    snapshot = {
        "project_slug": slug,
        "synced_at": datetime.now(timezone.utc).isoformat(),
        "site": config.site,
        "window_days": config.velocity_window_days,
        "boards": board_summaries,
        "skipped_boards": skipped_notes,
        "totals": {
            "issues_on_boards": sum(b["issue_count"] for b in board_summaries),
            "completed_in_window": total_completed,
            "active_pipeline": total_active,
            "weekly_velocity_estimate": round(total_completed / max(config.velocity_window_days / 7, 1), 1),
        },
    }

    _write_snapshot_files(slug, snapshot)
    return snapshot


def _write_snapshot_files(slug: str, snapshot: dict[str, Any]) -> tuple[Path, Path]:
    project_dir = project_slug_dir(slug)
    metrics_dir = project_dir / "metrics"
    metrics_dir.mkdir(parents=True, exist_ok=True)

    today = date.today().isoformat()
    json_path = metrics_dir / f"snapshot-{today}.json"
    json_path.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")

    latest_json = metrics_dir / "latest.json"
    latest_json.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")

    md_path = metrics_dir / f"snapshot-{today}.md"
    md_path.write_text(_render_snapshot_markdown(snapshot), encoding="utf-8")

    latest_md = metrics_dir / "latest.md"
    latest_md.write_text(md_path.read_text(encoding="utf-8"), encoding="utf-8")

    return json_path, md_path


def _render_snapshot_markdown(snapshot: dict[str, Any]) -> str:
    totals = snapshot.get("totals") or {}
    window = snapshot.get("window_days", 14)
    lines: list[str] = [
        f"# Jira velocity snapshot — {snapshot.get('project_slug')}",
        "",
        f"_Synced: {snapshot.get('synced_at')}_ · _Window: last {window} days_",
        "",
        "## Totals (all boards)",
        "",
        f"- **Issues on boards:** {totals.get('issues_on_boards', 0)}",
        f"- **Completed in window:** {totals.get('completed_in_window', 0)}",
        f"- **Active pipeline (design + eng):** {totals.get('active_pipeline', 0)}",
        f"- **Est. weekly throughput:** {totals.get('weekly_velocity_estimate', 0)} issues/week",
        "",
    ]

    for board in snapshot.get("boards", []):
        lines.extend(
            [
                f"## {board.get('board_name')} ({board.get('pillar')})",
                "",
                f"**Manager:** {board.get('manager')} · **Project:** {board.get('project_key') or '—'}",
                "",
                f"- Completed ({window}d): **{board.get('completed_in_window', 0)}**",
                f"- Updated ({window}d): {board.get('updated_in_window', 0)}",
                f"- Throughput ratio (done / active): {board.get('throughput_ratio', 0)}",
                "",
                "### Status buckets",
                "",
            ]
        )
        for bucket, count in sorted((board.get("status_buckets") or {}).items()):
            if count:
                lines.append(f"- {bucket}: {count}")
        lines.append("")

        by_assignee = board.get("by_assignee") or {}
        if by_assignee:
            lines.append("### By assignee (active buckets)")
            lines.append("")
            for person, counts in sorted(by_assignee.items()):
                active = (
                    counts.get("in_design", 0)
                    + counts.get("ready_for_eng", 0)
                    + counts.get("in_progress_eng", 0)
                )
                done = counts.get("done", 0)
                if active or done:
                    lines.append(f"- **{person}:** {active} active · {done} done (on board)")
            lines.append("")

    lines.extend(
        [
            "---",
            "",
            "_Regenerate: `python3 -m pd_os.cli jira-sync --project "
            f"{snapshot.get('project_slug')}`_",
            "",
        ]
    )
    return "\n".join(lines)


def format_discover_table(boards: list[dict[str, Any]], *, site: str) -> str:
    if not boards:
        return "No boards matched."
    lines = ["| ID | Name | Type | Project |", "|----|------|------|---------|"]
    for b in boards:
        lines.append(
            f"| {b.get('id')} | {b.get('name')} | {b.get('type')} | {b.get('project_key') or '—'} |"
        )
    lines.append("")
    lines.append(f"Board URLs: `{site}/jira/software/projects/KEY/boards/<id>`")
    return "\n".join(lines)
