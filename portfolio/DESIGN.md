---
version: alpha
name: Portfolio-2026
base: bmw-m
source: https://getdesign.md/bmw-m/design-md
description: |
  Brooke Katalinich portfolio (2026). Base system: getdesign.md bmw-m — near-black canvas,
  bold uppercase display, full-bleed photography/mockups, minimal chrome. Adapted for design-director
  case studies (Venmo, Firefox Nova, operating model). Copy source: portfolio/draft/. Visual reference:
  Portfolio 2026.fig.

colors:
  primary: "#ffffff"
  ink: "#ffffff"
  body: "#bbbbbb"
  body-strong: "#e6e6e6"
  muted: "#7e7e7e"
  hairline: "#3c3c3c"
  hairline-strong: "#262626"
  canvas: "#000000"
  surface-card: "#1a1a1a"
  surface-elevated: "#262626"
  surface-soft: "#0d0d0d"
  on-primary: "#000000"
  on-dark: "#ffffff"
  accent-firefox: "#7845e8"
  accent-firefox-soft: "rgba(120, 69, 232, 0.15)"
  accent-venmo: "#0074DE"
  accent-venmo-soft: "rgba(0, 116, 222, 0.15)"
  m-blue-light: "#0066b1"
  m-blue-dark: "#1c69d4"
  m-red: "#e22718"
  warning: "#f4b400"
  success: "#0fa336"

typography:
  display-xl:
    fontFamily: "SF Pro Display, Inter, BMWTypeNextLatin, -apple-system, BlinkMacSystemFont, sans-serif"
    fontSize: 80px
    fontWeight: 700
    lineHeight: 1
    letterSpacing: -0.02em
    fontStretch: condensed
  display-slide:
    fontFamily: "SF Pro Display, Inter, BMWTypeNextLatin, -apple-system, BlinkMacSystemFont, sans-serif"
    fontSize: 62px
    fontWeight: 700
    lineHeight: 1
    letterSpacing: -0.02em
    fontStretch: condensed
  display-lg:
    fontFamily: "SF Pro Display, Inter, BMWTypeNextLatin, sans-serif"
    fontSize: 56px
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: -0.02em
    fontStretch: condensed
  display-md:
    fontFamily: "SF Pro Display, Inter, BMWTypeNextLatin, sans-serif"
    fontSize: 40px
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: -0.02em
    fontStretch: condensed
  display-sm:
    fontFamily: "SF Pro Display, Inter, BMWTypeNextLatin, sans-serif"
    fontSize: 32px
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: 0
  title-lg:
    fontFamily: "SF Pro Text, Inter, BMWTypeNextLatin, sans-serif"
    fontSize: 24px
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: 0
  title-md:
    fontFamily: "SF Pro Text, Inter, BMWTypeNextLatin, sans-serif"
    fontSize: 20px
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: 0
  title-sm:
    fontFamily: "SF Pro Text, Inter, BMWTypeNextLatin, sans-serif"
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: 0
  label-uppercase:
    fontFamily: "SF Pro Text, Inter, BMWTypeNextLatin, sans-serif"
    fontSize: 14px
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: 1.5px
  body-md:
    fontFamily: "SF Pro Text, Inter, BMWTypeNextLatin Light, sans-serif"
    fontSize: 24px
    fontWeight: 400
    lineHeight: 1.35
    letterSpacing: 0
  body-sm:
    fontFamily: "SF Pro Text, Inter, BMWTypeNextLatin Light, sans-serif"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: 0
  list-num:
    fontFamily: "SF Pro Display, Inter, BMWTypeNextLatin, sans-serif"
    fontSize: 62px
    fontWeight: 700
    lineHeight: 1
    fontStretch: condensed
  caption:
    fontFamily: "SF Pro Text, Inter, BMWTypeNextLatin, sans-serif"
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: 0.5px
  button:
    fontFamily: "SF Pro Text, Inter, BMWTypeNextLatin, sans-serif"
    fontSize: 14px
    fontWeight: 700
    lineHeight: 1
    letterSpacing: 1.5px
  nav-link:
    fontFamily: "SF Pro Text, Inter, BMWTypeNextLatin, sans-serif"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: 0.5px

rounded:
  none: 0px
  xs: 2px
  sm: 4px
  md: 6px
  full: 9999px

spacing:
  xxs: 4px
  xs: 8px
  sm: 12px
  md: 16px
  lg: 24px
  xl: 40px
  xxl: 64px
  section: 96px

components:
  button-primary:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.on-dark}"
    typography: "{typography.button}"
    rounded: "{rounded.none}"
    padding: 16px 32px
    height: 48px
  button-primary-outline:
    backgroundColor: transparent
    textColor: "{colors.on-dark}"
    typography: "{typography.button}"
    rounded: "{rounded.none}"
    padding: 16px 32px
    height: 48px
  button-accent-firefox:
    backgroundColor: "{colors.accent-firefox}"
    textColor: "{colors.on-dark}"
    typography: "{typography.button}"
    rounded: "{rounded.none}"
    padding: 16px 32px
    height: 48px
  button-accent-venmo:
    backgroundColor: "{colors.accent-venmo}"
    textColor: "{colors.on-dark}"
    typography: "{typography.button}"
    rounded: "{rounded.none}"
    padding: 16px 32px
    height: 48px
  top-nav:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.on-dark}"
    typography: "{typography.nav-link}"
    height: 64px
  hero-photo-band:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.on-dark}"
    typography: "{typography.display-xl}"
    padding: 96px
  overview-slide:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.on-dark}"
    typography: "{typography.display-slide}"
    padding: 96px
  case-study-band-firefox:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.on-dark}"
    accentColor: "{colors.accent-firefox}"
    typography: "{typography.display-slide}"
    padding: 96px
  case-study-band-venmo:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.on-dark}"
    accentColor: "{colors.accent-venmo}"
    typography: "{typography.display-slide}"
    padding: 96px
  proof-stat:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.accent-firefox}"
    typography: "{typography.display-sm}"
    rounded: "{rounded.none}"
    padding: 24px
  feature-photo-card:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.on-dark}"
    typography: "{typography.title-md}"
    rounded: "{rounded.none}"
    padding: 24px
  footer:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.body}"
    typography: "{typography.body-sm}"
    padding: 64px
