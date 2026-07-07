#!/usr/bin/env bash
# Manager-safe export: AI velocity mandate (no Jira data, no team audit, no political notes).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PROJECT="2026-06-ai-velocity-mandate"
SRC="$REPO_ROOT/data/projects/$PROJECT"
DEST="${1:-$HOME/Desktop/ai-velocity-mandate-shareable-$(date +%Y%m%d)}"

if [[ ! -d "$SRC" ]]; then
  echo "Project not found: $SRC" >&2
  exit 1
fi

echo "Exporting manager packet → $DEST"
mkdir -p "$DEST"

copy() {
  local rel="$1"
  if [[ -f "$SRC/$rel" ]]; then
    mkdir -p "$DEST/$(dirname "$rel")"
    cp "$SRC/$rel" "$DEST/$rel"
  fi
}

# Safe artifacts only
copy "SHARE.md"
copy "README.md"
copy "brief.shareable.md"
copy "jira.example.json"
copy "metrics/README.md"
copy "drafts/2026-06__raja-executive-summary.md"
copy "drafts/2026-06__raja-slack-send-ahead.md"
copy "drafts/2026-06__group-session-agenda.md"

WARN=0
if find "$DEST" -name '*.json' ! -name 'jira.example.json' 2>/dev/null | grep -q .; then
  echo "WARNING: unexpected JSON in export"
  WARN=1
fi
if grep -r -E 'FXAI-[0-9]{3,}|bkatalinich@|Anthony Keen|coaching target' "$DEST" 2>/dev/null | grep -q .; then
  echo "WARNING: possible sensitive patterns in export:"
  grep -r -n -E 'FXAI-[0-9]{3,}|bkatalinich@|Anthony Keen|coaching target' "$DEST" 2>/dev/null || true
  WARN=1
fi
if [[ -d "$DEST/metrics/inbox" ]] || [[ -f "$DEST/metrics/latest.json" ]]; then
  echo "WARNING: metrics data leaked into export"
  WARN=1
fi

cat > "$DEST/START-HERE.md" <<EOF
# AI velocity mandate — manager packet

Read first: \`drafts/2026-06__raja-executive-summary.md\`

Supporting: \`brief.shareable.md\`, \`SHARE.md\`

Exported: $(date +%Y-%m-%d)
EOF

echo ""
echo "Manager packet ready: $DEST"
echo "  START-HERE.md → executive summary"
if [[ "$WARN" -eq 1 ]]; then
  echo "Review warnings above before sending."
  exit 1
fi
echo "No obvious sensitive patterns detected."
