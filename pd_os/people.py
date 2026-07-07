from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from dateutil.parser import parse as parse_dt

from pd_os.transcripts import Utterance


def slugify_person(name: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "_", name.strip()).strip("_")
    return s or "Unknown"


@dataclass(frozen=True)
class MeetingMeta:
    title: str
    meeting_date: date


def guess_meeting_date_from_filename(path: Path) -> date | None:
    # Tries to extract YYYY-MM-DD from filename, e.g. "2026-04-08-weekly.txt"
    m = re.search(r"(\d{4}-\d{2}-\d{2})", path.name)
    if not m:
        return None
    try:
        return parse_dt(m.group(1)).date()
    except Exception:
        return None


def ensure_person_file(people_dir: Path, person_name: str) -> Path:
    people_dir.mkdir(parents=True, exist_ok=True)
    path = people_dir / f"{slugify_person(person_name)}.md"
    if not path.exists():
        path.write_text(
            "\n".join(
                [
                    f"# {person_name}",
                    "",
                    "## Communication preferences (inferred)",
                    "- _TBD_",
                    "",
                    "## Pushback patterns",
                    "- _TBD_",
                    "",
                    "## Commitments / follow-ups",
                    "- _TBD_",
                    "",
                    "## Notable quotes",
                    "- _TBD_",
                    "",
                    "## Meeting log",
                    "",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
    return path


def _bullets_from_lines(lines: list[str]) -> list[str]:
    out: list[str] = []
    for ln in lines:
        ln = ln.strip()
        if not ln:
            continue
        out.append(f"- {ln}")
    return out


def extract_signals(person: str, utterances: list[Utterance]) -> dict[str, list[str]]:
    """
    Offline-first heuristics. Not meant to be perfect; meant to be consistent.
    """
    person_utts = [u.text for u in utterances if u.speaker == person]
    joined = "\n".join(person_utts)

    # Commitments: "I'll", "I will", "I'll take", "I'll follow up", "I can", "I'll send"
    commitments: list[str] = []
    for line in person_utts:
        if re.search(r"\b(I'll|I will|I'll take|I'll follow up|I can|I'll send|I'll share|I'll do)\b", line, re.I):
            commitments.append(line)

    # Pushback: "I don't think", "concern", "risk", "but", "however", "push back"
    pushback: list[str] = []
    for line in person_utts:
        if re.search(r"\b(concern|risk|I don't think|I disagree|push back|however|but)\b", line, re.I):
            pushback.append(line)

    # Preference inference: tone/style clues
    prefs: list[str] = []
    if re.search(r"\b(data|metrics|numbers|benchmark|measure)\b", joined, re.I):
        prefs.append("Responds to data/metrics framing.")
    if re.search(r"\b(customer|users?|impact|outcome)\b", joined, re.I):
        prefs.append("Responds to customer/impact framing.")
    if re.search(r"\b(quick|fast|ship|iterate)\b", joined, re.I):
        prefs.append("Prefers speed/iteration language.")
    if re.search(r"\b(risk|mitigat|edge case|failure)\b", joined, re.I):
        prefs.append("Wants risk/mitigation called out explicitly.")

    # Quotes: pick up to 3 longer lines
    quotes = sorted(person_utts, key=lambda s: len(s), reverse=True)[:3]

    return {
        "prefs": prefs,
        "pushback": pushback[:5],
        "commitments": commitments[:5],
        "quotes": quotes,
    }


def _meeting_entry_header(meta: MeetingMeta) -> str:
    return f"### {meta.meeting_date.isoformat()} — {meta.title}"


def _signal_section_lines(signals: dict[str, list[str]]) -> list[str]:
    lines: list[str] = []
    if signals.get("prefs"):
        lines.append("**Preference signals**")
        lines.extend(_bullets_from_lines(signals["prefs"]))
        lines.append("")
    if signals.get("pushback"):
        lines.append("**Pushback / concerns**")
        lines.extend(_bullets_from_lines(signals["pushback"]))
        lines.append("")
    if signals.get("commitments"):
        lines.append("**Commitments**")
        lines.extend(_bullets_from_lines(signals["commitments"]))
        lines.append("")
    if signals.get("quotes"):
        lines.append("**Notable quotes (verbatim-ish)**")
        lines.extend(_bullets_from_lines([f"“{q}”" for q in signals["quotes"]]))
        lines.append("")
    return lines


def append_meeting_log(person_file: Path, meta: MeetingMeta, signals: dict[str, list[str]]) -> None:
    if not any(signals.values()):
        return
    existing = person_file.read_text(encoding="utf-8", errors="replace")
    header = _meeting_entry_header(meta)
    if header in existing:
        merge_meeting_signals(person_file, meta, signals)
        return

    entry_lines: list[str] = [header, ""]
    entry_lines.extend(_signal_section_lines(signals))
    insertion = "\n".join(entry_lines).strip() + "\n\n"

    if "\n## Meeting log\n" not in existing:
        existing = existing.rstrip() + "\n\n## Meeting log\n\n"

    person_file.write_text(existing.rstrip() + "\n\n" + insertion, encoding="utf-8")


def merge_meeting_signals(person_file: Path, meta: MeetingMeta, signals: dict[str, list[str]]) -> bool:
    """
    Add transcript-derived signal sections to an existing meeting entry, or create one.
    Returns True if the file was updated.
    """
    if not any(signals.values()):
        return False

    existing = person_file.read_text(encoding="utf-8", errors="replace")
    header = _meeting_entry_header(meta)
    section_lines = _signal_section_lines(signals)
    if not section_lines:
        return False

    if header not in existing:
        append_meeting_log(person_file, meta, signals)
        return True

    start = existing.index(header)
    after_header = existing[start + len(header) :]
    next_m = re.search(r"\n### \d{4}-\d{2}-\d{2} — ", after_header)
    end = start + len(header) + (next_m.start() if next_m else len(after_header))
    block = existing[start:end]

    additions: list[str] = []
    if signals.get("prefs") and "**Preference signals**" not in block:
        additions.append("**Preference signals**")
        additions.extend(_bullets_from_lines(signals["prefs"]))
        additions.append("")
    if signals.get("pushback") and "**Pushback / concerns**" not in block:
        additions.append("**Pushback / concerns**")
        additions.extend(_bullets_from_lines(signals["pushback"]))
        additions.append("")
    if signals.get("commitments") and "**Commitments**" not in block:
        additions.append("**Commitments**")
        additions.extend(_bullets_from_lines(signals["commitments"]))
        additions.append("")
    if signals.get("quotes") and "**Notable quotes (verbatim-ish)**" not in block:
        additions.append("**Notable quotes (verbatim-ish)**")
        additions.extend(_bullets_from_lines([f"“{q}”" for q in signals["quotes"]]))
        additions.append("")

    if not additions:
        return False

    insertion = "\n".join(additions).strip() + "\n"
    updated = existing[:end].rstrip() + "\n\n" + insertion + "\n" + existing[end:].lstrip("\n")
    person_file.write_text(updated, encoding="utf-8")
    return True


def append_summary_meeting_log(person_file: Path, meta: MeetingMeta, summary_bullets: list[str]) -> None:
    """Append meeting context from Granola summary (no per-speaker transcript)."""
    existing = person_file.read_text(encoding="utf-8", errors="replace")
    header = _meeting_entry_header(meta)
    if header in existing:
        return

    entry_lines: list[str] = []
    entry_lines.append(header)
    entry_lines.append("")
    entry_lines.append("**Meeting context (from Granola summary)**")
    entry_lines.extend(_bullets_from_lines(summary_bullets))
    entry_lines.append("")

    insertion = "\n".join(entry_lines).strip() + "\n\n"

    if "\n## Meeting log\n" not in existing:
        existing = existing.rstrip() + "\n\n## Meeting log\n\n"

    person_file.write_text(existing.rstrip() + "\n\n" + insertion, encoding="utf-8")

