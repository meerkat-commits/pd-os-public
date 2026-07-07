#!/usr/bin/env python3
"""Nova design-token simplification scorecard.

Fetches Are We Design Tokens Yet (AWDTY) data and reports consolidation
metrics for PM/stakeholder comms: type scale, color, spacing, and trajectory.

Data source: https://firefoxux.github.io/arewedesigntokensyet/
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

AWDTY_BASE = "https://firefoxux.github.io/arewedesigntokensyet"
PROPERTY_VALUES_URL = f"{AWDTY_BASE}/data/propertyValues.json"
HISTORY_URL = (
    "https://raw.githubusercontent.com/FirefoxUX/arewedesigntokensyet/main/src/data"
)

CORE_FONT_TOKENS = (
    "--font-size-xsmall",
    "--font-size-small",
    "--font-size-root",
    "--font-size-large",
    "--font-size-xlarge",
    "--font-size-xxlarge",
)

SCORECARD_PROPS = (
    ("font-size", r"(--font-size[^,)]+)"),
    ("color", r"(--(?:text-color|color)[^,)]+)"),
    ("gap", r"(--space[^,)]+)"),
    ("border-radius", r"(--border-radius[^,)]+)"),
    ("padding", r"(--space[^,)]+)"),
)


def fetch_json(url: str, cache_dir: Path | None) -> dict | list:
    cache_path = None
    if cache_dir:
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_path = cache_dir / re.sub(r"[^\w.-]+", "_", url.split("/")[-1])
        if cache_path.exists():
            return json.loads(cache_path.read_text())

    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            payload = json.load(response)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        if cache_path and cache_path.exists():
            print(f"Warning: fetch failed ({exc}); using cached {cache_path}", file=sys.stderr)
            return json.loads(cache_path.read_text())
        raise

    if cache_path:
        cache_path.write_text(json.dumps(payload))
    return payload


def path_matches(path: str, surface: str) -> bool:
    filters = {
        "nova": lambda p: "newtab" in p or "nova" in p,
        "nova-ntp": lambda p: "activity-stream" in p,
        "aiwindow": lambda p: "aiwindow" in p,
        "legacy-chrome": lambda p: p.startswith("browser/themes/"),
        "urlbar": lambda p: "urlbar" in p,
        "global": lambda p: True,
    }
    return filters[surface](path)


def analyze_font_size(by_property: dict, surface: str) -> dict:
    prop_obj = by_property.get("font-size", {})
    token_names: set[str] = set()
    px_sizes: set[float] = set()
    token_uses = 0
    hard_uses = 0
    token_re = re.compile(r"var\(\s*(--font-size[^,)]+)")

    for value, val_obj in prop_obj.get("values", {}).items():
        files = {
            path: count
            for path, count in val_obj.get("files", {}).items()
            if path_matches(path, surface)
        }
        if not files:
            continue
        count = sum(files.values())
        if val_obj.get("isIgnored"):
            continue

        match = token_re.search(value)
        if match or val_obj.get("containsToken"):
            token_names.add(match.group(1) if match else value)
            token_uses += count
        else:
            hard_uses += count
            px_match = re.match(r"^(\d+(?:\.\d+)?)px$", value.strip())
            if px_match:
                px_sizes.add(float(px_match.group(1)))

    total = token_uses + hard_uses
    core_used = sorted(name for name in token_names if name in CORE_FONT_TOKENS)
    return {
        "total": total,
        "token_uses": token_uses,
        "hard_uses": hard_uses,
        "token_pct": round(100 * token_uses / total, 1) if total else 0,
        "token_names": sorted(token_names),
        "core_token_count": len(core_used),
        "core_tokens": core_used,
        "px_sizes": sorted(px_sizes),
    }


def analyze_property(
    by_property: dict, prop: str, token_pattern: str, surface: str
) -> dict:
    prop_obj = by_property.get(prop, {})
    tokens: set[str] = set()
    hardcoded: set[str] = set()
    token_uses = 0
    hard_uses = 0
    token_re = re.compile(token_pattern)

    for value, val_obj in prop_obj.get("values", {}).items():
        files = {
            path: count
            for path, count in val_obj.get("files", {}).items()
            if path_matches(path, surface)
        }
        if not files:
            continue
        count = sum(files.values())
        if val_obj.get("isIgnored"):
            continue

        if val_obj.get("containsToken"):
            match = token_re.search(value)
            if match:
                tokens.add(match.group(1))
            token_uses += count
        else:
            hardcoded.add(value.strip()[:60])
            hard_uses += count

    total = token_uses + hard_uses
    return {
        "token_types": len(tokens),
        "hardcoded_types": len(hardcoded),
        "token_uses": token_uses,
        "hard_uses": hard_uses,
        "token_pct": round(100 * token_uses / total, 1) if total else 0,
    }


def count_hardcoded_font_sizes(by_property: dict, surface: str) -> int:
    prop_obj = by_property.get("font-size", {})
    hardcoded: set[str] = set()
    for value, val_obj in prop_obj.get("values", {}).items():
        if val_obj.get("containsToken") or val_obj.get("isIgnored"):
            continue
        files = [
            path
            for path in val_obj.get("files", {})
            if path_matches(path, surface)
        ]
        if files:
            hardcoded.add(value.strip())
    return len(hardcoded)


def load_propagation(path_suffix: str, cache_dir: Path | None) -> list[dict]:
    url = f"{HISTORY_URL}/{path_suffix}/propagationHistory.json"
    try:
        return fetch_json(url, cache_dir)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return []


def format_history_points(history: list[dict], count: int = 3) -> str:
    if not history:
        return "n/a"
    points = history[-count:]
    return " → ".join(f"{point['date'][:7]}: {point['percentage']:.1f}%" for point in points)


def build_report(data: dict, cache_dir: Path | None) -> str:
    by_property = data["byProperty"]
    generated_at = data.get("generatedAt", "unknown")

    nova_font = analyze_font_size(by_property, "nova")
    ntp_font = analyze_font_size(by_property, "nova-ntp")
    ai_font = analyze_font_size(by_property, "aiwindow")
    legacy_font = analyze_font_size(by_property, "legacy-chrome")
    global_font = analyze_font_size(by_property, "global")

    newtab_history = load_propagation(
        "browser/extensions/newtab/css", cache_dir
    )
    nova_history = load_propagation(
        "browser/extensions/newtab/css/nova", cache_dir
    )

    lines = [
        "# Nova design token scorecard",
        "",
        f"_Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} "
        f"from [AWDTY](https://firefoxux.github.io/arewedesigntokensyet/) "
        f"(source data: {generated_at})._",
        "",
        "## Headline stats (PM-ready)",
        "",
        "| Metric | Nova / NTP | Legacy chrome | Whole tree |",
        "| :---- | :---- | :---- | :---- |",
        f"| Font-size on token scale | **{ntp_font['token_pct']}%** (NTP CSS) | "
        f"{legacy_font['token_pct']}% | {global_font['token_pct']}% |",
        f"| Core type scale steps in use | **{ntp_font['core_token_count']}** of 6 | "
        f"{legacy_font['core_token_count']} of 6 | {global_font['core_token_count']} of 6 |",
        f"| One-off font-size values | **{count_hardcoded_font_sizes(by_property, 'nova-ntp')}** (NTP) | "
        f"{count_hardcoded_font_sizes(by_property, 'legacy-chrome')} | "
        f"{count_hardcoded_font_sizes(by_property, 'global')} |",
        f"| Hardcoded px font sizes left | **{len(ntp_font['px_sizes'])}** | "
        f"{len(legacy_font['px_sizes'])} | {len(global_font['px_sizes'])} |",
        f"| AI Window font-size tokenized | **{ai_font['token_pct']}%** ({len(ai_font['token_names'])} tokens) | — | — |",
        "",
        "### Suggested talk track",
        "",
        f"- **NTP typography:** {ntp_font['token_pct']}% of font-size declarations use design "
        f"tokens; {ntp_font['core_token_count']} core scale steps cover the surface.",
        f"- **Legacy contrast:** browser chrome themes still carry "
        f"{count_hardcoded_font_sizes(by_property, 'legacy-chrome')} one-off font-size values "
        f"({legacy_font['token_pct']}% tokenized).",
        f"- **Smart Window:** built token-first — {ai_font['token_pct']}% font-size coverage, "
        f"{len(ai_font['px_sizes'])} hardcoded px sizes.",
        "",
        "## Property consolidation (Nova / newtab paths)",
        "",
        "| Property | Token types | Hardcoded types | Tokenized |",
        "| :---- | :---- | :---- | :---- |",
    ]

    for prop, pattern in SCORECARD_PROPS:
        nova = analyze_property(by_property, prop, pattern, "nova")
        lines.append(
            f"| `{prop}` | {nova['token_types']} | {nova['hardcoded_types']} | "
            f"**{nova['token_pct']}%** |"
        )

    lines.extend(
        [
            "",
            "## Trajectory",
            "",
            f"- **New Tab CSS propagation:** {format_history_points(newtab_history, 4)}",
            f"- **Nova CSS propagation:** {format_history_points(nova_history, 4)}",
            "",
            "## Core type scale (Nova NTP)",
            "",
        ]
    )

    if ntp_font["core_tokens"]:
        for token in ntp_font["core_tokens"]:
            lines.append(f"- `{token}`")
    else:
        lines.append("- _No core tokens detected._")

    if ntp_font["px_sizes"]:
        lines.extend(
            [
                "",
                "## Remaining hardcoded px font sizes (Nova NTP)",
                "",
                ", ".join(f"{size:g}px" for size in ntp_font["px_sizes"]),
            ]
        )

    lines.extend(
        [
            "",
            "## Caveats",
            "",
            "- Counts are from AWDTY's scanned CSS paths, not the entire mozilla-central tree.",
            "- Propagation % is an unweighted directory average; consolidation counts are more intuitive for stakeholders.",
            "- Legacy `var(--urlbarView-*)` and similar pre-token variables count as hardcoded.",
            "- Dimensional one-offs (`16px` widths/heights) remain the largest Nova debt in `activity-stream.css`.",
            "",
        ]
    )

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=Path(__file__).resolve().parent / ".cache",
        help="Directory for cached AWDTY JSON (default: scripts/.cache)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Write markdown report to this path (default: stdout)",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Do not read or write cache files",
    )
    args = parser.parse_args()
    cache_dir = None if args.no_cache else args.cache_dir

    data = fetch_json(PROPERTY_VALUES_URL, cache_dir)
    report = build_report(data, cache_dir)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report)
        print(f"Wrote {args.output}", file=sys.stderr)
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
