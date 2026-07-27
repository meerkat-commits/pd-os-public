#!/usr/bin/env bash
# Export a team-safe critique-prep slice (no people memory, digests, or calibration).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DEST="${1:-$HOME/Desktop/critique-prep-$(date +%Y%m%d)}"
HUB_URL=""

echo "Exporting critique slice → $DEST"
mkdir -p "$DEST"

RSYNC=(rsync -a
  --exclude '.git/'
  --exclude '.venv/'
  --exclude '__pycache__/'
)

copy() {
  local src="$1" dst="$2"
  mkdir -p "$(dirname "$DEST/$dst")"
  if [[ -e "$REPO_ROOT/$src" ]]; then
    cp -R "$REPO_ROOT/$src" "$DEST/$dst"
  fi
}

"${RSYNC[@]}" "$REPO_ROOT/pd_os/" "$DEST/pd_os/"
copy requirements.txt requirements.txt
copy setup/agents/critique-prep.md setup/agents/critique-prep.md
copy context-library/process/critique-prep.md context-library/process/critique-prep.md
copy context-library/process/mobile_ai_design_review_workflow.md context-library/process/mobile_ai_design_review_workflow.md
copy context-library/product-and-design.md context-library/product-and-design.md
copy templates/critique_notes.md templates/critique_notes.md

mkdir -p "$DEST/data/drafts/critique-prep"

cat > "$DEST/README.md" <<EOF
# Critique prep (team slice)

Standalone UI for Mobile & AI design critique — no full PD-OS required.

Team skills and procedures: **[$HUB_URL]($HUB_URL)** (clone alongside this folder as \`../ai-native-knowledge-hub/\`).

## Run

\`\`\`bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 -m pd_os.cli critique-dashboard --open
\`\`\`

Opens **http://127.0.0.1:8767** — prep form, principles, workflow, agent prompt.

## Cursor

After generating a prompt in the UI, paste in Cursor with \`@setup/agents/critique-prep.md\` (routes to the knowledge hub + local Mobile+AI workflow).

## Files

- \`setup/agents/critique-prep.md\` — hub router + PD-OS workflow context
- \`context-library/process/critique-prep.md\` — principles
- \`templates/critique_notes.md\` — capture outcomes after review
EOF

echo ""
echo "Critique slice ready: $DEST"
echo "  python3 -m pd_os.cli critique-dashboard --open"
