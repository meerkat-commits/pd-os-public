"""Ingest Granola meeting data (transcripts + summaries) into data/people/."""

from __future__ import annotations

import re
from datetime import date
from typing import Any

from pd_os.paths import ensure_base_folders, repo_root_from_here
from pd_os.people import (
    MeetingMeta,
    append_meeting_log,
    append_summary_meeting_log,
    ensure_person_file,
    extract_signals,
    merge_meeting_signals,
)
from pd_os.transcripts import Utterance, parse_transcript

BROOKE = "Brooke Katalinich"

EMAIL_DISPLAY: dict[str, str] = {
    "design.lead.com": "Design Lead",
    "pm.partner.com": "PM Partner",
}

_SKIP_EMAIL_FRAGMENTS = (
    "-leads@",
    "-partners@",
    "moco-lt@",
    "nova-area",
    "nova-xfn",
)


def _display_name_from_participant(part: str) -> str | None:
    part = part.strip()
    if not part:
        return None
    email_m = re.search(r"<([^>]+)>", part)
    email = email_m.group(1).lower() if email_m else None
    if email:
        if any(s in email for s in _SKIP_EMAIL_FRAGMENTS):
            return None
        if email in EMAIL_DISPLAY:
            return EMAIL_DISPLAY[email]
    name = re.sub(r"\s*\(note creator\).*", "", part, flags=re.I)
    name = re.sub(r"\s*from Mozilla.*", "", name, flags=re.I)
    name = re.sub(r"\s*<[^>]+>\s*", "", name).strip()
    if not name or name.lower() == "me" or name.lower() == "them":
        return None
    if email and "@" in name:
        local = email.split("@")[0]
        return local.replace(".", " ").title()
    return name


def attendee_display_name(attendee: dict[str, Any]) -> str | None:
    """Normalize a Granola API attendee record to a display name."""
    email = (attendee.get("email") or "").strip().lower()
    if email:
        if any(s in email for s in _SKIP_EMAIL_FRAGMENTS):
            return None
        if email in EMAIL_DISPLAY:
            return EMAIL_DISPLAY[email]
    name = (attendee.get("name") or "").strip()
    if not name:
        if email and "@" in email:
            return email.split("@")[0].replace(".", " ").title()
        return None
    if name.lower() in ("me", "them"):
        return None
    if email and "@" in name:
        return email.split("@")[0].replace(".", " ").title()
    return name


def attendee_names_from_api(attendees: list[dict[str, Any]] | None) -> list[str]:
    out: list[str] = []
    for a in attendees or []:
        if not isinstance(a, dict):
            continue
        name = attendee_display_name(a)
        if name and name not in out:
            out.append(name)
    return out


def api_transcript_to_utterances(
    transcript: list[dict[str, Any]] | None,
    *,
    attendees: list[dict[str, Any]] | None,
    owner_name: str = BROOKE,
) -> list[Utterance]:
    """
    Convert Granola API transcript segments to Utterances.

    macOS: speaker.source is microphone (note owner) or speaker (remote audio).
    For 1:1 meetings, remote audio is mapped to the sole non-owner attendee.
    """
    if not transcript:
        return []

    others = [n for n in attendee_names_from_api(attendees) if n != owner_name]
    remote_name = others[0] if len(others) == 1 else None

    utterances: list[Utterance] = []
    for item in transcript:
        if not isinstance(item, dict):
            continue
        text = (item.get("text") or "").strip()
        if not text:
            continue
        speaker_obj = item.get("speaker") if isinstance(item.get("speaker"), dict) else {}
        source = (speaker_obj.get("source") or "").strip().lower()
        diar = (speaker_obj.get("diarization_label") or "").strip()

        if source == "microphone":
            speaker = owner_name
        elif diar and diar.lower().startswith("speaker"):
            # iOS diarization — only map when we can pair with a single remote attendee.
            speaker = remote_name or diar
        elif source == "speaker" and remote_name:
            speaker = remote_name
        else:
            continue

        utterances.append(Utterance(speaker=speaker, text=text))
    return utterances


def ingest_api_transcript_meeting(
    *,
    title: str,
    meeting_date: date,
    transcript: list[dict[str, Any]] | None,
    attendees: list[dict[str, Any]] | None,
) -> int:
    """Extract per-speaker signals from a Granola API transcript into data/people/."""
    utterances = api_transcript_to_utterances(transcript, attendees=attendees)
    if not utterances:
        return 0

    root = repo_root_from_here()
    paths = ensure_base_folders(root)
    meta = MeetingMeta(title=title, meeting_date=meeting_date)

    speakers = {u.speaker for u in utterances}
    updated = 0
    for person in sorted(speakers):
        if person in ("Me", "Them") or person.lower().startswith("speaker "):
            continue
        person_file = ensure_person_file(paths.people, person)
        signals = extract_signals(person, utterances)
        if not any(signals.values()):
            person_utts = [u.text for u in utterances if u.speaker == person]
            if person_utts:
                signals = {**signals, "quotes": sorted(person_utts, key=len, reverse=True)[:2]}
        if merge_meeting_signals(person_file, meta, signals):
            updated += 1
    return updated