---

## Portfolio 2026 — usage

This file is the visual contract for **Claude Design**, **Cursor**, and **Claude Code `/design-sync`**.

| Source | Role |
|--------|------|
| `portfolio/draft/` | Copy source of truth — never invent metrics or titles |
| `Portfolio 2026.fig` | Pixel reference for slide layout |
| `portfolio/DESIGN.md` | Tokens, components, constraints (this file) |
| `portfolio/site/` | Deploy target after design is locked |

### Case-study accent rules

- **Firefox / Nova pages:** use `{colors.accent-firefox}` only — CTAs, stat highlights, focus rings.
- **Venmo pages:** use `{colors.accent-venmo}` only.
- **Home, About, How I work:** white on black only — no case-study accent.
- **Never mix** Firefox purple and Venmo blue in the same viewport.

### Slide patterns (from Figma)

**Overview slide** (`{component.overview-slide}`): black full-bleed band; `{typography.display-slide}` for "Overview", "Responsibilities", "Impact"; `{typography.list-num}` for 1/2/3; `{typography.body-md}` at 24px for list copy; device mockups rotated −45° on the right, exported as PNG (do not rebuild in CSS).

**Hello cover:** centered display wordmark on `{colors.canvas}`; minimal chrome.

### Content constraints

- Run `portfolio/draft/redaction-checklist.md` before any public export.
- Do not invent employer titles, dates, or unreleased metrics.
- Tone: decision quality over deliverable volume — editorial, not Dribbble.

---

## Overview

Black canvas (`{colors.canvas}`) with white condensed display type. Photography and device mockups carry visual weight; UI chrome stays minimal. Based on [getdesign.md bmw-m](https://getdesign.md/) — motorsport editorial discipline adapted for a design-director portfolio deck rendered as a site.

**Key characteristics:**
- True black background on hero and case-study slides
- `{typography.display-slide}` (62px condensed) for Figma-matched slide titles
- `{typography.display-xl}` (80px) for cover and home hero
- Heavy display (700) + light body (400 at 24px on slides, 16px in prose)
- `{rounded.none}` default — sharp rectangles, not SaaS pills
- Full-bleed mockup photography; depth from imagery, not drop shadows

## Colors

### Portfolio accents
- **Accent Firefox** (`{colors.accent-firefox}` — #7845e8): Nova / Smart Window case studies only.
- **Accent Venmo** (`{colors.accent-venmo}` — #0074DE): Venmo Experience Vision only.
- Soft variants for subtle backgrounds: `{colors.accent-firefox-soft}`, `{colors.accent-venmo-soft}`.

### Surface & text
- **Canvas** (`{colors.canvas}` — #000000): Default page and slide floor.
- **Surface Card** (`{colors.surface-card}` — #1a1a1a): Proof stats, cards on dark.
- **Ink / On Dark** (`{colors.on-dark}` — #ffffff): Headlines, primary text.
- **Body** (`{colors.body}` — #bbbbbb): Secondary copy on dark.
- **Muted** (`{colors.muted}` — #7e7e7e): Meta, footer, captions.

## Typography

| Token | Size | Use |
|-------|------|-----|
| `{typography.display-xl}` | 80px | Cover, home hero |
| `{typography.display-slide}` | 62px | Slide titles — Overview, Responsibilities, Impact |
| `{typography.list-num}` | 62px | Large numbered list indices (1, 2, 3) |
| `{typography.display-lg}` | 56px | Section heads |
| `{typography.body-md}` | 24px | Slide body copy, responsibility lines |
| `{typography.body-sm}` | 16px | Case study prose, footer |

**Font stack:** SF Pro Display/Text with Inter fallback. BMW M used condensed bold display + light body as the structural model.

## Components

See YAML frontmatter for token refs. Primary patterns:

- `{component.overview-slide}` — Firefox/Venmo overview slides from Figma
- `{component.case-study-band-firefox}` / `{component.case-study-band-venmo}` — chapter openers with case accent
- `{component.hero-photo-band}` — full-bleed hero with display headline
- `{component.proof-stat}` — metric cards (+14% DAU, token propagation, etc.)
- `{component.button-primary-outline}` — ghost CTA on photography

## Do's and Don'ts

### Do
- Read `portfolio/draft/` before writing copy.
- Export phone mockups from Figma as PNG; place with CSS transform rotate(-45deg) only if using pre-composited assets.
- One case-study accent color per page.
- Use `{spacing.section}` (96px) between major bands.

### Don't
- Don't use cream/violet placeholder palette from old `styles.css`.
- Don't codegen three iPhones from Figma MCP asset URLs.
- Don't mix Venmo blue and Firefox purple on the same screen.
- Don't bold body text on slides — hierarchy is size, not weight.

## Handoff

1. **Claude Design:** upload this file + Figma PNG + relevant `draft/case-studies/*.md`.
2. **Lock design** on canvas before code.
3. **Claude Code:** `/design-sync` → `portfolio/site/`.
4. **Redaction checklist** → deploy.

---

_Base system: [getdesign.md bmw-m](https://getdesign.md/). Regenerate base with `npx getdesign@latest add bmw-m` and re-apply Portfolio overrides above._
