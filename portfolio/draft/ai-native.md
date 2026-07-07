# AI-native design: tool stack and agentic workflows

Canonical reference for resume, LinkedIn, portfolio, and speaking. Public-safe only.

---

## Firefox bets I own

### Company-priority platform bets (2026)

| Bet | What | Status | Design ownership |
|-----|------|--------|------------------|
| Project Nova | Full-browser redesign: chrome, new tab, onboarding, settings. First cohesive Firefox redesign since Proton. | In Nightly · public community feedback | UX lead · execution owner for Nova sign-off, punch QA, decision registry |
| Smart Window / AI Mode | Opt-in AI browsing on Mozilla's terms: Private, Classic, Smart Window. Agentic task completion in-window. | Shipping with Nova program gates · 100% AI Window font-size tokenized | Modes, transitions, thinking states, reduced-motion variants |
| AI-native org transformation | How a 35-person hybrid org ships with AI: operating system, triad gates, proof bars, skills hub. | 2026 H2 mandate · monthly exec proof | Velocity frame, operating rules, pillar coaching model |

### Experience pillars (Firefox UX vision to desktop + mobile)

| Pillar | User promise | Desktop / Nova expression |
|--------|--------------|---------------------------|
| Agentic | Browser carries the task with consent | Smart Window thinking states, history resume, mode transitions, shake-to-summarize (iOS) |
| Habit Loops | Reasons to return | NTP widgets, tab groups, vertical tabs, compact mode, switcher customization |
| Localization | Global-first, not US-default | DE/NA locale in nova-classic; community-in-thread feedback worldwide |

### Executive and growth partnership

- PLG and monetization: design partnership with Product, Engineering, Data, and Marketing
- Mobile + AI UX: unified mandate across mobile vision and desktop AI surfaces

### UX vision statement (public)

> Create transformational, user-centric browsing experiences that put people in control of their online lives. By reimagining the window to the web, we are attracting new users, inspiring those we have, and building a healthier internet for all.

2025 half: personalized, private, always there when you need it (Smart Window).  
2026+ half: youthful, fresh, built around authentic moments of delight (Nova).

---

## AI-native tool stack

### Design and prototype

