# Nova design token scorecard

_Generated 2026-06-26 19:21 UTC from [AWDTY](https://firefoxux.github.io/arewedesigntokensyet/) (source data: 2026-06-26T08:18:40.745Z)._

## Headline stats (PM-ready)

| Metric | Nova / NTP | Legacy chrome | Whole tree |
| :---- | :---- | :---- | :---- |
| Font-size on token scale | **98.5%** (NTP CSS) | 6.3% | 64.7% |
| Core type scale steps in use | **6** of 6 | 2 of 6 | 6 of 6 |
| One-off font-size values | **5** (NTP) | 40 | 93 |
| Hardcoded px font sizes left | **1** | 6 | 17 |
| AI Window font-size tokenized | **100.0%** (5 tokens) | — | — |

### Suggested talk track

- **NTP typography:** 98.5% of font-size declarations use design tokens; 6 core scale steps cover the surface.
- **Legacy contrast:** browser chrome themes still carry 40 one-off font-size values (6.3% tokenized).
- **Smart Window:** built token-first — 100.0% font-size coverage, 0 hardcoded px sizes.

## Property consolidation (Nova / newtab paths)

| Property | Token types | Hardcoded types | Tokenized |
| :---- | :---- | :---- | :---- |
| `font-size` | 9 | 29 | **86.6%** |
| `color` | 5 | 5 | **97.4%** |
| `gap` | 7 | 7 | **96.3%** |
| `border-radius` | 5 | 16 | **87.9%** |
| `padding` | 7 | 25 | **91.0%** |

## Trajectory

- **New Tab CSS propagation:** 2026-03: 69.2% → 2026-04: 72.5% → 2026-05: 75.9% → 2026-06: 77.5%
- **Nova CSS propagation:** 2026-03: 69.2% → 2026-04: 72.5% → 2026-05: 75.9% → 2026-06: 77.5%

## Core type scale (Nova NTP)

- `--font-size-large`
- `--font-size-root`
- `--font-size-small`
- `--font-size-xlarge`
- `--font-size-xsmall`
- `--font-size-xxlarge`

## Remaining hardcoded px font sizes (Nova NTP)

56px

## Caveats

- Counts are from AWDTY's scanned CSS paths, not the entire mozilla-central tree.
- Propagation % is an unweighted directory average; consolidation counts are more intuitive for stakeholders.
- Legacy `var(--urlbarView-*)` and similar pre-token variables count as hardcoded.
- Dimensional one-offs (`16px` widths/heights) remain the largest Nova debt in `activity-stream.css`.
