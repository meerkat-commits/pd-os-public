from __future__ import annotations

import json
import re
from dataclasses import dataclass, replace
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from pd_os.granola_api import GranolaNote, get_note, list_notes
from pd_os.granola_sync import attendee_names_from_api, ingest_api_transcript_meeting
from pd_os.paths import ensure_base_folders, repo_root_from_here
from pd_os.people import MeetingMeta, append_summary_meeting_log, ensure_person_file
from pd_os.privacy import sanitize_text


def _parse_iso_date(s: str | None) -> date | None:
    if not s:
        return None
    try:
        # Handles YYYY-MM-DD... formats.
        return datetime.fromisoformat(s.replace("Z", "+00:00")).date()
    except Exception:
        return None


def _time_range_to_window(time_range: str, today: date | None = None) -> tuple[datetime, datetime]:
    """
    Returns (start_utc, end_utc) windows for Granola created_after/before.
    """
    today = today or date.today()
    end = datetime.combine(today + timedelta(days=1), datetime.min.time(), tzinfo=timezone.utc)

    if time_range == "last_24h":
        start = datetime.now(tz=timezone.utc) - timedelta(hours=24)
        return start, datetime.now(tz=timezone.utc)

    if time_range == "last_week":
        # Previous calendar week (Mon..Sun) relative to today.
        # today.weekday(): Mon=0..Sun=6
        start_of_this_week = today - timedelta(days=today.weekday())
        start_of_last_week = start_of_this_week - timedelta(days=7)
        end_of_last_week = start_of_this_week
        start = datetime.combine(start_of_last_week, datetime.min.time(), tzinfo=timezone.utc)
        end = datetime.combine(end_of_last_week, datetime.min.time(), tzinfo=timezone.utc)
        return start, end

    raise ValueError("time_range must be one of: last_24h, last_week")


def _attendee_names(attendees: list[dict] | None) -> list[str]:
    out: list[str] = []
    if not attendees:
        return out
    for a in attendees:
        if not isinstance(a, dict):
            continue
        name = (a.get("name") or "").strip()
        email = (a.get("email") or "").strip()
        if not name and email and "@" in email:
            name = email.split("@")[0].replace(".", " ").title()
        if name and name not in out:
            out.append(name)
    return out


def _summary_bullets(summary_markdown: str | None, max_items: int = 16) -> list[str]:
    if not summary_markdown:
        return []
    bullets: list[str] = []
    for raw in summary_markdown.splitlines():
        ln = raw.strip()
        if not ln:
            continue
        if ln.startswith("- "):
            bullets.append(ln[2:].strip())
        elif ln.startswith("### "):
            bullets.append(ln[4:].strip())
    return bullets[:max_items]


