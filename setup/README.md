# Setup

## First-time checklist

```bash
cd pd-os
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Zoom transcripts workflow (locked-down sharing)

Since transcripts/recordings may only be accessible to the meeting owner in a locked-down Zoom setup, this repo supports a **manual + fast** workflow:

1. Download a Zoom transcript (`.vtt`) you have access to
2. Put it in `~/Downloads` (or any folder you choose)
3. Run:

```bash
python3 -m pd_os.cli ingest-latest --meeting-title "Weekly Sync" --move-processed
```

If you prefer, you can ingest a specific file:

```bash
python3 -m pd_os.cli ingest-transcript "/full/path/to/transcript.vtt" --meeting-title "Weekly Sync"
```

## Scheduled automations (daily + weekly)

Granola sync + digest/rollup on a schedule via **launchd**. See **[`launchd/README.md`](launchd/README.md)**.

Quick start:

```bash
./setup/launchd/install.sh
# Edit ~/.config/pd-os/env with your grn_ API key
./setup/bin/run-daily.sh   # test
```

Optional **Cursor agent** prompts: [`agents/daily.md`](agents/daily.md), [`agents/weekly.md`](agents/weekly.md), [`agents/stakeholder-draft.md`](agents/stakeholder-draft.md), **[`agents/critique-prep.md`](agents/critique-prep.md)** (team — before design review), **[`agents/heuristics-review.md`](agents/heuristics-review.md)** (team — Nielsen / Acorn / DAU heuristic pass; plugin parity).

**Web UI** (artifacts, agents, critique prep form, changelog):

```bash
python3 -m pd_os.cli dashboard --open
```

Team ICs: **Agents** tab → **Critique prep** → fill form → copy Cursor prompt → paste in Cursor with `@setup/agents/critique-prep.md`.

**Critique-only slice** (share with designers — no full PD-OS):

```bash
python3 -m pd_os.cli critique-dashboard --open   # http://127.0.0.1:8767
./setup/bin/export-critique-slice.sh             # zip-friendly folder for team
```

## PD-OS ↔ AI Native Knowledge Hub

Team skills and agents live in **[FirefoxUX/ai-native-knowledge-hub](https://github.com/FirefoxUX/ai-native-knowledge-hub)** — not a personal export repo.

**Local clone** (sibling to pd-os):

```bash
# First time (if missing):
git clone https://github.com/FirefoxUX/ai-native-knowledge-hub.git ../ai-native-knowledge-hub

# Refresh main when consuming team skills:
git -C ../ai-native-knowledge-hub fetch origin
git -C ../ai-native-knowledge-hub checkout main && git -C ../ai-native-knowledge-hub pull
```

Clone path: `~/VibeCoding_BK/work/ai-native-knowledge-hub/` (alongside pd-os).

Open both folders in a Cursor multi-root workspace, or `@`-mention hub files from the sibling path.

| Layer | Where | Branch |
|-------|-------|--------|
| Team skills + agents | `../ai-native-knowledge-hub/` | `main` to consume; short-lived branch + PR to contribute |
| Personal OS (people, projects, transcripts) | this repo (`pd-os`) | your normal workflow |
| Local-only experiments | `~/.cursor/skills/` or pd-os | no hub branch needed |

**What stays in PD-OS:** `data/people/`, initiative artifacts, digests, calibration, velocity audit, stakeholder-specific drafts.

**What goes to the hub (via PR):** reusable critique/heuristics skills, templates, and team context that any Firefox UX discipline can use.

**Diff before contributing:** `./setup/bin/export-agents-repo.sh ~/pd-os-agents-export` then compare against the hub.

## Calibration (local only — not in GitHub)

Performance review calibration (`data/projects/*-performance-review-calibration/`, `pd_os/calibration.py`, calibration agents, launchd reminders) stays **on your machine only** — excluded via `.gitignore`. Keep using it locally; do not commit or push those paths.

### Workflow commands

```bash
python3 -m pd_os.cli commitments-digest --time-range last_24h
python3 -m pd_os.cli project-hygiene --stale-days 14
python3 -m pd_os.cli stakeholder-draft --person "Example Stakeholder"
python3 -m pd_os.cli stakeholder-drafts --time-range last_24h
python3 -m pd_os.cli run-daily --stakeholder-drafts   # all-in-one + draft contexts
```

### Jira velocity sync (Mobile & AI mandate)

See **`data/projects/2026-06-ai-velocity-mandate/SHARE.md`** for GitHub safety.

**Manager packet:**

```bash
./setup/bin/export-velocity-mandate-shareable.sh
```

**Co-work import** (local metrics — not committed):

```bash
python3 -m pd_os.cli jira-import
```

Optional API: add `JIRA_EMAIL` + `JIRA_API_TOKEN` to `~/.config/pd-os/env`, then `jira-sync`.

### Dashboard (local web UI)

Browse digests, commitments, hygiene reports, rollups, and stakeholder drafts in the browser:

```bash
python3 -m pd_os.cli dashboard --open
# or
./setup/bin/open-dashboard.sh
```

Opens **http://127.0.0.1:8765/** — sidebar navigation, rendered markdown, Refresh button.

## Shareable export (no personal data)

Scrubbed copy for zip / handoff — excludes `data/people/`, meeting notes, ratings, calibration packets:

```bash
./setup/bin/export-pd-os-shareable.sh
# → ~/Desktop/pd-os-shareable-YYYYMMDD/
```

Details: see local `data/projects/2026-06-performance-review-calibration/SHARE.md` (gitignored).

