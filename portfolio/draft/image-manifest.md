# Image manifest — portfolio full site

**Last updated:** 2026-07-07  
**Rule:** One image = one narrative beat. Export **2× PNG** from Figma; drop into `site/assets/` with the filename below. SVG placeholders exist until PNG replaces them.

**Quick export:** Open `Portfolio 2026.fig` → select frame → Export PNG @2x → save to path in **Deploy path** column.

**Redaction:** Run `redaction-checklist.md` on every image before public deploy.

---

## Status key

| Symbol | Meaning |
|--------|---------|
| ⬜ | Placeholder SVG only — export PNG |
| 🟡 | PNG exported, not yet reviewed |
| ✅ | Redaction passed, live on site |

---

## Home (`index.html`)

| Status | Section | Narrative job | Figma source | Deploy path | Alt text |
|--------|---------|---------------|--------------|-------------|----------|
| ⬜ | Hero | Editorial cover — name + role on black | Cover / Hello frame | `site/assets/cover-hello.png` | Brooke Katalinich portfolio cover — Director Mobile and AI UX |

---

## Firefox lead (`work/firefox-ai-nova.html`)

Accent: `#7845e8` only on this page.

**Last updated:** 2026-07-07 (user mocks wired)

| Status | Section | Narrative job | Source | Deploy path | Alt text |
|--------|---------|---------------|--------|-------------|----------|
| ✅ | **Overview hero cluster** | Two bets, one standard — desktop NTP + mobile + Smart Window | User mocks (HNT, HNT Nova, SW) | See cluster below | Composed on `firefox-ai-nova.html` |
| ✅ | Hero · back | Nova desktop NTP | HNT-template mock | `site/assets/firefox/nightly/nova-ntp.png` | Nova desktop new tab — widgets, shortcuts, habit loops |
| ✅ | Hero · mobile | Nova mobile NTP | HNT_-_Nova mock | `site/assets/firefox/nightly/nova-mobile-ntp.png` | Nova mobile new tab — shortcuts, Jump Back In |
| ✅ | Hero · smart | Smart Window agentic panel | SW mock | `site/assets/firefox/nightly/smart-window-ai.png` | Smart Window with opt-in AI panel beside the page |
| ✅ | Three modes · Private | On-device, maximum privacy | Private_Window mock | `site/assets/firefox/smart-window/mode-private.png` | Private window — leave no traces on this device |
| ✅ | Three modes · Classic | Familiar Firefox NTP | Reuses `nova-ntp.png` | (same) | Classic Nova new tab |
| ✅ | Three modes · Smart Window | Opt-in agentic AI | Reuses `smart-window-ai.png` | (same) | Smart Window AI panel |
| ⬜ | Stakes | Device ecosystem — sameness + switch-worthy | Figma · "Imagine what's next" | `site/assets/firefox/device-ecosystem.png` | Firefox device ecosystem |
| ⬜ | Pillars | Agentic · Habit Loops · Localization | Figma key slide | `site/assets/firefox/pillars.png` | Firefox experience pillars |
| ⬜ | Process | Brand timeline 2025 / 2026+ | Figma slide | `site/assets/firefox/brand-timeline.png` | Firefox brand timeline |
| ⬜ | Proof | Nova chrome strip (optional) | Nightly capture | `site/assets/firefox/nightly/nova-chrome.png` | Nova chrome in Nightly |

**Redaction:** No internal OKR numbers, unreleased AI partner UI, mobile-only metrics not cleared.

---

## Project Nova deep dive (`work/nova.html`)

| Status | Section | Narrative job | Source | Deploy path | Alt text |
|--------|---------|---------------|--------|-------------|----------|
| ✅ | Hero | Desktop NTP | HNT-template mock | `site/assets/firefox/nightly/nova-ntp.png` | Wired |
| ✅ | Proof | Mobile NTP | HNT_-_Nova mock | `site/assets/firefox/nightly/nova-mobile-ntp.png` | Wired |
| ⬜ | Proof | NTP propagation visual | Figma craft pillars or AWDTY screenshot | `site/assets/firefox/craft-pillars.png` | Nova design craft pillars — target experience, visual refinement, iterative process |
| ⬜ | Community | Public feedback loop | Screenshot of community landing (public) | `site/assets/firefox/community-tracker.png` | Nova community impact — public Reddit and Connect replies |

**Redaction:** Max 3 decision rows in HTML — no colleague POC names. Use sample rows in `01-project-nova.md` only.

---

## Smart Window deep dive (`work/smart-window.html`)

| Status | Section | Narrative job | Source | Deploy path | Alt text |
|--------|---------|---------------|--------|-------------|----------|
| ✅ | Hero | Three modes row | User mocks | Private + NTP + SW reuses | Wired |
| ✅ | Proof | Smart Window AI | SW mock | `site/assets/firefox/nightly/smart-window-ai.png` | Wired |

---

## Operating model (`work/operating-model.html`)

No Figma accent — white on black or neutral diagrams.

