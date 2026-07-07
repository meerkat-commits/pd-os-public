# Team & Organizational Context

Reference material for Smart Window design work. This file holds team
contacts, engineering infrastructure, organizational terminology, and
the detailed override reasoning. The SKILL.md holds the design mindset
and working process. This file holds the context you check when you
need specific organizational details.

Last updated: March 2026

## Team Contacts

**Product:** Jolie Huang, Loren Austin, Tapan Kamdar (mgmt)
**UX:** Paul Annett, Katie Lower, Emanuela Damiani (mgmt)
**Engineering:** Ed Lee, Shruti Kamath (mgmt)

**Slack:**
- `#ai4dev` — main hub for AI development
- `#GenAI-private` — Gen AI team (private)
- `@fx-ai-ux` — Slack group to @mention all AI UX designers

**Code lands in:** Mozilla Central (code name "Smart Window")

## Engineering & Dev Tooling

**Our prototyping stack:**
- **Claude Code + Figma MCP** is our primary path for design work
- Firefox Development MCP server: `https://mcp-dev.moz.tools/mcp`
  (auto-configured from Firefox checkout)
- `AGENTS.md` / `CLAUDE.md` in the Firefox repo
- `searchfox-cli`, `treeherder-cli` (Rust CLI tools on crates.io)
- Sandbox mode (`/sandbox`) for safe prototyping

**Other team infrastructure (context, not our workflow):**
- GitHub Copilot, Codex CLI available but not our tools
- AI reviews live on Phabricator
- Claude Code enterprise-wide via Catalog (SSO login)

**Production environment:**
- Cross-platform: Windows, Mac, Linux (Gecko/XPFE)
- HTML/CSS/JS on Gecko — no React, no animation libraries
- Compositor-safe properties only (transform + opacity)
- WebGPU available from Firefox 141
- `linear()` easing shipped in Fx104 — our competitive advantage
- All extensions supported except themes

## Team AI Principles (Oct 2024)

Co-created by the Gen AI team:

1. **Create responsibly, for users and Mozilla** — Aligned. No override.
2. **Build trust** — Aligned. Our "Honest Craft" and "Show Your Work" are
   the motion-specific expression.
3. **Design to delight** — Reframed. Delight is an outcome of honest craft,
   not a goal. If delight is the brief, you get spectacle.
4. **Embrace variability and imperfection** — Strongly aligned. Uncertainty
   is a design opportunity, not a problem to hide.

## Team Terminology

- **"Consent required" / "consent not required" / "on/off by default"** —
  the team avoids "opt-in" / "opt-out"
- **Sparkles icon** = AI (committed, team-wide)
- **"AI-enhanced mode"** = what Smart Window is evolving toward
- Models are **optional components** in about:addons

## Detailed Override Reasoning

### Firefox Internal Motion Work

**2018 principles (Quick/Informative/Whimsical):** Replaced for Smart
Window. Quick is incomplete — speed without soul is a spreadsheet.
Informative is table stakes. Whimsical without guardrails = bounce in
a trust product. Still apply to Classic Mode icon-level microinteractions.

**Nova themes (Balanced/Snappy/Smooth/Calm):** Replaced. Vibes, not
principles. The testing tool is valuable. The theme model is gone.

**Bounce on hover:** Killed. Tone-deaf for privacy-first AI.

**Figma carousel values (500ms, cubic-bezier(0.5, 0, 0.2, 1)):** Not
rejected, but must be validated against named primitives.

**Shield micro-animation explorations:** Good instinct, wrong sequence.
System defines personality first, then components.

### Acorn Brand Principles

- "Crafted with care" — Aligned. Our standard.
- "Delightful" — Reframed as outcome not goal.
- "Empowering" — Aligned. Maps to kill switch, agency, control.
- "Trailblazing" — Made specific: our 5 design positions.

### Industry Motion Standards & Best Practices

We evaluated the full landscape of motion design frameworks, standards,
best practices, and industry thinking — from established design systems
to individual practitioner philosophies to platform-level guidance to
academic research. Where something aligned with our vision, we adopted
it. Where it didn't, we overrode it. Where it was partially right, we
took what served us and left the rest.

The detailed competitive research lives in `motion-landscape.md`. The
motion theory and technical foundations live in `ux-motion-foundations.md`.
Our principles and positions are the synthesis — not a copy of any single
framework, but an original system informed by everything and beholden to
nothing except our own craft standard.

Key positions that emerged from this evaluation:
- We use designed curves (cubic-bezier, linear()) over spring physics
  for system-initiated animations. Taste over physics. Intention over
  emergent behavior.
- We organize motion by interaction type (browser register / AI register),
  not by mood or theme.
- Our baseline for browser chrome is fast and invisible. Our AI moments
  earn the right to be noticed.
- We reject overshoot, bounce, and elastic easing for trust-critical UI.
  Warmth comes from the curve, not from simulation.
- We treat `prefers-reduced-motion` as a design starting point, not a
  compliance checkbox.
- Our motion system starts at principles (why) and extends to surface
  specs (what). Most systems start at timing and curves. That's Layer 2.
  We start at Layer 1.

### UX Pattern Overrides

**Sparkles animation:** No shimmer, twinkle, or magic performance.
Clean, warm motion. Test case for Honest Craft.

**Consent flow:** Not functional sequence — it's the hero animation.
First impression of Smart Window's motion personality.

**Local model quality:** Don't mask lower performance/reliability with
confident animation. Motion communicates quality difference honestly.

**Model removal:** Users remove via about:addons, not Smart Window.
Design what happens when user returns after external removal.

### The Meta-Override

Every industry framework treats motion systems as speed and easing.
Ours starts at principles and extends to surface specs. The speed
and easing serve the principles. Nobody else has built it this way.
