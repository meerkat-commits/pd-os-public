# Portfolio — Brooke Katalinich

VP-positioned portfolio for external hire, speaking, Maven teaching, and advisory.

**Copy is locked in `draft/`.** Next step: Claude Design Session 0 per `claude-workflow.md`.

## Layout

```
portfolio/
├── README.md                 ← you are here
├── DESIGN.md                 ← visual contract (bmw-m + portfolio overrides)
├── claude-workflow.md        ← Claude Design / Claude Code handoff (start here)
├── THREAD-HANDOFF.md         ← session state for new threads (read after long breaks)
├── draft/                    ← source copy (edit here first)
│   ├── home.md
│   ├── about.md
│   ├── resume.md             ← full VP-positioned resume (markdown)
│   ├── linkedin.md           ← headline + About copy for LinkedIn
│   ├── ai-native.md          ← Firefox bets, tool stack, agentic workflows
│   ├── how-i-work.md
│   ├── redaction-checklist.md
│   ├── image-manifest.md       ← image map: narrative → file → Figma source
│   └── case-studies/
│       ├── 00-venmo-experience-vision.md
│       ├── 01-firefox-ai-nova-vision.md
│       ├── 01-project-nova.md
│       ├── 02-smart-window.md
│       └── 03-design-operating-model.md
└── site/                     ← static HTML (no build step)
    ├── index.html            ← synced from draft (placeholder styles)
    ├── about.html
    ├── how-i-work.html
    ├── styles.css            ← placeholder — Claude Design replaces
    └── work/
        ├── venmo-experience-vision.html
        ├── firefox-ai-nova.html
        ├── nova.html
        ├── smart-window.html
        └── operating-model.html
```

## Workflow

1. **Edit copy** in `draft/` — markdown is the source of truth.
2. **Design** with Claude Design — follow `claude-workflow.md` (session order + prompts).
3. **Sync to HTML** when design is locked (Claude Code `/design-sync` or Cursor with `DESIGN.md`).
4. **Check redaction** against `draft/redaction-checklist.md` before any public deploy.
5. **Preview locally:**

```bash
cd portfolio/site
python3 -m http.server 8080
# open http://localhost:8080
```

## Claude Design — Session 0 attach list

1. `DESIGN.md`
2. `claude-workflow.md`
3. `THREAD-HANDOFF.md`
4. `draft/home.md`
5. `draft/about.md`
6. `draft/ai-native.md`
7. `draft/case-studies/01-firefox-ai-nova-vision.md`

Paste the Session 0 prompt from `claude-workflow.md`.

## Deploy

Static site — any host works (Netlify, GitHub Pages, Cloudflare Pages). Point the build/publish directory at `portfolio/site/`. Run redaction checklist first.

## TODO before launch

- [ ] Claude Design Sessions 0–6 (visual design)
- [ ] Figma PNG exports → `site/assets/` (see `draft/image-manifest.md`)
- [ ] Nightly screenshots → `site/assets/firefox/`
- [ ] LinkedIn URL in `about.md` / `about.html`
- [ ] GitHub public repo link
- [ ] Sync case study HTML from `draft/case-studies/` (or rebuild in Claude Design)
- [ ] Run redaction checklist on full site

## Done

- [x] VP + AI-native copy in `draft/`
- [x] Resume, LinkedIn, ai-native reference docs
- [x] Humanizer pass on draft copy
- [x] Career timeline corrected (Rocket, PayPal, Mozilla)
- [x] Maven course integrated
- [x] Email in about
- [x] Home, about, how-i-work HTML synced (placeholder styles)

## Related PD-OS sources

| Portfolio section | PD-OS source |
|-------------------|--------------|
| Nova case study | `data/projects/2026-02-project-nova/` |
| Smart Window | `.cursor/skills/smart-window-design/` |
| Operating model | `data/projects/2026-06-ai-velocity-mandate/brief.shareable.md` |
| Token metrics | `data/projects/2026-02-project-nova/dashboard-design-tokens.md` |
| Community story | `data/projects/2026-06-nova-podcast/drafts/nova-podcast-outline-v3.md` |

## Canonical one-liner

> I own Firefox's 2026 bets (Nova, Smart Window) and the operating system behind a 35-person hybrid org — enabling AI-native builders at scale with hub skills, triad gates, and proof bars.
