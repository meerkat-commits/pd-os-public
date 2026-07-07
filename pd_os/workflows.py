"""Commitments tracking, project hygiene, and stakeholder draft context bundles."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from pd_os.automation import (
    DigestItem,
    _date_window_for_time_range,
    _dedupe_items,
    _extract_person_entries,
    _time_range_to_window,
    filter_digest_items,
)
from pd_os.paths import ensure_base_folders, repo_root_from_here
from pd_os.people import slugify_person
from pd_os.privacy import filter_stakeholder_markdown, sanitize_text

_SKIP_PEOPLE_FILES = frozenset(
    {
        "them",
        "meeting_title",
        "date",
        "meeting_participants",
        "brooke",
        "brooke_katalinich",
    }
)

_STAKEHOLDER_HEADER = re.compile(r"^###\s+(?P<name>.+?)\s+—\s+", re.I)
_TOP_SECTION = re.compile(r"^##\s+(?P<title>.+?)\s*$")
_BULLET = re.compile(r"^- (.+)$")


@dataclass(frozen=True)
class ProjectHygieneRow:
    slug: str
    path: Path
    issues: list[str]


def _digest_window(time_range: str) -> tuple[date, date, str]:
    if time_range == "last_week":
        start_dt, end_dt = _time_range_to_window("last_week")
        since = start_dt.date()
        until = (end_dt - timedelta(seconds=1)).date()
        return since, until, f"{since.isoformat()} to {until.isoformat()}"

    since, until, label, _ = _date_window_for_time_range(time_range)
    return since, until, label


def _collect_items(time_range: str) -> list[DigestItem]:
    root = repo_root_from_here()
    paths = ensure_base_folders(root)
    since, until, _ = _digest_window(time_range)

    items: list[DigestItem] = []
    for pf in sorted(paths.people.glob("*.md")):
        if pf.stem.lower() in _SKIP_PEOPLE_FILES:
            continue
        items.extend(_extract_person_entries(pf, since=since, until=until))
    return filter_digest_items(_dedupe_items(items))


def write_commitments_digest(*, time_range: str = "last_24h") -> Path:
    """Write a commitments-focused digest under data/digests/."""
    root = repo_root_from_here()
    paths = ensure_base_folders(root)
    since, until, label = _digest_window(time_range)

    digests_dir = paths.data / "digests"
    digests_dir.mkdir(parents=True, exist_ok=True)
    out_path = digests_dir / f"commitments-{until.isoformat()}.md"

    items = [i for i in _collect_items(time_range) if i.section.lower().startswith("commitments")]

    by_person: dict[str, list[DigestItem]] = {}
    for i in items:
        by_person.setdefault(i.person, []).append(i)

    lines: list[str] = [
        f"# Commitments tracker — {label}",
        "",
        f"_Window: {since.isoformat()} → {until.isoformat()}_",
        "",
    ]

    if not by_person:
        lines.append("- _No commitments found in this window._")
        lines.append("")
        out_path.write_text("\n".join(lines), encoding="utf-8")
        return out_path

    for person in sorted(by_person.keys()):
        lines.append(f"## {person}")
        lines.append("")
        for i in sorted(by_person[person], key=lambda x: (x.meeting_date, x.meeting_title)):
            lines.append(f"- **{i.meeting_date}** · _{i.meeting_title}_ — {i.text}")
        lines.append("")

    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return out_path


def _scan_project(path: Path, *, stale_days: int, today: date) -> ProjectHygieneRow:
    issues: list[str] = []
    slug = path.name

    if not path.is_dir():
        return ProjectHygieneRow(slug=slug, path=path, issues=["not a directory"])

    expected = ["brief.md", "decisions.md"]
    for name in expected:
        if not (path / name).exists():
            issues.append(f"missing `{name}`")

    for folder in ("research", "drafts"):
        p = path / folder
        if not p.exists():
            issues.append(f"missing `{folder}/`")

    decisions = path / "decisions.md"
    if decisions.exists():
        age_days = (today - date.fromtimestamp(decisions.stat().st_mtime)).days
        if age_days > stale_days:
            issues.append(f"`decisions.md` stale ({age_days}d since last edit; threshold {stale_days}d)")

    brief = path / "brief.md"
    if brief.exists():
        text = brief.read_text(encoding="utf-8", errors="replace").strip()
        if len(text) < 80 or "_TBD_" in text[:400]:
            issues.append("`brief.md` looks empty or mostly placeholders")

    return ProjectHygieneRow(slug=slug, path=path, issues=issues)


def write_project_hygiene(*, stale_days: int = 14) -> Path:
    """Scan data/projects/ and write a hygiene report."""
    root = repo_root_from_here()
    paths = ensure_base_folders(root)
    today = date.today()

    digests_dir = paths.data / "digests"
    digests_dir.mkdir(parents=True, exist_ok=True)
    out_path = digests_dir / f"project-hygiene-{today.isoformat()}.md"

    projects_root = paths.projects
    rows: list[ProjectHygieneRow] = []

    if projects_root.exists():
        for child in sorted(projects_root.iterdir()):
            if not child.is_dir() or child.name.startswith("."):
                continue
            rows.append(_scan_project(child, stale_days=stale_days, today=today))

    lines: list[str] = [
        f"# Project hygiene — {today.isoformat()}",
        "",
        f"_Flag initiatives with missing files or `decisions.md` older than {stale_days} days._",
        "",
    ]

    problem_rows = [r for r in rows if r.issues]
    healthy = [r for r in rows if not r.issues]

    if not rows:
        lines.append("- _No project folders under `data/projects/` yet. Create `YYYY-MM-<slug>/` with `brief.md` and `decisions.md`._")
    elif not problem_rows:
        lines.append("- All scanned project folders look healthy.")
    else:
        lines.append("## Needs attention")
        lines.append("")
        for r in problem_rows:
            rel = r.path.relative_to(root)
            lines.append(f"### `{r.slug}` (`{rel}`)")
            for issue in r.issues:
                lines.append(f"- {issue}")
            lines.append("")

    if healthy:
        lines.append("## Healthy")
        lines.append("")
        for r in healthy:
            lines.append(f"- `{r.slug}`")
        lines.append("")

    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return out_path


def _stakeholder_blurb_from_library(name: str, library_path: Path) -> str | None:
    if not library_path.exists():
        return None
    text = library_path.read_text(encoding="utf-8", errors="replace")
    name_l = name.lower()
    chunks: list[str] = []
    in_block = False
    for line in text.splitlines():
        m = _STAKEHOLDER_HEADER.match(line.strip())
        if m:
            if in_block and chunks:
                break
            header_name = m.group("name").strip()
            in_block = name_l in header_name.lower() or header_name.lower() in name_l
            if in_block:
                chunks = [line.strip()]
            continue
        if in_block:
            chunks.append(line)
    block = "\n".join(chunks).strip()
    return block if block else None


def _person_static_sections(person_file: Path) -> dict[str, list[str]]:
    """Parse top-level ## sections before Meeting log."""
    sections: dict[str, list[str]] = {}
    cur: str | None = None
    for raw in person_file.read_text(encoding="utf-8", errors="replace").splitlines():
        if raw.strip() == "## Meeting log":
            break
        m = _TOP_SECTION.match(raw.strip())
        if m:
            cur = m.group("title").strip()
            sections[cur] = []
            continue
        if cur and (b := _BULLET.match(raw.strip())):
            text = b.group(1).strip()
            if text and text != "_TBD_":
                sections[cur].append(text)
    return sections


