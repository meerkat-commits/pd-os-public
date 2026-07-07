# Claude workflow — Portfolio 2026

Handoff doc for **Claude Design** and **Claude Code**. Read this first in any portfolio session.

**Owner:** Brooke Katalinich  
**Goal:** VP-positioned portfolio — platform bets, AI-native org transformation, agentic workflows, documented decisions.  
**Audience:** VP / CPO hire · speaking (Maven, Substack) · advisory · Mozilla peers.

**State:** Copy locked in `draft/`. Visual design not started. `site/styles.css` is placeholder.

---

## Sources of truth

| What | Where | Claude's role |
|------|--------|---------------|
| Copy and narrative | `portfolio/draft/` | Read only. Do not invent titles, dates, or metrics. |
| Career facts | `draft/resume.md` | Locked timeline — Rocket, PayPal, Mozilla |
| Tool stack and bets | `draft/ai-native.md` | Canonical reference for agentic workflows |
| Session state | `THREAD-HANDOFF.md` | What's done vs next |
| Visual tokens | `portfolio/DESIGN.md` | Follow exactly. Base: [getdesign.md bmw-m](https://getdesign.md/bmw-m/design-md). |
| Pixel reference | `Portfolio 2026.fig` → PNG exports | Match layout; see `draft/image-manifest.md` for filenames. |
| Deploy target | `portfolio/site/` | Write here only after design is locked on canvas. |
| Redaction | `portfolio/draft/redaction-checklist.md` | Run before any public export or deploy. |

**PD-OS depth (if more context needed):**

| Case study | PD-OS path |
|------------|------------|
| Nova | `data/projects/2026-02-project-nova/` |
| Smart Window | `.cursor/skills/smart-window-design/` |
| Operating model | `data/projects/2026-06-ai-velocity-mandate/brief.shareable.md` |
| Token metrics | `data/projects/2026-02-project-nova/dashboard-design-tokens.md` |

---

## Tool routing

```
Edit copy          →  PD-OS / Cursor (portfolio/draft/)
Visual design      →  Claude Design (claude.ai/design)
Lock + iterate     →  Claude Design canvas (inline edits, comments)
Code handoff       →  Claude Code (/design-sync from DESIGN.md)
Resume / LinkedIn  →  draft/resume.md, draft/linkedin.md
Deploy             →  portfolio/site/ → Netlify / GitHub Pages / Cloudflare
```

**Do not use Figma MCP → HTML codegen** for full slides. Export PNGs from Figma instead.

---

## Before session 1 — Figma exports

Export from `Portfolio 2026.fig` at **2× PNG**. Save to `portfolio/site/assets/`:

| File | Figma source | Used on |
|------|--------------|---------|
| `cover-hello.png` | Cover / Hello frame | Home |
| `firefox-overview.png` | FF page · Overview (`497:2547`) | Firefox case study opener |
| `venmo-intention.png` | Venmo · Intention slide | Venmo case study |
| `venmo-gap-matrix.png` | Venmo · Gap matrix | Venmo case study |
| `venmo-vision-statement.png` | Venmo · "Take Venmo Anywhere" | Venmo hero |

Optional: phone mockup clusters as single flattened PNGs per slide.

---

## Claude Design — session order

Build in deck order. Lock each screen before moving on.

### Session 0 — Onboard the project

**Upload:** `DESIGN.md`, this file, `THREAD-HANDOFF.md`, `draft/home.md`, `draft/about.md`, `draft/ai-native.md`

**Prompt:**

```
You are building Brooke Katalinich's 2026 VP-positioned design portfolio.

Read DESIGN.md as the visual contract. Read claude-workflow.md for process.
Read THREAD-HANDOFF.md for locked narrative and career facts.
Copy comes from portfolio/draft/ only — never invent metrics, titles, or dates.

Positioning: AI-native design executive owning Firefox's 2026 bets (Nova + Smart Window)
across a 35-person hybrid org. Agentic workflows, proof bars, Maven teaching.

Tone: editorial keynote deck as a website — black slides, condensed white type,
device mockups as photography. Humanized voice — plain prose, no bold in body paragraphs.

Accent rules: Firefox #7845e8 on Mozilla pages only, Venmo #0074DE on Venmo pages only,
never mixed in one viewport.
```

---

### Session 1 — Firefox Overview slide (proof)

**Upload:** `DESIGN.md`, `firefox-overview.png`, `draft/case-studies/01-firefox-ai-nova-vision.md`

**Prompt:**

```
Recreate the attached Firefox Overview slide using DESIGN.md tokens.

Layout:
- Black full-bleed background (#000)
- Left: "Overview", responsibilities, impact stats from markdown (public-safe only)
- Right: three rotated phone mockups (use PNG as reference; export as images)
- Type: display-slide 62px condensed bold for headings; body-md 24px for list copy

Copy exactly from draft/case-studies/01-firefox-ai-nova-vision.md.
Accent: #7845e8 for stat emphasis only if needed.
Do not use +14% DAU unless confirmed in draft (it is not — use proof table from markdown).
```

---

### Session 2 — Home + Hello cover

**Upload:** `DESIGN.md`, `cover-hello.png`, `draft/home.md`

**Prompt:**

```
Build the portfolio home page from draft/home.md.

Hero: Hello cover treatment on black canvas (reference cover-hello.png).
Below: proof strip (5 stats from home.md), philosophy block (4 principles),
case study cards (Firefox AI+Nova → Operating system → Venmo prior work),
audience routing (VP / AI-native / Director / Speaking / Advisory).

Follow DESIGN.md. No case-study accent on home — white on black only.
Humanized voice: no bold spam in paragraph copy.
Cards link to case study pages (paths in draft).
```

---

### Session 3 — Firefox deep dives + operating model

**Upload:** `draft/case-studies/01-project-nova.md`, `02-smart-window.md`, `03-design-operating-model.md`, `ai-native.md`

Build as linked pages from unified Firefox case study — not home-grid cards.

- Nova + Smart Window: accent `#7845e8`
- Operating model: white on black; link to tool stack content from `ai-native.md` where relevant

---

### Session 4 — Venmo (prior work)

**Upload:** `draft/case-studies/00-venmo-experience-vision.md`, Venmo PNG exports

Accent `#0074DE` only. Frame as prior SLT-approved strategic work, not lead narrative.

---

### Session 5 — About + How I work

**Upload:** `draft/about.md`, `draft/how-i-work.md`

About: bio, Firefox bets table, Maven teaching, VP open-to, contact links.  
How I work: agentic workflows, tool stack summary, PD-OS, hub, token scorecard.

---

### Session 6 — Polish + export

1. Walk every page against `DESIGN.md` Do's and Don'ts.
2. Check responsive: slide bands stack; mockups scale; type uses clamp().
3. Export format:
   - Recruiter PDF/PPTX from Claude Design
   - Live site HTML for handoff to Claude Code
4. Do not publish yet — run redaction first.

---

## Claude Code handoff

When canvas design is locked:

```
/design-sync

Repo: pd-os/portfolio/
Design contract: portfolio/DESIGN.md
Target: portfolio/site/
Copy source: portfolio/draft/

Implement the locked Claude Design export as static HTML + CSS.
No build step. Match DESIGN.md tokens. Propagate copy from draft/ markdown.
Do not revert to the old cream/violet placeholder styles.css palette.
Align all Work nav links to work/firefox-ai-nova.html.
```

---

## Design rules (quick reference)

From `DESIGN.md`:

- **Canvas:** `#000000` on heroes and case-study slides
- **Type:** condensed bold display (62px slides, 80px cover); 24px slide body; 16px prose
- **Accents:** one per page — Firefox `#7845e8` or Venmo `#0074DE`
- **Mockups:** PNG exports, rotated −45° if compositing — not CSS-rebuilt phones
- **Radius:** `{rounded.none}` default — sharp rectangles, not SaaS pills
- **Voice:** narrative over artifacts · AI-native builders at scale · discipline owners gate · proof has a bar

---

## Redaction gate (required before deploy)

Run `portfolio/draft/redaction-checklist.md`. Minimum pre-flight:

1. Grep site for: `Raja`, `Lattice`, `tier`, `calibrat`, confidential `@mozilla.com`
2. No unreleased Venmo/PayPal metrics
3. Decision registry: structure + max 3 public decisions only
4. Contact links filled in (`about.html`)
5. All external links resolve

---

## Known anti-patterns

| Don't | Do instead |
|-------|------------|
| Figma MCP → React/Tailwind codegen | Export slide PNG + match in Claude Design |
| Edit `site/*.html` copy directly | Edit `draft/` → propagate on design-sync |
| Mix Venmo blue + Firefox purple on one screen | One accent per viewport |
| Invent proof points | Use only what's in `draft/` |
| Deploy before redaction | Checklist every time |
| Bold every keyword in prose | Humanized plain voice from draft |

---

## Open items (human fills in)

- [ ] LinkedIn URL in `about.md` / `about.html`
- [ ] GitHub public repo link (PD-OS shareable export or other)
- [ ] Location (optional)
- [ ] Nightly screenshots → `site/assets/firefox/`
- [ ] Figma PNG exports → `site/assets/`
- [ ] Venmo hero slides export to `site/assets/venmo/`

## Done (no longer open)

- [x] Email in `about.md` (brooke.katalinich@gmail.com)
- [x] Career timeline in `resume.md` (Rocket, PayPal roles corrected)
- [x] VP positioning and AI-native copy in `draft/`
- [x] Maven course linked
- [x] Humanizer pass on draft copy

---

## Canonical one-liner

> I own Firefox's 2026 bets (Nova, Smart Window) and the operating system behind a 35-person hybrid org — enabling AI-native builders at scale with hub skills, triad gates, and proof bars.

Use in meta description, LinkedIn (`draft/linkedin.md`), and home hero.
