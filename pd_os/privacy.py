"""Filter personal or low-signal content from digests and shared artifacts."""

from __future__ import annotations

import re

# Personal / family / health / housing — drop entire line if matched.
_PERSONAL_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(p, re.I)
    for p in (
        r"\b(my wife|my husband|my kid|my sister|my father|brother-in-law|landlord)\b",
        r"\bhaven\b",
        r"\b(buying a house|buy a house|house hunt|housing market|looking at houses)\b",
        r"\b(homesick|moved in|couple years out from (buying|purchasing))\b",
        r"\bcomparing prices\b",
        r"\b(newer construction|renovated older homes)\b",
        r"\bball on tee\b",
        r"\b(boys and girls in area|signup for)\b",
        r"\b(end of year event|competitive matches)\b",
        r"\b(los gatos|danville|watsonville|san ramon|mount diablo)\b",
        r"\b(school-age kids?|little kids|little one|school age)\b",
        r"\b(t-ball|dance school|recital|soccer club|soccer tournament)\b",
        r"\b(jaundice|sepsis|homesick)\b",
        r"\b(allergies over the weekend|my voice|scratchy through|voice goes out)\b",
        r"\b(has doctors|doctor's appointment)\b",
        r"\b(no big events|pretty chill)\b",
        r"\b(roses|mulch|watering.{0,24}grass|yard of grass|big gardener)\b",
        r"\b(smog test|oil change|auto shop|dropped the car off)\b",
        r"\bwhere we (are|live|moved)\b",
        r"\bwater park|dublin wave\b",
        r"\b(dog friendly beach|do they allow dogs)\b",
        r"\bstanford consultation\b",
        r"\b(weekend|personal updates?|personal matters)\b",
        r"\bhealthcare.*personal\b",
        r"\b@[a-z0-9._-]+\.(com|org|net)\b",
        r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
    )
)

# Casual transcript noise — mainly for commitments / pushback / quotes.
_NOISE_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(p, re.I)
    for p in (
        r"share my (screen|desktop|whole desktop)",
        r"zoom a little",
        r"can you hear me",
        r"if you can hear me okay",
        r"^oh wait\b",
        r"^nope i can't access",
        r"^yeah\. yeah\. yeah",
        r"^but (i don't know|but yeah)\.?$",
        r"^but i feel like it",
        r"^but you'll get used to it",
        r"^has been, you know, hopefully",
        r"^i can i can go sorry",
        r"google rose gardens",
        r"^weird okay yeah i'll",
        r"^you know what i think i can select",
    )
)

_WORK_CONTEXT = re.compile(
    r"\b("
    r"nova|firefox|figma|lattice|calibration|jira|release|design|mobile|desktop|"
    r"community|reddit|connect|engineer|research|stakeholder|review|mockup|"
    r"prototype|fox fooding|onboarding|wallpaper|token|sidebar|toolbar|"
    r"promotion|performance review|product review|netlify|claude"
    r")\b",
    re.I,
)

# Trailing personal asides in otherwise work-safe meeting-context bullets.
_TRAILING_PERSONAL: tuple[re.Pattern[str], ...] = tuple(
    re.compile(p, re.I)
    for p in (
        r"\s+but has school-age kids.*",
        r"\s+but has (younger )?children.*",
        r"\s+\([^)]*school[^)]*\)",
    )
)


def contains_personal_info(text: str) -> bool:
    return any(p.search(text) for p in _PERSONAL_PATTERNS)


def is_transcript_noise(text: str) -> bool:
    if any(p.search(text) for p in _NOISE_PATTERNS):
        return True
    # Long conversational ramble without clear work topic.
    if len(text) > 160 and not _WORK_CONTEXT.search(text):
        return True
    return False


def is_casual_pushback(text: str) -> bool:
    """Drop small-talk pushback lines with no work topic."""
    if _WORK_CONTEXT.search(text):
        return False
    if len(text) <= 200 and re.match(r"^(oh|yeah|cool|wow|nice|but)\b", text.strip(), re.I):
        return True
    return False


def include_in_digest(text: str, section: str) -> bool:
    """Return False if this bullet should not appear in digests."""
    if contains_personal_info(text):
        return False
    section_l = section.lower()
    if section_l.startswith(("commitments", "pushback", "notable quotes")):
        if is_transcript_noise(text):
            return False
        if section_l.startswith(("pushback", "notable quotes")) and is_casual_pushback(text):
            return False
    return True


def sanitize_text(text: str, *, section: str) -> str | None:
    """Return cleaned text for digests, or None if the line should be omitted."""
    if not include_in_digest(text, section):
        return None

    cleaned = text.strip()
    if section.lower().startswith("meeting context"):
        for pattern in _TRAILING_PERSONAL:
            cleaned = pattern.sub("", cleaned).strip()
        if contains_personal_info(cleaned):
            return None
    return cleaned or None


_SECTION_HEADER = re.compile(r"^\*\*(?P<title>.+?)\*\*\s*$")
_BULLET = re.compile(r"^- (.+)$")


def _section_from_header(title: str) -> str:
    t = title.lower()
    if "commitment" in t:
        return "Commitments"
    if "pushback" in t or "concern" in t:
        return "Pushback"
    if "preference" in t:
        return "Preference signals"
    if "meeting context" in t or "granola" in t:
        return "Meeting context"
    return "Meeting context"


def filter_stakeholder_markdown(text: str, *, default_section: str = "Meeting context") -> str:
    """Remove personal / low-signal bullets from a meeting-log or notes markdown chunk."""
    current_section = default_section
    kept: list[str] = []

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            if kept and kept[-1] != "":
                kept.append("")
            continue

        if stripped.startswith("### "):
            kept.append(line)
            current_section = default_section
            continue

        header = _SECTION_HEADER.match(stripped)
        if header:
            kept.append(line)
            current_section = _section_from_header(header.group("title"))
            continue

        bullet = _BULLET.match(stripped)
        if bullet:
            cleaned = sanitize_text(bullet.group(1), section=current_section)
            if cleaned:
                kept.append(f"- {cleaned}")
            continue

        if not contains_personal_info(stripped) and not is_transcript_noise(stripped):
            kept.append(line)

    # Drop trailing blank lines.
    while kept and kept[-1] == "":
        kept.pop()

    return _drop_empty_sections("\n".join(kept))


def _drop_empty_sections(text: str) -> str:
    """Remove section headers that have no bullets before the next header."""
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        header = _SECTION_HEADER.match(line.strip())
        if not header:
            out.append(line)
            i += 1
            continue

        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        has_content = False
        while j < len(lines):
            nxt = lines[j].strip()
            if _SECTION_HEADER.match(nxt) or nxt.startswith("### "):
                break
            if nxt.startswith("- "):
                has_content = True
                break
            j += 1

        if has_content:
            out.append(line)
        i += 1

    return "\n".join(out).strip()