| Status | Section | Narrative job | Source | Deploy path | Alt text |
|--------|---------|---------------|--------|-------------|----------|
| ⬜ | Hero | Four-layer operating system | Diagram (Figma or export from brief) | `site/assets/operating-model/four-layers.png` | AI-native design operating system — program, triad, org capability, velocity proof |
| ⬜ | Three bets | QA · Faster calls · Code not slides | `brief.shareable.md` visual or Figma | `site/assets/operating-model/three-bets.png` | Three velocity bets — QA closure, faster tactical calls, code-native stretch |
| ⬜ | Tools | PD-OS dashboard (optional) | Local screenshot — crop names | `site/assets/operating-model/pd-os-dashboard.png` | PD-OS critique prep dashboard — design operating system |

**Redaction:** Crop colleague names from dashboard. No Jira board IDs.

---

## Venmo prior work (`work/venmo-experience-vision.html`)

Accent: `#0074DE` only on this page.

| Status | Section | Narrative job | Figma source | Deploy path | Alt text |
|--------|---------|---------------|--------------|-------------|----------|
| ⬜ | Hero | Experience Vision 2024 cover | Venmo · Cover | `site/assets/venmo/cover.png` | Venmo Experience Vision 2024 — strategic vision cover |
| ⬜ | The call | Intention + Magic | Intention + Magic slides | `site/assets/venmo/intention-magic.png` | Venmo 2024 intention — cohesive target experience and experience mood |
| ⬜ | Prioritization | Gap matrix 2×2 | Gap matrix slide | `site/assets/venmo/gap-matrix.png` | Venmo experience gap matrix — Simple to Enriching, Local to Social |
| ⬜ | Value props | Three-up celebrate / simple / spirit | Value props slide | `site/assets/venmo/value-props.png` | Venmo value props — celebrate customers, simple and intuitive, Venmo spirit |
| ⬜ | North star | Take Venmo Anywhere | Vision statement slide | `site/assets/venmo/vision-anywhere.png` | Venmo Anywhere vision — from splitting bills to financial confidence |
| ⬜ | Process | Workstreams timeline | C2 Priorities / workstreams | `site/assets/venmo/workstreams.png` | Venmo 2024 workstreams — product thinking, benchmarking, vision journey |
| ⬜ | Proof | Commerce flywheel | Flywheel diagram | `site/assets/venmo/flywheel.png` | Venmo commerce flywheel — reach, sellers, relevancy loops |

**Redaction:** No unreleased PayPal metrics, seller data, or confidential OKR targets on slides.

---

## About + How I work (optional)

| Status | Page | Narrative job | Source | Deploy path |
|--------|------|---------------|--------|-------------|
| ⬜ | About | Maven course card | maven.com screenshot or Figma | `site/assets/about/maven-course.png` |
| ⬜ | How I work | Tool stack diagram | Figma or simple diagram | `site/assets/about/tool-stack.png` |

Skip if time-boxed — prose-only is fine on these pages.

---

## 30-minute export sprint (do in this order)

1. **Figma batch 1 (10 min)** — `cover-hello.png`, `firefox/overview.png`, `firefox/brand-timeline.png`, `venmo/cover.png`, `venmo/gap-matrix.png`
2. **Figma batch 2 (10 min)** — remaining Firefox + Venmo slides from tables above
3. **Nightly batch (10 min)** — capture `nova-chrome.png`, `nova-ntp.png`, `smart-window-ai.png` from public Nightly build
4. **Drop files** — same basename as manifest; refresh browser (PNG auto-replaces SVG via `<picture>`)
5. **Redaction pass** — skim each PNG at 100% zoom before `git push`

---

## File tree (target)

```
site/assets/
├── cover-hello.png
├── firefox/
│   ├── overview.png
│   ├── vision-statement.png
│   ├── device-ecosystem.png
│   ├── pillars.png
│   ├── brand-timeline.png      ⬜
│   ├── craft-pillars.png       ⬜
│   ├── modes-three-up.png
│   ├── community-tracker.png
│   ├── nightly/
│   │   ├── nova-ntp.png          ✅ desktop NTP (overview + Classic mode)
│   │   ├── nova-mobile-ntp.png   ✅ mobile NTP
│   │   ├── smart-window-ai.png   ✅ agentic panel (overview + Smart mode)
│   │   └── nova-chrome.png       ⬜ optional chrome strip
│   └── smart-window/
│       ├── mode-private.png      ✅ Private mode
│       └── states.png            ⬜ thinking/error states (future)
├── venmo/
│   ├── cover.png
│   ├── intention-magic.png
│   ├── gap-matrix.png
│   ├── value-props.png
│   ├── vision-anywhere.png
│   ├── workstreams.png
│   └── flywheel.png
└── operating-model/
    ├── four-layers.png
    ├── three-bets.png
    └── pd-os-dashboard.png
```

---

## HTML pattern (wired on site)

**Overview hero cluster** (`firefox-ai-nova.html`):
```html
<section class="hero-cluster hero-cluster--firefox">…</section>
```

**Three modes row**:
```html
<div class="modes-three">…</div>
```

**Single figure** (remaining placeholders):

Regenerate SVG placeholders: `python3 site/scripts/generate-placeholders.py`

---

## Claude Design sessions (after PNG export)

| Session | Upload |
|---------|--------|
| 1 | `DESIGN.md` + `firefox/overview.png` + `01-firefox-ai-nova-vision.md` |
| 2 | `cover-hello.png` + `home.md` |
| 3 | Nova + Smart Window PNGs + deep-dive markdown |
| 4 | Venmo PNGs + `00-venmo-experience-vision.md` |
| 5 | Operating model PNGs + `03-design-operating-model.md` |
