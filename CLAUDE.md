# PD-OS — Claude Context

This file is the **master context** for this repository.

## What this repo is

PD-OS is a lightweight **Product Design leader operating system**, inspired by the repo-style structure described in Aakash Gupta’s PM-OS article (`https://www.news.aakashg.com/p/pm-os`).

It provides:
- a **context library** (`context-library/`) for stable, reusable info
- a **design initiatives workspace** (`data/projects/`) for accumulating artifacts
- a **people memory** (`data/people/`) that compounds from meeting transcripts
- a small local CLI (`python3 -m pd_os.cli ...`) to ingest transcripts (including Zoom `.vtt`)

## How to use context

Prefer pulling the minimum required context:
- For stakeholder messages: start with `context-library/stakeholders.md`, then relevant `data/people/<Name>.md`, then the initiative’s latest `drafts/`.
- For an initiative: start with `data/projects/<initiative>/brief.md` + `decisions.md` + latest drafts + any `research/` synthesis.
- For **Nova desktop UI** (chrome, NTP, settings): read `context-library/design-md/nova-classic/DESIGN.md` and follow Cursor skill **`nova-classic`** (`~/.cursor/skills/nova-classic/SKILL.md`).
- For **team skills + agents** (critique prep, heuristics, design system, voice): start at [`../ai-native-knowledge-hub/`](../ai-native-knowledge-hub/) — canonical FirefoxUX/ai-native-knowledge-hub. Read `AGENTS.md` → discipline index → matching skill file. Do not invent Firefox UI or brand rules; flag uncertainty.

## PD-OS ↔ AI Native Knowledge Hub

| Keep in **PD-OS** | Keep in **knowledge hub** |
|-------------------|---------------------------|
| `data/people/`, initiative `brief.md` / `decisions.md` / drafts | Reusable skills, agents, templates, team memory |
| Transcripts, digests, calibration, velocity audit | Critique prep, heuristics, design-system procedures |
| Stakeholder-specific framing | Cross-discipline procedures the whole UX org can use |

**Day-to-day:** point agents at the hub (`main`). **Contributing:** short-lived branch in the hub → PR → merge. Do not maintain a long-lived personal fork — that recreates the old `pd-os-agents` drift problem.

Local clone (sibling to this repo): `../ai-native-knowledge-hub/`

## Design-leadership priorities

- **Narrative over artifacts**: optimize for shared understanding and decision quality, not deliverables volume.
- **Decision hygiene**: capture what was decided, why, trade-offs, and what would change the decision.
- **Critique as a system**: hub design skills + `setup/agents/critique-prep.md` (routes to [ai-native-knowledge-hub](../ai-native-knowledge-hub/)); PD-OS principles: `context-library/process/critique-prep.md`.
- **Stakeholder-aware communication**: tailor framing per person (use `data/people/`).

## Repo conventions

- **Don’t overwrite history** in `data/people/`: append new meeting entries.
- **Keep artifacts close to the work**: put drafts/research under the relevant project folder.
- **Name projects with date prefixes**: `YYYY-MM-<slug>` to keep a chronological archive.

