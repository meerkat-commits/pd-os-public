from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Utterance:
    speaker: str
    text: str


_SPEAKER_LINE = re.compile(
    r"^\s*(?P<speaker>[A-Z][\w .,'-]{0,80}?)(?:\s*\((?:Host|Guest|Organizer|External)\))?\s*:\s*(?P<text>.+?)\s*$"
)

_SPEAKER_LINE_BRACKET = re.compile(
    r"^\s*\[(?P<speaker>[^\]]{1,80})\]\s*(?P<text>.+?)\s*$"
)

_VTT_TIMESTAMP = re.compile(
    r"^\s*\d{2}:\d{2}:\d{2}\.\d{3}\s+-->\s+\d{2}:\d{2}:\d{2}\.\d{3}.*$"
)


def normalize_zoom_vtt_to_text(vtt_text: str) -> str:
    """
    Zoom cloud transcript downloads are commonly WebVTT.

    We strip:
    - 'WEBVTT' header
    - cue identifiers (numeric lines)
    - timestamp lines
    - empty lines

    And keep only the spoken text lines, joined with newlines.
    """
    out_lines: list[str] = []
    for raw in vtt_text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.upper() == "WEBVTT":
            continue
        if line.isdigit():
            continue
        if _VTT_TIMESTAMP.match(line):
            continue
        # Some VTTs contain style/metadata blocks; drop obvious ones.
        if line.startswith("NOTE") or line.startswith("STYLE") or line.startswith("REGION"):
            continue
        out_lines.append(line)
    return "\n".join(out_lines).strip() + ("\n" if out_lines else "")


def parse_transcript(text: str) -> list[Utterance]:
    """
    Best-effort parser for common transcript formats:
      - "Jane Doe: ... "
      - "Jane Doe (Host): ..."

    Lines that don't match a speaker pattern are appended to the previous utterance.
    """
    utterances: list[Utterance] = []
    last_idx: int | None = None

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        m = _SPEAKER_LINE.match(line)
        if m:
            utterances.append(Utterance(speaker=m.group("speaker").strip(), text=m.group("text").strip()))
            last_idx = len(utterances) - 1
            continue

        b = _SPEAKER_LINE_BRACKET.match(line)
        if b:
            utterances.append(Utterance(speaker=b.group("speaker").strip(), text=b.group("text").strip()))
            last_idx = len(utterances) - 1
            continue

        if last_idx is not None:
            prev = utterances[last_idx]
            utterances[last_idx] = Utterance(speaker=prev.speaker, text=f"{prev.text} {line}".strip())

    return utterances


def read_transcript_file(path: Path) -> str:
    suf = path.suffix.lower()
    if suf == ".pdf":
        try:
            from pypdf import PdfReader  # type: ignore
        except Exception as e:
            raise RuntimeError(
                "PDF transcript support requires pypdf. Install dependencies with: python3 -m pip install -r requirements.txt"
            ) from e

        reader = PdfReader(str(path))
        pages_text: list[str] = []
        for page in reader.pages:
            pages_text.append(page.extract_text() or "")
        return "\n".join(pages_text).strip() + "\n"

    raw = path.read_text(encoding="utf-8", errors="replace")
    if suf == ".vtt":
        return normalize_zoom_vtt_to_text(raw)
    return raw


def unique_speakers(utterances: Iterable[Utterance]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for u in utterances:
        if u.speaker not in seen:
            seen.add(u.speaker)
            out.append(u.speaker)
    return out