def parse_participants_line(raw: str) -> list[str]:
    out: list[str] = []
    for part in raw.split(","):
        name = _display_name_from_participant(part)
        if name and name not in out and name != BROOKE:
            out.append(name)
    return out


def normalize_granola_inline_speakers(text: str) -> str:
    """Granola often exports 'Me:' / 'Them:' inline on one line — split to one utterance per line."""
    text = re.sub(r"\s+Me:\s+", "\nMe: ", text)
    text = re.sub(r"\s+Them:\s+", "\nThem: ", text)
    return text.strip()


def remap_me_them_transcript(text: str, other_name: str) -> str:
    text = normalize_granola_inline_speakers(text)
    lines: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if re.match(r"^Me:\s*", line, re.I):
            lines.append(re.sub(r"^Me:\s*", f"{BROOKE}: ", line, flags=re.I))
        elif re.match(r"^Them:\s*", line, re.I):
            lines.append(re.sub(r"^Them:\s*", f"{other_name}: ", line, flags=re.I))
        else:
            lines.append(line)
    return "\n".join(lines) + "\n"


def ingest_transcript_meeting(
    *,
    title: str,
    meeting_date: date,
    transcript: str,
    other_speaker: str | None = None,
    extra_speakers: list[str] | None = None,
) -> int:
    root = repo_root_from_here()
    paths = ensure_base_folders(root)
    meta = MeetingMeta(title=title, meeting_date=meeting_date)

    text = transcript
    if other_speaker and re.search(r"\bMe:\s*|\bThem:\s*", text, re.I):
        text = remap_me_them_transcript(text, other_speaker)

    utterances = parse_transcript(text)
    speakers = {u.speaker for u in utterances}
    if extra_speakers:
        speakers.update(extra_speakers)

    updated = 0
    for person in sorted(speakers):
        if person in ("Me", "Them"):
            continue
        person_file = ensure_person_file(paths.people, person)
        signals = extract_signals(person, utterances)
        if not any(signals.values()):
            # Still record attendance when we have transcript lines but no heuristic hits.
            person_utts = [u.text for u in utterances if u.speaker == person]
            if person_utts:
                signals = {**signals, "quotes": sorted(person_utts, key=len, reverse=True)[:2]}
        if any(signals.values()):
            append_meeting_log(person_file, meta, signals)
            updated += 1
    return updated


def ingest_summary_meeting(
    *,
    title: str,
    meeting_date: date,
    summary: str,
    participants: list[str],
    max_participants: int = 8,
) -> int:
    """Append a summary-based log for small meetings or next-step assignees."""
    root = repo_root_from_here()
    paths = ensure_base_folders(root)
    meta = MeetingMeta(title=title, meeting_date=meeting_date)

    assignees = _names_from_next_steps(summary)
    # Small meetings: update all attendees, not only "Next steps" names (often just "Brooke").
    if len(participants) <= 4:
        targets = list(dict.fromkeys(participants + assignees))
    else:
        targets = assignees if assignees else participants
    if len(targets) > max_participants:
        targets = targets[:max_participants]

    bullets = _summary_bullets(summary)
    if not bullets:
        return 0

    updated = 0
    for person in targets:
        if person == BROOKE:
            continue
        person_file = ensure_person_file(paths.people, person)
        append_summary_meeting_log(person_file, meta, bullets)
        updated += 1
    return updated


def _names_from_next_steps(summary: str) -> list[str]:
    names: list[str] = []
    in_next = False
    for line in summary.splitlines():
        if re.search(r"next steps", line, re.I):
            in_next = True
            continue
        if in_next and line.startswith("###"):
            break
        if in_next:
            m = re.match(r"^-\s*([^:]+):", line)
            if m:
                name = m.group(1).strip()
                if name and name not in names:
                    names.append(name)
    return names


def _summary_bullets(summary: str) -> list[str]:
    bullets: list[str] = []
    for line in summary.splitlines():
        line = line.strip()
        if line.startswith("- "):
            bullets.append(line[2:].strip())
        elif line.startswith("### "):
            bullets.append(line[4:].strip())
    return bullets[:12]