def sync_granola_to_people(*, time_range: str, cache_dir: Path | None = None) -> int:
    """
    Pulls Granola notes for the window and updates data/people.

    - Summary bullets via append_summary_meeting_log
    - Transcript signals (commitments, pushback, prefs) when API returns transcript
    - Uses Granola API (GRANOLA_API_KEY env var)
    - Caches raw notes under data/inbox/granola-api/
    """
    root = repo_root_from_here()
    paths = ensure_base_folders(root)
    cache_dir = cache_dir or (paths.data / "inbox" / "granola-api")
    cache_dir.mkdir(parents=True, exist_ok=True)

    start, end = _time_range_to_window(time_range)
    raw_items = list_notes(created_after=start, created_before=end)

    updated = 0
    for item in raw_items:
        note_id = item.get("id") or item.get("note_id")
        if not note_id:
            continue
        note: GranolaNote = get_note(note_id=note_id, include_transcript=True)

        meeting_day = _parse_iso_date(note.start_time) or _parse_iso_date(note.created_at) or date.today()
        meta = MeetingMeta(title=note.title, meeting_date=meeting_day)

        bullets = _summary_bullets(note.summary_markdown)
        attendees = attendee_names_from_api(note.attendees) or _attendee_names(note.attendees)
        if not attendees:
            attendees = ["Unknown"]

        # Cache raw note for traceability (refresh when transcript newly available).
        cache_path = cache_dir / f"{meeting_day.isoformat()}__{note.id}.json"
        cache_payload = {
            "id": note.id,
            "title": note.title,
            "created_at": note.created_at,
            "start_time": note.start_time,
            "web_url": note.web_url,
            "summary_markdown": note.summary_markdown,
            "attendees": note.attendees,
            "transcript": note.transcript,
        }
        if not cache_path.exists() or note.transcript:
            cache_path.write_text(json.dumps(cache_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        if bullets:
            for person in attendees:
                person_file = ensure_person_file(paths.people, person)
                append_summary_meeting_log(person_file, meta, bullets)
                updated += 1

        if note.transcript:
            updated += ingest_api_transcript_meeting(
                title=note.title,
                meeting_date=meeting_day,
                transcript=note.transcript,
                attendees=note.attendees,
            )

    return updated


@dataclass(frozen=True)
class DigestItem:
    person: str
    meeting_date: str
    meeting_title: str
    section: str
    text: str


def filter_digest_items(items: list[DigestItem]) -> list[DigestItem]:
    """Drop or redact personal / low-signal lines before writing digests."""
    out: list[DigestItem] = []
    for item in items:
        cleaned = sanitize_text(item.text, section=item.section)
        if not cleaned:
            continue
        out.append(replace(item, text=cleaned) if cleaned != item.text else item)
    return out


_MEETING_HEADER = re.compile(r"^###\s+(?P<d>\d{4}-\d{2}-\d{2})\s+—\s+(?P<title>.+?)\s*$")
_BOLD_SECTION = re.compile(r"^\*\*(?P<section>[^*]{1,80})\*\*\s*$")
_BULLET = re.compile(r"^- (.+)$")


def _date_window_for_time_range(time_range: str) -> tuple[date, date, str, datetime]:
    """Returns (since_date, until_date, label, since_datetime_utc)."""
    now = datetime.now(tz=timezone.utc)
    today = now.date()

    if time_range == "today":
        start = datetime.combine(today, datetime.min.time(), tzinfo=timezone.utc)
        return today, today, today.isoformat(), start

    if time_range == "last_24h":
        since_dt = now - timedelta(hours=24)
        return since_dt.date(), today, f"last 24h (through {today.isoformat()})", since_dt

    raise ValueError("time_range must be one of: last_24h, today")


def _extract_granola_api_cache_items(cache_dir: Path, since_dt: datetime) -> list[DigestItem]:
    """Meeting context from notes cached during recent sync-granola runs."""
    items: list[DigestItem] = []
    if not cache_dir.exists():
        return items

    for path in sorted(cache_dir.glob("*.json")):
        try:
            if path.stat().st_mtime < since_dt.timestamp():
                continue
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue

        title = (data.get("title") or "(untitled)").strip()
        meeting_day = _parse_iso_date(data.get("start_time")) or _parse_iso_date(data.get("created_at"))
        if not meeting_day:
            continue

        bullets = _summary_bullets(data.get("summary_markdown"))
        if not bullets:
            continue

        attendees = _attendee_names(data.get("attendees"))
        if not attendees:
            attendees = ["Unknown"]

        for person in attendees:
            for text in bullets:
                items.append(
                    DigestItem(
                        person=person,
                        meeting_date=meeting_day.isoformat(),
                        meeting_title=title,
                        section="Meeting context (from Granola summary)",
                        text=text,
                    )
                )
    return items


def _dedupe_items(items: list[DigestItem]) -> list[DigestItem]:
    seen: set[tuple[str, str, str, str, str]] = set()
    out: list[DigestItem] = []
    for i in items:
        key = (i.person, i.meeting_date, i.meeting_title, i.section, i.text)
        if key in seen:
            continue
        seen.add(key)
        out.append(i)
    return out


def _extract_person_entries(path: Path, since: date, until: date) -> list[DigestItem]:
    person = path.stem.replace("_", " ")
    items: list[DigestItem] = []

    cur_date: str | None = None
    cur_title: str | None = None
    cur_section: str | None = None

    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = _MEETING_HEADER.match(raw.strip())
        if m:
            cur_date = m.group("d")
            cur_title = m.group("title").strip()
            cur_section = None
            continue

        if not cur_date or not cur_title:
            continue

        try:
            d = date.fromisoformat(cur_date)
        except Exception:
            continue
        if d < since or d > until:
            continue

        s = _BOLD_SECTION.match(raw.strip())
        if s:
            cur_section = s.group("section").strip()
            continue

        b = _BULLET.match(raw.strip())
        if b and cur_section:
            items.append(
                DigestItem(
                    person=person,
                    meeting_date=cur_date,
                    meeting_title=cur_title,
                    section=cur_section,
                    text=b.group(1).strip(),
                )
            )

    return items


def write_daily_digest(*, time_range: str = "last_24h") -> Path:
    """
    Writes data/digests/YYYY-MM-DD.md from people meeting logs in the window.

    Default window is last 24 hours (not calendar today). Includes Granola
    "Meeting context" bullets from data/people and recent granola-api cache.
    """
    root = repo_root_from_here()
    paths = ensure_base_folders(root)
    since, until, label, since_dt = _date_window_for_time_range(time_range)

    digests_dir = paths.data / "digests"
    digests_dir.mkdir(parents=True, exist_ok=True)
    out_path = digests_dir / f"{until.isoformat()}.md"

    people_files = sorted(paths.people.glob("*.md"))
    all_items: list[DigestItem] = []
    for pf in people_files:
        all_items.extend(_extract_person_entries(pf, since=since, until=until))

    cache_dir = paths.data / "inbox" / "granola-api"
    all_items.extend(_extract_granola_api_cache_items(cache_dir, since_dt))
    all_items = filter_digest_items(_dedupe_items(all_items))

    def pick(section: str) -> list[DigestItem]:
        return [i for i in all_items if i.section.lower().startswith(section.lower())]

    meeting_context = pick("Meeting context")
    commitments = pick("Commitments")
    pushback = pick("Pushback")
    prefs = pick("Preference")

    def render(items: list[DigestItem], limit: int = 80) -> list[str]:
        if not items:
            return ["- _None found_"]
        return [f"- **{i.person}** ({i.meeting_date}, {i.meeting_title}): {i.text}" for i in items[:limit]]

    lines: list[str] = []
    lines.append(f"# Daily digest — {label}")
    lines.append("")
    lines.append("## Meeting context (Granola)")
    lines.extend(render(meeting_context))
    lines.append("")
    lines.append("## Commitments")
    lines.extend(render(commitments))
    lines.append("")
    lines.append("## Pushback / concerns")
    lines.extend(render(pushback))
    lines.append("")
    lines.append("## Preference signals")
    lines.extend(render(prefs))
    lines.append("")

    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return out_path


def write_weekly_rollup(*, time_range: str = "last_week") -> Path:
    """
    Writes a weekly rollup file under data/rollups/weekly/.
    """
    if time_range != "last_week":
        raise ValueError("weekly-rollup currently supports only time_range=last_week")

    root = repo_root_from_here()
    paths = ensure_base_folders(root)

    start_dt, end_dt = _time_range_to_window("last_week")
    since = start_dt.date()
    until = (end_dt - timedelta(seconds=1)).date()

    rollup_dir = paths.data / "rollups" / "weekly"
    rollup_dir.mkdir(parents=True, exist_ok=True)
    out_path = rollup_dir / f"{since.isoformat()}__to__{until.isoformat()}.md"

    people_files = sorted(paths.people.glob("*.md"))
    all_items: list[DigestItem] = []
    for pf in people_files:
        all_items.extend(_extract_person_entries(pf, since=since, until=until))

    all_items = filter_digest_items(all_items)

    lines: list[str] = []
    lines.append(f"# Weekly rollup — {since.isoformat()} to {until.isoformat()}")
    lines.append("")

    by_person: dict[str, list[DigestItem]] = {}
    for i in all_items:
        by_person.setdefault(i.person, []).append(i)

    for person in sorted(by_person.keys()):
        items = by_person[person]
        commits = [i for i in items if i.section.lower().startswith("commitments")]
        concerns = [i for i in items if i.section.lower().startswith("pushback")]
        lines.append(f"## {person}")
        lines.append("")
        lines.append("### Commitments")
        if commits:
            for i in commits[:25]:
                lines.append(f"- ({i.meeting_date}) {i.text}")
        else:
            lines.append("- _None found_")
        lines.append("")
        lines.append("### Pushback / concerns")
        if concerns:
            for i in concerns[:25]:
                lines.append(f"- ({i.meeting_date}) {i.text}")
        else:
            lines.append("- _None found_")
        lines.append("")

    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return out_path


def run_daily_automation(
    *,
    digest_time_range: str = "last_24h",
    stakeholder_drafts: bool = False,
) -> dict[str, object]:
    """Sync Granola (last 24h), write digests, commitments tracker, and project hygiene."""
    from pd_os.workflows import (
        write_commitments_digest,
        write_project_hygiene,
        write_stakeholder_drafts_from_commitments,
    )

    entries = sync_granola_to_people(time_range="last_24h")
    digest_path = write_daily_digest(time_range=digest_time_range)
    commitments_path = write_commitments_digest(time_range=digest_time_range)
    hygiene_path = write_project_hygiene()
    draft_paths: list[Path] = []
    if stakeholder_drafts:
        draft_paths = write_stakeholder_drafts_from_commitments(time_range=digest_time_range)

    return {
        "entries": entries,
        "digest_path": digest_path,
        "commitments_path": commitments_path,
        "hygiene_path": hygiene_path,
        "draft_paths": draft_paths,
    }


def run_weekly_automation(*, stakeholder_drafts: bool = False) -> dict[str, object]:
    """Sync Granola (last calendar week), rollup, commitments, and project hygiene."""
    from pd_os.workflows import (
        write_commitments_digest,
        write_project_hygiene,
        write_stakeholder_drafts_from_commitments,
    )

    entries = sync_granola_to_people(time_range="last_week")
    rollup_path = write_weekly_rollup(time_range="last_week")
    commitments_path = write_commitments_digest(time_range="last_week")
    hygiene_path = write_project_hygiene(stale_days=14)
    draft_paths: list[Path] = []
    if stakeholder_drafts:
        draft_paths = write_stakeholder_drafts_from_commitments(time_range="last_week", max_people=12)

    return {
        "entries": entries,
        "rollup_path": rollup_path,
        "commitments_path": commitments_path,
        "hygiene_path": hygiene_path,
        "draft_paths": draft_paths,
    }

