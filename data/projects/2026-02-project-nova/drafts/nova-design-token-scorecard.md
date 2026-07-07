# Nova design implementation — token consolidation (PM deck draft)

**Purpose:** Stakeholder-friendly metrics for how Nova streamlines design implementation via design tokens.  
**Source:** [Are We Design Tokens Yet?](https://firefoxux.github.io/arewedesigntokensyet/) — refreshed via `../scripts/nova-token-scorecard.py`  
**Audience:** PM, cross-functional leads, leadership updates  
**Last updated:** 2026-06-26

---

## Slide 1 — The headline

### Nova puts design on a system, not a spreadsheet of one-offs

**Before (legacy chrome):** dozens of arbitrary CSS values per property — hard to maintain, hard to keep consistent across surfaces.

**After (Nova-built UI):** named scales for type, color, spacing, and radius — one change updates the whole surface.

> **98.5%** of New Tab font sizes now use the design type scale (AWDTY).  
> **97%** of New Tab text colors use design tokens.  
> Smart Window was built **100% token-first**.

---

## Slide 2 — Typography on a named scale

### Nova NTP routes typography through Acorn’s 6-step type scale

| | Legacy browser chrome | Nova New Tab |
| :---- | :---- | :---- |
| Font-size declarations on tokens | **6%** | **98.5%** |
| One-off font-size values (AWDTY) | **40** | **5** |
| Hardcoded px font sizes | **6** | **1** (`56px` hero/clock) |

**The scale (Acorn):**

| Token | Typical use |
| :---- | :---- |
| `--font-size-xsmall` | Captions, metadata |
| `--font-size-small` | Compact UI, tabs |
| `--font-size-root` | Body default |
| `--font-size-large` | Emphasis |
| `--font-size-xlarge` | Subheadings |
| `--font-size-xxlarge` | Display / hero |

**Talk track:**  
*"On Nova New Tab, 98.5% of font-size declarations use the design type scale — six named steps, not one-off pixel values. Legacy chrome themes still carry 40 distinct one-off font-size values (6% tokenized). That's the contrast."*

**Do not say:** a browser-wide *"we went from X font sizes to 6"* unless X is measured for a specific surface from AWDTY. We have no indexed historical before-count for the whole tree.

---

## Slide 3 — Color, spacing, radius

### Nova consolidates the whole visual vocabulary, not just type

| Property | Nova / newtab | What it means |
| :---- | :---- | :---- |
| Text `color` | **97%** on tokens | Palette-driven, not one-off hex |
| `gap` / spacing | **96%** on tokens | 7-step space scale |
| `border-radius` | **88%** on tokens | 5 named radius tokens |
| `padding` | **91%** on tokens | Same space scale as gap |

**Talk track:**  
*"Nova isn't just a visual refresh — it's a implementation model. Color, spacing, and corner radius all route through named tokens, the same way typography does."*

---

## Slide 4 — Greenfield proof (Smart Window)

### Surfaces built during Nova don't inherit legacy debt

| Surface | Font-size tokenized | Hardcoded px sizes |
| :---- | :---- | :---- |
| AI Window / Smart Window | **100%** | **0** |
| Acorn `moz-*` widgets | **100%** | **0** |
| Preferences widgets | **100%** | **0** |
| URL bar chrome | **0%** | legacy `--urlbarView-*` vars |

**Talk track:**  
*"Smart Window and our component library were built token-first. The remaining gap is legacy chrome — toolbar, urlbar, panel UI — not the new product surfaces."*

---

## Slide 5 — Momentum

### New Tab CSS token coverage: 28% → 77% in 16 months

| Date | New Tab CSS propagation |
| :---- | :---- |
| Feb 2025 | 28% |
| Jul 2025 | 60% |
| Jun 2026 | 77% |

Global browser average today: **~60%** — useful for engineering, but a weaker stakeholder headline because it blends Nova wins with unmigrated legacy chrome.

**Talk track:**  
*"Nova New Tab went from under a third to over three-quarters token coverage in about a year. The long tail is chrome theming, not the surfaces we redesigned."*

---

## Slide 6 — What's left (honest close)

### Nova streamlined the vocabulary; dimensions are the next pass

Remaining non-token debt on Nova paths is mostly **dimensional**, not color or type:

- `nova/activity-stream.css` — icon/card widths and heights (`16px`, `32px`)
- `view-nova.css` — urlbar chrome still on pre-token legacy variables

**Talk track:**  
*"We've consolidated type, color, spacing, and radius. The next consolidation target is hardcoded dimensions in NTP layout and urlbar chrome migration."*

---

## Appendix — Metric definitions

| Term | Definition |
| :---- | :---- |
| **Tokenized %** | Share of CSS declarations for a property that reference a design token (`var(--…)` matching Acorn/stylelint rules) |
| **One-off values** | Distinct hardcoded values (px, em, hex, legacy vars) that aren't design tokens |
| **Core type scale** | 6 body/display steps: xsmall → xxlarge |
| **Propagation %** | AWDTY directory average — engineering coverage metric; use as secondary, not headline |

---

## Refresh instructions

```bash
python3 data/projects/2026-02-project-nova/scripts/nova-token-scorecard.py \
  --output data/projects/2026-02-project-nova/drafts/nova-token-scorecard-latest.md
```

Re-run monthly or before stakeholder reviews. Compare `generatedAt` in the output to confirm fresh data.
