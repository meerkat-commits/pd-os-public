# Open items — PD-OS

Checklist for **bootstrapping**, **data layout**, **transcripts → people**, **templates/skills**, and **hooks to Mobile + AI review**. Workspace-wide lists: [`../../OPEN_ITEMS.md`](../../OPEN_ITEMS.md). Review playbook: [`../../design/design-review-workflow/README.md`](../../design/design-review-workflow/README.md).

---

## Environment & CLI

- [ ] **`python3 -m venv .venv`** + **`pip install -r requirements.txt`** on each machine (see [`setup/README.md`](setup/README.md))
- [ ] Confirm **`python3 -m pd_os.cli --help`** (or `ingest-latest --help`) runs with venv activated
- [ ] Optional: alias **`ingest-latest`** in shell profile for your preferred **`--meeting-title`** default

## `data/` layout

- [ ] Create **`data/inbox/transcripts/`** and at least one **`data/projects/<initiative>/`** skeleton (`brief.md`, `research/`, `drafts/`, `decisions.md`)
- [ ] Agree naming convention for initiatives (date prefix vs Jira key slug)
- [ ] Decide **Git policy** for **`data/people/`** (ignore for PII, commit redacted stubs only, or private fork—match your org)

## Transcripts & people compounding

- [ ] Run one **`ingest-transcript`** or **`ingest-latest`** end-to-end from a real `.vtt` / text file
- [ ] Spot-check **`data/people/*.md`** for tone, PII, and wrong attributions; adjust heuristics or process if needed
- [ ] Optional: spike **LLM-backed extractor** mode (README **Notes**) if heuristic summaries are too thin

## Context library & templates

- [ ] Review **`context-library/`** (product, stakeholders, Firefox voice) against current org reality
- [ ] Copy **`templates/design_brief.md`** / **`critique_notes.md`** into a live project and trim placeholders
- [ ] Align **`templates/`** with one **[Mobile+AI · …]** phase in [design-review-workflow](../../design/design-review-workflow/README.md) as a pilot

## Skills & sub-agents

- [x] Team skills moved to **[ai-native-knowledge-hub](https://github.com/FirefoxUX/ai-native-knowledge-hub)**; PD-OS keeps `meeting_ingest` and `smart_window_design` only
- [ ] Update **`CLAUDE.md`** if default priorities (critique vs vision vs ingest) change

## Async design review + Heuristics linkage

- [ ] After a **`#mobile_x_ai`** thread closes, paste **Slack permalink** + outcome into the initiative **`decisions.md`** or **`drafts/`**
- [ ] Confirm teammates know **Heuristics** telemetry can post to **`#mobile_x_ai`** (see **`design/heuristics-plugin`** [OPEN_ITEMS](../../design/heuristics-plugin/OPEN_ITEMS.md))

## Parking lot

- [ ] _CLI wrapper for “append last Slack review URL” (local convention)_
- [ ] _Other PD-OS improvements_
