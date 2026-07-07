# Nova design token dashboard

**For:** Claude / design agents working on Project Nova  
**Use:** `@`-attach or point agents here before spec, prototype, or stakeholder copy work  
**Initiative:** [`brief.md`](brief.md) · Visual spec: [`context-library/design-md/nova-classic/DESIGN.md`](../../../context-library/design-md/nova-classic/DESIGN.md)  
**Data source:** [Are We Design Tokens Yet?](https://firefoxux.github.io/arewedesigntokensyet/) (AWDTY)  
**Last refreshed:** 2026-06-26 (AWDTY `generatedAt`: 2026-06-26T08:18:40Z)

---

## Status at a glance

| Metric | Nova NTP | Legacy chrome | Whole tree |
| :---- | :---- | :---- | :---- |
| Font-size on token scale | **98.5%** | 6.3% | 64.7% |
| Core type scale in use | **6 / 6** | 2 / 6 | 6 / 6 |
| One-off font-size values | **5** | 40 | 93 |
| Hardcoded px font sizes | **1** (`56px`) | 6 | 17 |
| AI Window font-size tokenized | **100%** | — | — |
| New Tab CSS propagation | **77.5%** (Jun 2026) | — | ~59.6% avg |

### Property consolidation (Nova / newtab paths)

| Property | Token types | Hardcoded types | Tokenized |
| :---- | :---- | :---- | :---- |
| `font-size` | 9 | 29 | **86.6%** |
| `color` | 5 | 5 | **97.4%** |
| `gap` | 7 | 7 | **96.3%** |
| `border-radius` | 5 | 16 | **87.9%** |
| `padding` | 7 | 25 | **91.0%** |

### Trajectory

| Surface | Feb 2025 | Jul 2025 | Jun 2026 |
| :---- | :---- | :---- | :---- |
| New Tab CSS propagation | 28% | 60% | **77.5%** |
| Global AWDTY average | ~19% | ~26% | **~57%** |

---

## Surface health

| Surface | Token posture | Notes |
| :---- | :---- | :---- |
| **Nova NTP** (`activity-stream.css`) | Strong | Type/color/spacing on scale; dimensions still one-off |
| **Smart Window / AI Window** | Complete | 100% font-size tokenized; greenfield |
| **Acorn `moz-*` widgets** | Complete | All widget paths at 100% |
| **Preferences widgets** | Complete | Token-first rebuild |
| **Browser chrome themes** | Weak (~29% avg) | Long tail; urlbar, toolbar, panel UI |
| **URL bar** (`view-nova.css`, `view-proton.css`) | Weak | 0% font-size tokens; legacy `--urlbarView-*` vars |
| **CustomizableUI / Panel UI** | Weak (~23% avg) | `panelUI-shared.css` high non-token debt |

---

## Agent rules — implementation

When producing Nova specs, prototypes, or CSS:

1. **Use Acorn design tokens** — never invent hex, px, or em values when a token exists.
2. **Type:** prefer the 6-step scale (`--font-size-xsmall` → `--font-size-xxlarge`); add heading tokens only for explicit hierarchy.
3. **Space:** use `--space-*` tokens for padding, gap, margin — not raw `8px`, `16px`, etc.
4. **Color:** use `--text-color`, `--color-*`, `--background-color-*` — not hardcoded hex.
5. **Radius:** use `--border-radius-*` — not arbitrary px.
6. **Greenfield surfaces** (Smart Window, new components): **100% token-first** — match AI Window, not legacy chrome patterns.
7. **Legacy chrome work:** migrating to tokens is in scope; copying legacy one-offs (`0.8em`, `--urlbarView-small-font-size`) is not.
8. **Known acceptable exception on NTP:** `56px` hero/clock font-size (only remaining hardcoded px font-size on NTP).

### Core type scale

| Token | Use |
| :---- | :---- |
| `--font-size-xsmall` | Captions, metadata |
| `--font-size-small` | Compact UI, tabs, secondary labels |
| `--font-size-root` | Body default |
| `--font-size-large` | Emphasis |
| `--font-size-xlarge` | Subheadings |
| `--font-size-xxlarge` | Display / hero |

Heading tokens (`--font-size-heading-*`) for NTP hierarchy only when the 6-step scale isn't enough.

---

## Stakeholder messaging

Use **consolidation** metrics, not propagation %, as the headline.

### Say

- *"Nova New Tab: 98.5% of font sizes on a 6-step type scale."*
- *"97% of NTP text colors use design tokens."*
- *"Smart Window was built 100% token-first."*
- *"New Tab CSS went from 28% to 77% token coverage in 16 months."*
- *"Legacy chrome still has 40 one-off font-size values — that's the contrast."*

### Don't say

- Lead with *"59% propagation"* — blends Nova wins with unmigrated legacy chrome.
- Imply a browser-wide before/after font-size count unless you cite a specific AWDTY surface and metric (we do not have a indexed historical “before” count for the whole tree).

---

## Remaining debt (prioritized)

| Priority | Area | Issue | Top files |
| :---- | :---- | :---- | :---- |
| P1 | NTP dimensions | Hardcoded `16px` / `32px` widths & heights | `nova/activity-stream.css` (624 non-token refs) |
| P1 | URL bar chrome | Legacy vars, 0% font-size tokenization | `view-nova.css`, `view-proton.css`, `urlbar-searchbar.css` |
| P2 | Panel / toolbar | Low token coverage | `panelUI-shared.css`, `customizeMode.css` |
| P2 | Onboarding / ASRouter | High non-token count | `aboutwelcome.css`, `asrouter-newtab-multistage.css` |
| P3 | Platform globals | 0–6% on OS chrome globals | `toolkit/themes/*/global` |

Non-token debt fingerprint: **px dimensions** > legacy **var()** > hardcoded **hex**.

---

## Metric definitions

| Term | Meaning |
| :---- | :---- |
| **Tokenized %** | Share of declarations for a property using `var(--…)` design tokens (AWDTY / stylelint rules) |
| **One-off values** | Distinct hardcoded px, em, hex, or pre-token legacy vars |
| **Core type scale** | 6 steps: xsmall → xxlarge |
| **Propagation %** | AWDTY unweighted directory average — engineering metric; secondary for stakeholders |
| **Consolidation** | Fewer distinct values → named scales (better PM narrative) |

---

## Related artifacts

| File | Purpose |
| :---- | :---- |
| [`scripts/nova-token-scorecard.py`](scripts/nova-token-scorecard.py) | Regenerate metrics from live AWDTY data |
| [`drafts/nova-token-scorecard-latest.md`](drafts/nova-token-scorecard-latest.md) | Auto-generated snapshot (re-run script) |
| [`drafts/nova-design-token-scorecard.md`](drafts/nova-design-token-scorecard.md) | PM slide deck draft |
| [`context-library/design-md/nova-classic/DESIGN.md`](../../../context-library/design-md/nova-classic/DESIGN.md) | Visual design spec (color, geometry, components) |
| [AWDTY Token Stats](https://firefoxux.github.io/arewedesigntokensyet/token-stats/) | Token usage counts |
| [AWDTY Non-token Values](https://firefoxux.github.io/arewedesigntokensyet/non-token-values/) | Searchable hardcoded values |

---

## Refresh

```bash
python3 data/projects/2026-02-project-nova/scripts/nova-token-scorecard.py \
  --output data/projects/2026-02-project-nova/drafts/nova-token-scorecard-latest.md
```

After running, update the **Status at a glance** and **Trajectory** tables in this file from `nova-token-scorecard-latest.md`. Re-run monthly or before stakeholder reviews.
