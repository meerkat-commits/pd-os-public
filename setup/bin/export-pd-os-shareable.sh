#!/usr/bin/env bash
# Create a scrubbed copy of pd-os safe to zip or share (no ratings, meeting notes, or people memory).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DEST="${1:-$HOME/Desktop/pd-os-shareable-$(date +%Y%m%d)}"

CALIBRATION='2026-06-performance-review-calibration'
VELOCITY='2026-06-ai-velocity-mandate'

echo "Exporting shareable pd-os → $DEST"
mkdir -p "$DEST"

RSYNC=(rsync -a --delete --delete-excluded
  --exclude '.git/'
  --exclude '.venv/'
  --exclude '__pycache__/'
  --exclude '.pytest_cache/'
  --exclude 'data/people/'
  --exclude 'data/inbox/'
  --exclude 'data/digests/'
  --exclude 'data/rollups/'
  --exclude 'data/drafts/'
  --exclude 'data/knowledge/'
  --exclude "data/projects/${CALIBRATION}/private/"
  --exclude "data/projects/${CALIBRATION}/decisions.md"
  --exclude "data/projects/${CALIBRATION}/sources.md"
  --exclude "data/projects/${VELOCITY}/metrics/"
  --exclude "data/projects/${VELOCITY}/decisions.md"
  --exclude "data/projects/${VELOCITY}/brief.md"
  --exclude "data/projects/${VELOCITY}/jira.json"
  --exclude "data/projects/${VELOCITY}/private/"
  --exclude "data/projects/${VELOCITY}/drafts/2026-06__raja-1on1-talking-points.md"
  --exclude "data/projects/${VELOCITY}/drafts/2026-06__velocity-survey.md"
  --exclude "data/projects/${VELOCITY}/drafts/2026-06__monthly-dashboard-template.md"
  --exclude "data/projects/${VELOCITY}/drafts/2026-06__claude-cowork-jira-prompt.md"
  --exclude "data/projects/${VELOCITY}/drafts/2026-06__group-session-agenda.md"
  --exclude "data/projects/${VELOCITY}/drafts/2026-06__raja-velocity-baseline-tldr.md"
  --exclude "data/projects/${VELOCITY}/drafts/2026-06__raja-slack-send-ahead.md"
  --exclude "data/projects/${VELOCITY}/drafts/2026-06__raja-reorg-velocity-sync.md"
  --exclude "data/projects/2026-06-nova-podcast/"
  --exclude "data/projects/2026-06-nova-nightly-screenshots/captures/"
  --exclude "data/projects/2026-06-nova-nightly-screenshots/.profiles/"
  --exclude "data/projects/2026-06-nova-nightly-screenshots/.state/"
  --exclude "pd_os/calibration.py"
  --exclude "setup/agents/calibration.md"
  --exclude "setup/agents/calibration-ic.md"
  --exclude "setup/bin/calibration-reminders.sh"
  --exclude "setup/bin/calibration-reminders-pm.sh"
  --exclude "setup/launchd/com.pd-os.calibration-reminders.plist"
  --exclude "setup/launchd/com.pd-os.calibration-reminders-pm.plist"
  --exclude "setup/launchd/install-calibration-reminders.sh"
  --exclude "setup/launchd/uninstall-calibration-reminders.sh"
  --exclude '*performance-summary*'
  --exclude '*calibration-session*'
  --exclude '*calibration-summaries*'
  --exclude '*calibration-promotions*'
  --exclude '*calibration-signals*'
  --exclude '*calibration-packet*'
  --exclude '*calibration-run*'
  --exclude '*calibration__*'
  --exclude '*external-ICs*'
  --exclude '*position-shifts*'
  --exclude '2026-06-02__*'
  --exclude '2026-06-09__*'
  --exclude 'EXPORT-google-doc.md'
  --exclude 'portfolio/.public-export/'
  --exclude 'portfolio/.github-publish/'
  --exclude 'portfolio/.fig-extract/'
)

"${RSYNC[@]}" "$REPO_ROOT/" "$DEST/"

# Ensure shareable stub exists in export (real sources.md is excluded)
if [[ -f "$REPO_ROOT/data/projects/${CALIBRATION}/sources.example.md" ]]; then
  cp "$REPO_ROOT/data/projects/${CALIBRATION}/sources.example.md" \
    "$DEST/data/projects/${CALIBRATION}/sources.example.md"
fi

# Quick scan for common leakage patterns
WARN=0
if grep -r -l -E 'Mostly [Mm]eets|Greatly [Ee]xceeds|promotion not supported' \
  "$DEST/data/projects/${CALIBRATION}/drafts" 2>/dev/null | grep -q .; then
  echo "WARNING: possible rating language still in calibration drafts:"
  grep -r -l -E 'Mostly [Mm]eets|Greatly [Ee]xceeds|promotion not supported' \
    "$DEST/data/projects/${CALIBRATION}/drafts" 2>/dev/null || true
  WARN=1
fi
if [[ -d "$DEST/data/people" ]] || [[ -d "$DEST/data/inbox" ]]; then
  echo "WARNING: data/people or data/inbox present in export"
  WARN=1
fi
if find "$DEST" -path '*/private/granola-api/*.json' 2>/dev/null | grep -q .; then
  echo "WARNING: Granola JSON found in export"
  WARN=1
fi
if grep -r -l -E 'assignee|mozilla-hub\.atlassian\.net/jira' \
  "$DEST/data/projects/${VELOCITY}" 2>/dev/null \
  | grep -v -E 'SHARE\.md|jira\.example\.json' | grep -q .; then
  echo "WARNING: possible Jira/assignee leakage in velocity mandate:"
  grep -r -l -E 'assignee|mozilla-hub\.atlassian\.net/jira' \
    "$DEST/data/projects/${VELOCITY}" 2>/dev/null \
    | grep -v -E 'SHARE\.md|jira\.example\.json' || true
  WARN=1
fi

cat > "$DEST/SHARE.md" <<'EOF'
# PD-OS — shareable concept export

This folder is a **scrubbed snapshot** for showing how a design-lead operating system works — not a live personal instance.

## What's included

- Repo layout: `context-library/`, `data/projects/`, `templates/`, `setup/`, Python CLI (`pd_os/`)
- Example initiatives (Nova decisions, mobile DAU brief, velocity shareable docs)
- Team workflow pointers → [AI Native Knowledge Hub](https://github.com/FirefoxUX/ai-native-knowledge-hub)

## What's excluded (stays on the owner's machine)

- `data/people/` — transcript-derived people memory
- `data/inbox/`, digests, rollups — raw inputs and daily automation
- Velocity Jira metrics, internal briefs, manager-only drafts
- Performance review calibration
- Podcast prep and Nightly screenshot captures

## Quick start (recipient)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 -m pd_os.cli dashboard --open
```

Regenerate this export from a full PD-OS checkout:

```bash
./setup/bin/export-pd-os-shareable.sh
```
EOF

echo ""
echo "Shareable export ready: $DEST"
echo "Included from calibration: research/, scope docs, low-risk-code one-pager, SHARE.md, sources.example.md"
echo "Included from velocity mandate: executive summary, brief.shareable.md, SHARE.md"
if [[ "$WARN" -eq 1 ]]; then
  echo "Review warnings above before sharing."
  exit 1
fi
echo "No obvious sensitive patterns detected."
