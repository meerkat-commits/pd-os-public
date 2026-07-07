# How I work

## Headline

I build systems so design teams compound instead of resetting every quarter. Agentic workflows, proof bars, and an AI-native tool stack.

Most design leaders describe operating models. I ship them: in PD-OS locally, upstream in the [team skills hub](https://github.com/FirefoxUX/ai-native-knowledge-hub), on Firefox's 2026 bets in production, and in [AI-Driven Design on Maven](https://maven.com/bkatalinich/ai-driven-design/preview/354376) with Eduardo Feo.

Full tool stack and Firefox bets: [`ai-native.md`](ai-native.md)

---

## Firefox bets I own

| Bet | Scope | Status |
|-----|-------|--------|
| Project Nova | Full-browser redesign: chrome, NTP, onboarding, settings | In Nightly · decision registry · community-in-thread |
| Smart Window | Opt-in AI: Private, Classic, Smart Window; agentic in-window task completion | Program gates · 100% AI Window tokenized |
| AI-native org transformation | Operating system for 35-person hybrid org | 2026 H2 mandate |

Three pillars: Agentic (Smart Window, shake-to-summarize), Habit Loops (NTP, tab groups, vertical tabs), Localization (global community feedback).

Exec partnership: PLG and monetization with Product, Engineering, Data, and Marketing.

---

## AI-native tool stack

### Design to ship

| Layer | Tools |
|-------|-------|
| Spec and align | Figma · nova-classic `design-md` · AWDTY token scorecard |
| Prototype | Cursor · code in Firefox tree · Claude Design for visual lock |
| Handoff | Sprint/ticket-linked artifacts |
| QA | Punch QA · single visual-gap backlog |

### Agents and skills

| Layer | Tools |
|-------|-------|
| Team (canonical) | [AI Native Knowledge Hub](https://github.com/FirefoxUX/ai-native-knowledge-hub) |
| Leadership (local) | PD-OS: context library, initiative workspace, people memory, CLI dashboard |
| Routed skills | `nova-classic` · `smart-window-design` · `accessibility` · `prototype-comments` |

### Decisions and velocity

| Layer | Tools |
|-------|-------|
| Fast calls | UserTesting / AI-moderated research |
| Throughput | Claude Co-work to Jira import · `pd_os.cli` snapshots |
| Context | Granola / Zoom `.vtt` · Slack to `decisions.md` |

---

## Agentic workflows

### Critique to decision

1. Before posting: critique prep agent (hub) + principles doc
2. Post: Slack with `[Mobile+AI · Design]` prefix + validation gates
3. After thread settles: link + summary to `decisions.md` or initiative draft

### Spec to ship (Nova / Smart Window)

1. Agent context: `design-md` + token scorecard
2. Figma spec or runnable prototype in Firefox tree
3. Punch QA, single backlog, eng ticket, Nightly

### Anyone generates, discipline gates

AI accelerates thinking, making, and review. Design gates craft and intent. Eng gates merge and release. PM gates scope and success criteria. The bar is what ships and what users feel — enabled by hub skills, context, and code in the tree.

### Hub to org spread

Point agents at hub (`main`). Designer executes. Proof bar met. Pillar lead coaches. PR upstream. No personal fork drift.

---

## PD-OS (Product Design Operating System)

Inspired by [PM-OS](https://www.news.aakashg.com/p/pm-os). Lightweight design leadership OS:

- Context library: stable product, stakeholder, and process context
- Initiative workspace: `brief.md`, `decisions.md`, drafts per project
- People memory: transcript ingestion to compounding per-person briefs
- Agents: critique prep, calibration reminders, daily/weekly workflows
- Dashboard: local UI for digests, critique prep form, changelog

```bash
python3 -m pd_os.cli dashboard --open
```

Share publicly: architecture overview, critique prep flow, CLI demo.  
Keep private: calibration ratings, people reports, gitignored `data/people/`.

---

## Nova token scorecard

Living [AWDTY](https://firefoxux.github.io/arewedesigntokensyet/) dashboard for agents and PMs:

- Propagation history (NTP: 28% to 77.5%)
- Surface health by chrome area
- Agent rules: never invent hex when a token exists

Refresh: `data/projects/2026-02-project-nova/scripts/nova-token-scorecard.py`

---

## Writing defaults

From `context-library/writing-style.md`:

- Lead with a 1 to 2 sentence TL;DR
- Then 3 to 6 bullets: decision, rationale, trade-offs, next steps
- Tone: direct, calm, specific

---

## Close

I optimize for enabling AI-native builders at scale — compounding context, shared skills, and proof that shows up in product.