def _recent_meeting_blocks(person_file: Path, *, limit: int = 3) -> list[str]:
    text = person_file.read_text(encoding="utf-8", errors="replace")
    if "## Meeting log" not in text:
        return []
    log = text.split("## Meeting log", 1)[1]
    parts = re.split(r"\n(?=### \d{4}-\d{2}-\d{2} — )", log)
    blocks = [p.strip() for p in parts if p.strip() and p.strip().startswith("### ")]
    return blocks[:limit]


def write_stakeholder_draft(
    *,
    person: str,
    purpose: str = "follow-up",
    time_range: str = "last_24h",
) -> Path:
    """
    Assemble a draft context file for Cursor/agent to turn into a message.
    Does not call an LLM — output is input for setup/agents/stakeholder-draft.md.
    """
    root = repo_root_from_here()
    paths = ensure_base_folders(root)
    since, until, label = _digest_window(time_range)

    person_file = paths.people / f"{slugify_person(person)}.md"
    if not person_file.exists():
        raise FileNotFoundError(f"No person file for {person!r}: {person_file}")

    drafts_dir = paths.data / "drafts" / "stakeholder"
    drafts_dir.mkdir(parents=True, exist_ok=True)
    out_path = drafts_dir / f"{until.isoformat()}__{slugify_person(person)}.md"

    library = root / "context-library" / "stakeholders.md"
    blurb = _stakeholder_blurb_from_library(person, library)
    static = _person_static_sections(person_file)
    meetings = _recent_meeting_blocks(person_file, limit=3)

    person_display = person_file.stem.replace("_", " ")
    recent_items = [i for i in _collect_items(time_range) if i.person == person_display]
    commits = [i for i in recent_items if i.section.lower().startswith("commitments")]
    pushback = [i for i in recent_items if i.section.lower().startswith("pushback")]
    prefs = [i for i in recent_items if i.section.lower().startswith("preference")]

    lines: list[str] = [
        f"# Stakeholder draft context — {person}",
        "",
        f"- **Purpose:** {purpose}",
        f"- **Window:** {label}",
        f"- **Agent prompt:** `setup/agents/stakeholder-draft.md`",
        "",
        "## Draft message",
        "",
        "_Write 3–6 sentences below (or ask Cursor using the agent prompt)._",
        "",
        "---",
        "",
    ]

    if blurb:
        lines.append("## Stakeholder library")
        lines.append("")
        lines.append(blurb)
        lines.append("")

    for title, bullets in static.items():
        if bullets:
            filtered = [
                b
                for b in bullets[:8]
                if sanitize_text(b, section=title) is not None
            ]
            if not filtered:
                continue
            lines.append(f"## {title} (from person file)")
            lines.append("")
            for b in filtered:
                lines.append(f"- {sanitize_text(b, section=title)}")
            lines.append("")

    if commits:
        lines.append("## Recent commitments")
        lines.append("")
        for i in commits[:12]:
            lines.append(f"- **{i.meeting_date}** · _{i.meeting_title}_ — {i.text}")
        lines.append("")

    if pushback:
        lines.append("## Recent pushback / concerns")
        lines.append("")
        for i in pushback[:8]:
            lines.append(f"- **{i.meeting_date}** — {i.text[:280]}")
        lines.append("")

    if prefs:
        lines.append("## Preference signals")
        lines.append("")
        for i in prefs[:6]:
            lines.append(f"- {i.text}")
        lines.append("")

    if meetings:
        lines.append("## Recent meeting log (excerpt)")
        lines.append("")
        for block in meetings:
            filtered = filter_stakeholder_markdown(block)
            # Skip blocks that are only a meeting header after filtering.
            substantive = [
                ln for ln in filtered.splitlines()
                if ln.strip() and not ln.strip().startswith("### ")
            ]
            if not substantive:
                continue
            excerpt = filtered[:1200]
            lines.append(excerpt)
            if len(filtered) > 1200:
                lines.append("_…truncated…_")
            lines.append("")

    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return out_path


def write_stakeholder_drafts_from_commitments(
    *,
    time_range: str = "last_24h",
    purpose: str = "follow-up",
    max_people: int = 8,
) -> list[Path]:
    """Create draft context files for each person with commitments in the window."""
    items = [i for i in _collect_items(time_range) if i.section.lower().startswith("commitments")]
    people = sorted({i.person for i in items})[:max_people]
    out: list[Path] = []
    for person in people:
        out.append(write_stakeholder_draft(person=person, purpose=purpose, time_range=time_range))
    return out
