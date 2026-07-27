#!/usr/bin/env bash
# Publish vetted shareable velocity docs to branch share/ai-velocity-mandate (managers + ICs).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PD_OS_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
GIT_ROOT="$(cd "$PD_OS_ROOT/../.." && pwd)"
PROJECT_SRC="$PD_OS_ROOT/data/projects/2026-06-ai-velocity-mandate"
SHARE_ROOT="work/pd-os/data/projects/2026-06-ai-velocity-mandate-share"
BRANCH="share/ai-velocity-mandate"
CURRENT_BRANCH=""

cleanup() {
  if [[ -n "$CURRENT_BRANCH" ]]; then
    git -C "$GIT_ROOT" checkout "$CURRENT_BRANCH" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

if [[ ! -d "$PROJECT_SRC" ]]; then
  echo "Project not found: $PROJECT_SRC" >&2
  exit 1
fi

CURRENT_BRANCH="$(git -C "$GIT_ROOT" branch --show-current)"
echo "Syncing share branch → $BRANCH (from $CURRENT_BRANCH)"

# Stage sources on current branch before checkout (share branch lacks main project paths).
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"; cleanup' EXIT

stage_copy() {
  local src_rel="$1"
  local dest_rel="$2"
  local src="$PROJECT_SRC/$src_rel"
  if [[ ! -f "$src" ]]; then
    echo "  skip (missing): $src_rel"
    return 0
  fi
  mkdir -p "$TMP/$(dirname "$dest_rel")"
  cp "$src" "$TMP/$dest_rel"
  echo "  staged $dest_rel"
}

echo "Staging from $PROJECT_SRC..."
stage_copy "drafts/2026-06__team-facing-summary.md" "team/2026-06__team-facing-summary.md"
stage_copy "brief.shareable.md" "team/brief.shareable.md"
stage_copy "drafts/2026-06__velocity-operating-rules.md" "team/2026-06__velocity-operating-rules.md"
stage_copy "drafts/2026-06__raja-velocity-baseline-tldr.md" "managers/2026-06__raja-velocity-baseline-tldr.md"
stage_copy "drafts/2026-06__raja-executive-summary.md" "managers/2026-06__raja-executive-summary.md"
stage_copy "drafts/2026-06__raja-slack-send-ahead.md" "managers/2026-06__raja-slack-send-ahead.md"
stage_copy "SHARE.md" "SHARE.md"
stage_copy "jira.example.json" "jira.example.json"
stage_copy "metrics/README.md" "metrics/README.md"

if git -C "$GIT_ROOT" show-ref --verify --quiet "refs/heads/$BRANCH"; then
  git -C "$GIT_ROOT" checkout "$BRANCH"
else
  git -C "$GIT_ROOT" checkout -b "$BRANCH"
fi

rm -rf "$GIT_ROOT/$SHARE_ROOT"
mkdir -p "$GIT_ROOT/$SHARE_ROOT"
cp -R "$TMP/." "$GIT_ROOT/$SHARE_ROOT/"
echo "Copied staged shareable files into $SHARE_ROOT"

cat > "$GIT_ROOT/$SHARE_ROOT/START-HERE.md" <<EOF
# AI velocity mandate — shareable branch

This branch contains **vetted files only**. Sensitive work (Jira exports, team audit, 1:1 notes) stays on \`main\` and is gitignored.

| Audience | Start here |
|----------|------------|
| **ICs + partners** | [team/2026-06__team-facing-summary.md](team/2026-06__team-facing-summary.md) · [operating rules](team/2026-06__velocity-operating-rules.md) |
| **Managers + Raja** | [managers/2026-06__raja-executive-summary.md](managers/2026-06__raja-executive-summary.md) |

**Related (on \`main\`):**

- Design specs: https://github.com/meerkat-commits/pd-os
- Team skills + agents: 

**Not on this branch:** Co-work Jira prompt, group session agenda, internal \`brief.md\`, metrics data.

Last synced: $(date +%Y-%m-%d)
EOF

# Remove anything else under share root that might linger
find "$GIT_ROOT/$SHARE_ROOT" -type f ! -path "$GIT_ROOT/$SHARE_ROOT/*" 2>/dev/null | true

git -C "$GIT_ROOT" add "$SHARE_ROOT"
if git -C "$GIT_ROOT" diff --cached --quiet; then
  echo "No changes on $BRANCH"
else
  git -C "$GIT_ROOT" commit -m "$(cat <<EOF
Sync shareable AI velocity mandate snapshot.

Team + manager packets only; no Jira data or internal audit artifacts.
EOF
)"
fi

git -C "$GIT_ROOT" checkout "$CURRENT_BRANCH"
trap - EXIT
rm -rf "$TMP"

echo ""
echo "Share branch ready: $BRANCH"
echo "  Link: https://github.com/meerkat-commits/pd-os"
echo "  Push: git push -u origin $BRANCH"
