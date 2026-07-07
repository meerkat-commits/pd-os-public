#!/usr/bin/env python3
"""Generate SVG placeholders for portfolio assets. PNG exports replace via <picture>."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "assets"

# path, title, source hint, accent (firefox|venmo|neutral|home)
ITEMS: list[tuple[str, str, str, str]] = [
    ("cover-hello.svg", "Hello cover", "Figma: Cover / Hello", "home"),
    ("firefox/overview.svg", "Firefox Overview", "Figma FF · Overview 497:2547", "firefox"),
    ("firefox/vision-statement.svg", "UX Vision Statement", "Figma FF · Vision slide", "firefox"),
    ("firefox/device-ecosystem.svg", "Device ecosystem", "Figma · Imagine what's next", "firefox"),
    ("firefox/pillars.svg", "Three pillars", "Figma · Agentic · Habit · Localization", "firefox"),
    ("firefox/brand-timeline.svg", "Brand timeline", "Figma · 2025 / 2026+", "firefox"),
    ("firefox/craft-pillars.svg", "Design craft pillars", "Figma FF · Craft slide", "firefox"),
    ("firefox/modes-three-up.svg", "Three modes", "Figma · Private / Classic / Smart", "firefox"),
    ("firefox/community-tracker.svg", "Community tracker", "Public landing screenshot", "firefox"),
    ("firefox/nightly/nova-chrome.svg", "Nova chrome", "Nightly capture", "firefox"),
    ("firefox/nightly/nova-ntp.svg", "Nova NTP", "Nightly capture", "firefox"),
    ("firefox/nightly/smart-window-ai.svg", "Smart Window AI", "Nightly capture", "firefox"),
    ("firefox/smart-window/modes-diagram.svg", "Modes diagram", "Figma Smart Window", "firefox"),
    ("firefox/smart-window/states.svg", "Thinking states", "Figma or spec export", "firefox"),
    ("venmo/cover.svg", "Experience Vision 2024", "Figma Venmo · Cover", "venmo"),
    ("venmo/intention-magic.svg", "Intention + Magic", "Figma Venmo", "venmo"),
    ("venmo/gap-matrix.svg", "Gap matrix", "Figma Venmo · 2x2", "venmo"),
    ("venmo/value-props.svg", "Value props", "Figma Venmo · three-up", "venmo"),
    ("venmo/vision-anywhere.svg", "Take Venmo Anywhere", "Figma Venmo · Vision", "venmo"),
    ("venmo/workstreams.svg", "Workstreams", "Figma Venmo · C2 timeline", "venmo"),
    ("venmo/flywheel.svg", "Commerce flywheel", "Figma Venmo · Flywheel", "venmo"),
    ("operating-model/four-layers.svg", "Four layers", "Diagram from brief", "neutral"),
    ("operating-model/three-bets.svg", "Three bets", "brief.shareable.md", "neutral"),
    ("operating-model/pd-os-dashboard.svg", "PD-OS dashboard", "Local screenshot", "neutral"),
]

ACCENTS = {
    "firefox": "#7845e8",
    "venmo": "#0074DE",
    "home": "#ffffff",
    "neutral": "#bbbbbb",
}


def svg_content(title: str, source: str, accent: str) -> str:
    color = ACCENTS.get(accent, "#bbbbbb")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">
  <rect width="1920" height="1080" fill="#000000"/>
  <rect x="80" y="80" width="1760" height="920" fill="none" stroke="#262626" stroke-width="2"/>
  <rect x="80" y="80" width="6" height="920" fill="{color}"/>
  <text x="120" y="200" fill="#ffffff" font-family="system-ui, sans-serif" font-size="56" font-weight="700">{title}</text>
  <text x="120" y="280" fill="#7e7e7e" font-family="system-ui, sans-serif" font-size="28">Placeholder — export 2× PNG from Figma</text>
  <text x="120" y="340" fill="#bbbbbb" font-family="ui-monospace, monospace" font-size="22">{source}</text>
  <text x="120" y="980" fill="#3c3c3c" font-family="ui-monospace, monospace" font-size="18">See draft/image-manifest.md</text>
</svg>
"""


def main() -> None:
    for rel, title, source, accent in ITEMS:
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(svg_content(title, source, accent), encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT.parent)}")
    print(f"\n{len(ITEMS)} placeholders in {ROOT}")


if __name__ == "__main__":
    main()
