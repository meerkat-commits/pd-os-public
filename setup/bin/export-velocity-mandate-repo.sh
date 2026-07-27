#!/usr/bin/env bash
# Export vetted AI velocity mandate docs into a standalone repo (no Jira data, audit, or internal brief).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PD_OS_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PROJECT_SRC="$PD_OS_ROOT/data/projects/2026-06-ai-velocity-mandate"
DEST="${1:-$HOME/pd-os-ai-velocity-mandate}"
REPO_SLUG="pd-os-ai-velocity-mandate"

if [[ ! -d "$PROJECT_SRC" ]]; then
  echo "Project not found: $PROJECT_SRC" >&2
  exit 1
fi

echo "Exporting velocity mandate (shareable only) → $DEST"
if [[ -d "$DEST/.git" ]]; then
  find "$DEST" -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
else
  rm -rf "$DEST"
  mkdir -p "$DEST"
fi
mkdir -p "$DEST/team" "$DEST/managers" "$DEST/metrics"

copy() {
  local src_rel="$1" dest_rel="$2"
  local src="$PROJECT_SRC/$src_rel"
  if [[ ! -f "$src" ]]; then
    echo "  skip (missing): $src_rel"
    return 0
  fi
  cp "$src" "$DEST/$dest_rel"
  echo "  + $dest_rel"
}

copy "drafts/2026-06__team-facing-summary.md" "team/2026-06__team-facing-summary.md"
copy "brief.shareable.md" "team/brief.shareable.md"
copy "drafts/2026-06__velocity-operating-rules.md" "team/2026-06__velocity-operating-rules.md"
copy "drafts/2026-06__raja-velocity-baseline-tldr.md" "managers/2026-06__raja-velocity-baseline-tldr.md"
copy "drafts/2026-06__raja-executive-summary.md" "managers/2026-06__raja-executive-summary.md"
copy "drafts/2026-06__raja-slack-send-ahead.md" "managers/2026-06__raja-slack-send-ahead.md"
copy "jira.example.json" "jira.example.json"
copy "metrics/README.md" "metrics/README.md"

# Rewrite links + scrub patterns that should not ship in a standalone repo
if command -v perl >/dev/null 2>&1; then
  find "$DEST" -type f \( -name '*.md' -o -name '*.json' \) -print0 | while IFS= read -r -d '' f; do
    perl -i -pe '
      s/\*?Working detail: \[brief\.md\]\([^)]+\) \(local\)\*?\s*·?\s*//g;
      s/\*Shareable copy: \[on GitHub\]\([^)]+\)\*//g;
      s/Same ~15 designers/Same team/g;
      s|https://github.com/meerkat-commits/pd-os
      s/Velocity proofs \+ this doc/This repo/g;
    ' "$f"
  done
  # Manager doc: generalize named risk row (source file keeps full detail locally)
  MGR="$DEST/managers/2026-06__raja-executive-summary.md"
  if [[ -f "$MGR" ]]; then
    perl -i -0pe 's/\| Anthony \/ mobile.*?named early \|/| Partner velocity narrative | Plan + numbers; situational gaps named early |/s' "$MGR"
  fi
fi

cat > "$DEST/.gitignore" <<'EOF'
.DS_Store
*.swp
metrics/inbox/
metrics/latest.*
metrics/archive/
private/
brief.md
decisions.md
jira.json
EOF

cat > "$DEST/START-HERE.md" <<EOF
# AI velocity mandate

Vetted, shareable docs only. Jira exports, team audit, and internal planning stay in private PD-OS — not in this repo.

| Audience | Start here |
|----------|------------|
| **ICs + partners** | [team/2026-06__team-facing-summary.md](team/2026-06__team-facing-summary.md) |
| **Managers + leadership** | [managers/2026-06__raja-executive-summary.md](managers/2026-06__raja-executive-summary.md) |

**Related tools**

- [design-md](https://github.com/meerkat-commits/pd-os) — Nova + mobile specs
- AI Native Knowledge Hub — team skills + critique/heuristics agents

Exported: $(date +%Y-%m-%d)
EOF

cat > "$DEST/README.md" <<'EOF'
# AI velocity mandate (shareable)

Mobile & AI UX — how we're working faster with AI **without** a new program, extra meetings, or design-as-QC.

This repo is a **standalone export** of vetted docs. Sensitive work (Jira throughput, team audit tiers, 1:1 notes) stays in private PD-OS.

## Start here

See **[START-HERE.md](START-HERE.md)** for audience routing.

| Folder | Who |
|--------|-----|
| [`team/`](team/) | ICs and partners — three bets + tool links |
| [`managers/`](managers/) | Leadership — executive summary + async send-ahead |

## Three bets

1. **Faster calls** — tactical user signal in hours, not weeks  
2. **Code, not slides** — eng-ready prototypes in the Firefox tree  
3. **Close the loop** — lightweight Nova build review; paper cuts post-Nightly  

## Regenerate

From your PD-OS checkout:

```bash
./setup/bin/export-velocity-mandate-repo.sh ~/pd-os-ai-velocity-mandate
cd ~/pd-os-ai-velocity-mandate
git add -A && git commit -m "Sync from PD-OS" && git push
```

## License

Internal Mozilla design ops — private repo; adjust before wider release if needed.
EOF

WARN=0
if grep -r -E 'FXAI-[0-9]{3,}|bkatalinich@|coaching target|brief\.md \(local\)' "$DEST" \
  --exclude-dir=.git 2>/dev/null | grep -q .; then
  echo "WARNING: possible sensitive patterns remain:"
  grep -r -n -E 'FXAI-[0-9]{3,}|bkatalinich@|coaching target|brief\.md \(local\)' "$DEST" \
    --exclude-dir=.git 2>/dev/null || true
  WARN=1
fi
if find "$DEST" \( -name 'latest.json' -o -name 'latest.md' \) ! -path '*/.git/*' 2>/dev/null | grep -q .; then
  echo "WARNING: metrics data in export"
  WARN=1
fi

if [[ ! -d "$DEST/.git" ]]; then
  git -C "$DEST" init -b main
  echo "  git init → $DEST"
fi

echo ""
if [[ "$WARN" -eq 1 ]]; then
  echo "Review warnings before pushing."
  exit 1
fi

echo "Standalone velocity repo ready: $DEST"
echo ""
echo "Next steps:"
echo "  cd $DEST"
echo "  git add -A && git commit -m \"Initial export of shareable AI velocity mandate\""
echo "  gh repo create $REPO_SLUG --private --source=. --remote=origin --push"