| Tool | Role in workflow |
|------|------------------|
| Figma | Source of truth for specs, decks, stakeholder alignment. PNG export to Claude Design. |
| Figma Make | Rapid UI flow and variant generation. Taught in [AI-Driven Design (Maven)](https://maven.com/bkatalinich/ai-driven-design/preview/354376). |
| Loveable | Agentic prototyping for exploration and iteration chains |
| Figma Desktop MCP | Design context when local `.fig` is open; component mapping for routed prototypes |
| Claude Design | Visual design, portfolio canvas, locked design iterations before code handoff |
| Claude Code | `/design-sync` from `DESIGN.md` to static HTML; eng-adjacent spec work |
| Cursor | Day-to-day design leadership OS, portfolio copy, code-native prototypes in the Firefox tree |
| Firefox tree / mach | Runnable prototypes linked in sprint tickets. Proof bar: Eng can build from it. |
| HTML prototypes | Smart Window states, motion explorations. Local or tree-linked. |

### Agent and skills infrastructure

| Tool | Role in workflow |
|------|------------------|
| [AI Native Knowledge Hub](https://github.com/FirefoxUX/ai-native-knowledge-hub) | Canonical team skills and agents: critique prep, heuristics, design-system procedures |
| PD-OS | Personal design leadership OS: context library, initiative workspace, people memory, CLI + dashboard |
| nova-classic `design-md` | Agent-readable design system spec. Rule: never invent hex when a token exists. |
| [AWDTY scorecard](https://firefoxux.github.io/arewedesigntokensyet/) | Living token dashboard for agents and PMs. NTP propagation 28% to 77.5%. |
| Cursor skills | `nova-classic`, `smart-window-design`, `accessibility`, `prototype-comments` |

### Research and decisions

| Tool | Role in workflow |
|------|------------------|
| UserTesting / AI-moderated research | Tactical decisions (&lt;48h, reversible). Proof bar: signal changed the call. |
| Decision registry | Nova cross-team decisions logged with eng links |
| Punch QA + single backlog | Visual-gap queue: blocker / fix before exposure / accept and track |

### Ops and compounding context

| Tool | Role in workflow |
|------|------------------|
| Claude Co-work to Jira import | Velocity throughput snapshots via `pd_os.cli jira-import` |
| Granola / Zoom `.vtt` | Meeting transcript ingestion to people memory in PD-OS |
| Slack | Async review with `[Mobile+AI · Design]` prefixes; thread to `decisions.md` when settled |
| Jira / Bugzilla | Sprint-linked prototypes, punch findings, ship proof |

### Classic toolkit

Miro · Axure · Adobe Creative Suite · Keynote

---

## Agentic workflows (how the stack connects)

### 1. Design leadership loop (PD-OS)

```
Transcript (.vtt / Granola) → people memory + initiative brief
         ↓
Critique prep agent (hub) → principles check → Slack post skeleton
         ↓
Thread settles → summary → decisions.md
         ↓
Monthly exec proof (5 bullets) → leadership 1:1
```

### 2. Spec and prototype loop (Nova / Smart Window)

```
design-md + token scorecard → agent context
         ↓
Figma spec OR code prototype in Firefox tree
         ↓
Punch QA → single visual-gap backlog
         ↓
Eng ticket / sprint link → ship
```

### 3. Portfolio and stakeholder artifact loop

```
draft/*.md (copy source of truth)
         ↓
Claude Design (visual lock on canvas)
         ↓
Claude Code / Cursor + DESIGN.md → portfolio/site/
```

### 4. Triad gate loop (org-wide)

Anyone can generate with AI. Discipline owners gate. Proof is ship or decision.

| Moment | Who generates | Who gates | Proof |
|--------|---------------|-----------|-------|
| PM concept / proto | PM (+ AI) | Design (intent + craft) | Decision memo + owner |
| Designer PR | Designer (+ AI) | Eng (r? + land) | Landed diff + ticket |
| AI critique / a11y check | Agent | Design accepts/rejects | Logged finding to action |
| Tactical UX call | Research (+ AI-moderated) | Design | Signal changed the decision |

### 5. Team fluency loop (hub to org)

```
Hub skill on main → agent pointed at canonical procedure
         ↓
Designer executes (Cursor / Claude / Figma per tier)
         ↓
Proof bar met → pattern spreads via pillar leads
         ↓
Short-lived branch → PR → merge upstream
```

---

## Proof bars (what counts)

Counts:

- Decision changed because AI surfaced a tradeoff, risk, or missing state
- Prototype linked in eng ticket / sprint planning
- Punch finding closed from single queue before wider exposure
- Fast research signal changed a tactical call

Doesn't count:

- Loom or local HTML with no eng link
- "We ran a test" with no decision change
- Figma labeled "prototype" when Eng needed runnable code
- More Figma files, same shipped outcomes

---

## Teaching: AI-Driven Design (Maven)

[maven.com/bkatalinich/ai-driven-design](https://maven.com/bkatalinich/ai-driven-design/preview/354376) · Co-instructor with Eduardo Feo (Mozilla) · 4.8★

Same AI-native workflows from Firefox, taught to designers, PMs, and innovation leads.

| Module focus | Maps to Mozilla practice |
|--------------|--------------------------|
| AI across the design lifecycle | Velocity mandate · fluency framework |
| Agentic prototyping (tool chains) | Hub skills · Cursor · Claude |
| Figma Make + Loveable for flows/variants | Tactical exploration tier |
| Cursor for functional demos | Code-native stretch · tree prototypes |
| Case study deliverable | Portfolio-ready artifact with decision narrative |

---

## One-liners (pick by audience)

VP / exec: I own Firefox's 2026 platform bets and the operating system that ships them: agents, tokens, triad gates, monthly proof — enabling AI-native builders at scale.

Speaking / teaching: I teach [AI-Driven Design on Maven](https://maven.com/bkatalinich/ai-driven-design/preview/354376). Agentic workflows with proof bars, not tool demos. Same stack I run at Mozilla.

Hiring: Cursor, Claude, hub skills, code in the Firefox tree. Designers initiate. Partners co-create. Everyone builds with AI — discipline owners gate craft.

---

## PD-OS sources (internal depth)

- `data/projects/2026-02-project-nova/`: Nova bets, decisions, token dashboard
- `data/projects/2026-06-ai-velocity-mandate/brief.shareable.md`: operating rules (public)
- `data/projects/2026-07-ai-fluency-framework/`: triad gates, fluency ladder
- `.cursor/skills/smart-window-design/`: Smart Window spec depth
- `portfolio/claude-workflow.md`: Claude Design to Code handoff

Do not use on public site: `brief.md`, Raja 1:1 docs, team tier audit, Jira board IDs, internal OKR numbers.
