#!/usr/bin/env bash
# Local export of team-safe PD-OS agents + Cursor skills (for testing or diffing).
# Canonical team repo: 
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PD_OS_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
WORKSPACE_ROOT="$(cd "$PD_OS_ROOT/../.." && pwd)"
HEURISTICS_SKILLS="$WORKSPACE_ROOT/design/heuristics-plugin/.cursor/skills"
HUMANIZER_SKILL="${HUMANIZER_SKILL:-$HOME/.cursor/skills/humanizer}"
PROTOTYPE_COMMENTS_SKILL="${PROTOTYPE_COMMENTS_SKILL:-$HOME/.cursor/skills/prototype-comments}"
# Skills excluded from team export (local-only or manager scope)
EXPORT_SKIP_SKILLS="firefox-mobile-dau smart-window-design"
DEST="${1:-$HOME/pd-os-agents-export}"

echo "Exporting agents + skills → $DEST"
mkdir -p "$DEST"

copy() {
  local src="$1" dst="$2"
  if [[ ! -e "$src" ]]; then
    echo "  skip (missing): $src"
    return 0
  fi
  mkdir -p "$(dirname "$DEST/$dst")"
  cp -R "$src" "$DEST/$dst"
  echo "  + $dst"
}

# --- Agents (team + reusable) ---
copy "$PD_OS_ROOT/setup/agents/critique-prep.md" "setup/agents/critique-prep.md"
copy "$PD_OS_ROOT/setup/agents/heuristics-review.md" "setup/agents/heuristics-review.md"

# --- Cursor skill routers (.claude/skills in PD-OS — local only; team skills in hub) ---
for skill in meeting_ingest smart_window_design; do
  copy "$PD_OS_ROOT/.claude/skills/${skill}.md" ".claude/skills/${skill}.md"
done

# --- Context + templates ---
copy "$PD_OS_ROOT/context-library/process/critique-prep.md" "context-library/process/critique-prep.md"
copy "$PD_OS_ROOT/context-library/process/mobile_ai_design_review_workflow.md" "context-library/process/mobile_ai_design_review_workflow.md"
copy "$PD_OS_ROOT/context-library/product-and-design.md" "context-library/product-and-design.md"
copy "$PD_OS_ROOT/context-library/writing-style.md" "context-library/writing-style.md"
copy "$PD_OS_ROOT/context-library/stakeholders.md" "context-library/stakeholders.md"
copy "$PD_OS_ROOT/context-library/brands/firefox_voice.md" "context-library/brands/firefox_voice.md"
copy "$PD_OS_ROOT/context-library/design-md/nova-classic/DESIGN.md" "context-library/design-md/nova-classic/DESIGN.md"
copy "$PD_OS_ROOT/context-library/design-md/nova-classic/README.md" "context-library/design-md/nova-classic/README.md"
copy "$PD_OS_ROOT/context-library/design-md/firefox-mobile-android/DESIGN.md" "context-library/design-md/firefox-mobile-android/DESIGN.md"
copy "$PD_OS_ROOT/context-library/design-md/firefox-mobile-android/README.md" "context-library/design-md/firefox-mobile-android/README.md"

copy "$PD_OS_ROOT/templates/critique_notes.md" "templates/critique_notes.md"
copy "$PD_OS_ROOT/templates/design_brief.md" "templates/design_brief.md"
copy "$PD_OS_ROOT/templates/vision_onepager.md" "templates/vision_onepager.md"
copy "$PD_OS_ROOT/templates/strategy_narrative.md" "templates/strategy_narrative.md"

sync_skill() {
  local src="$1" rel_dst="$2"
  if [[ ! -d "$src" ]]; then
    echo "  skip (missing): $src"
    return 0
  fi
  mkdir -p "$(dirname "$DEST/$rel_dst")"
  rsync -a --delete "${src}/" "$DEST/$rel_dst/"
  echo "  + $rel_dst/"
}

# --- Heuristics plugin skills (bundled for standalone use) ---
if [[ -d "$HEURISTICS_SKILLS" ]]; then
  mkdir -p "$DEST/.cursor/skills"
  for d in "$HEURISTICS_SKILLS"/*/; do
    [[ -d "$d" ]] || continue
    name="$(basename "$d")"
    if [[ " $EXPORT_SKIP_SKILLS " == *" $name "* ]]; then
      echo "  skip (export): $name"
      continue
    fi
    sync_skill "$d" ".cursor/skills/$name"
  done
else
  echo "WARNING: heuristics skills not found at $HEURISTICS_SKILLS"
fi

# --- Humanizer skill (full Cursor skill) ---
sync_skill "$HUMANIZER_SKILL" ".cursor/skills/humanizer"

# --- Prototype comments skill ---
sync_skill "$PROTOTYPE_COMMENTS_SKILL" ".cursor/skills/prototype-comments"

# --- Path rewrites: monorepo → this repo ---
if command -v perl >/dev/null 2>&1; then
  find "$DEST" -type f \( -name '*.md' -o -name 'SKILL.md' \) -print0 | while IFS= read -r -d '' f; do
    perl -i -pe '
      s|design/heuristics-plugin/\.cursor/skills/|\.cursor/skills/|g;
      s|\.\./\.\./design/heuristics-plugin/\.cursor/skills/|\.cursor/skills/|g;
      s|\s*\(from PD-OS: `[^`]+`\)\s*||g;
      s|\*\*Figma plugin:\*\* `design/heuristics-plugin/` —|\*\*Figma plugin (separate repo):\*\*|g;
      s|Heuristics Figma plugin \(`design/heuristics-plugin/`\)|Heuristics Figma plugin|g;
      s|design/heuristics-plugin/README\.md|Heuristics Figma plugin README \(separate repo\)|g;
    ' "$f"
  done
  find "$DEST" -type f \( -name '*.md' -o -name 'SKILL.md' \) -print0 | while IFS= read -r -d '' f; do
    perl -i -pe 's/^\s*\(\)\s*$//g' "$f"
  done
fi

cat > "$DEST/.gitignore" <<'EOF'
.DS_Store
*.swp
EOF

cat > "$DEST/AGENTS.md" <<'EOF'
# Agents index (local export)

> Canonical team index: FirefoxUX/ai-native-knowledge-hub

| Agent | Path | Notes |
|-------|------|-------|
| Critique prep | `setup/agents/critique-prep.md` | Routes to hub + PD-OS Mobile+AI workflow |
| Heuristics review | `setup/agents/heuristics-review.md` | Routes to hub design skills |

## PD-OS local skills (`.claude/skills/`)

| Skill | Path |
|-------|------|
| Meeting ingest | `.claude/skills/meeting_ingest.md` |
| Smart Window design | `.claude/skills/smart_window_design.md` |
EOF

cat > "$DEST/README.md" <<'EOF'
# PD-OS design agents & skills (local export)

> **Canonical team repo:** FirefoxUX/ai-native-knowledge-hub — use that for shared skills and agents. This folder is a local export from PD-OS for testing or diffing only.

Team-safe **Cursor agents**, **skill routers**, and **process docs** for design critique and heuristic review.

## What's included

- **Agents** — `setup/agents/` (hub routers for critique + heuristics)
- **Local skills** — `.claude/skills/` (meeting ingest, Smart Window only)
- **Principles & workflow** — `context-library/process/`
- **Templates** — `templates/` (critique notes, briefs, vision docs)

See **[AGENTS.md](AGENTS.md)** and the knowledge hub for team skills.

## Use in Cursor

1. Clone this repo anywhere on your machine.
2. Open the folder in Cursor (or add it to a multi-root workspace alongside your design files).
3. In chat, `@`-mention agents and context, e.g.:
   - `@setup/agents/critique-prep.md`
   - `@context-library/process/critique-prep.md`
   - `@.cursor/skills/heuristics-review-bundle/SKILL.md`

### Optional: install heuristics skills globally

Symlink bundled skills into your user skills folder so Cursor picks them up in any project:

```bash
for d in .cursor/skills/*/; do
  name="$(basename "$d")"
  ln -sf "$(pwd)/$d" "$HOME/.cursor/skills/$name"
done
```

## Typical flows

**Before async design review**

1. Optional: `@setup/agents/heuristics-review.md` on your Figma frame
2. `@setup/agents/critique-prep.md` — decision ask, questions, paste-ready Slack post
3. After review: `templates/critique_notes.md`

**Vision / strategy**

- `@.claude/skills/vision_from_sources.md` + `templates/vision_onepager.md`

**Copy / voice**

- `@.claude/skills/humanizer.md` — full AI-pattern audit (see `.cursor/skills/humanizer/SKILL.md`)
- `@.claude/skills/rewrite_human.md` — lighter human tone pass

**Accessibility**

- `@.claude/skills/accessibility.md` or `@.cursor/skills/accessibility/SKILL.md`

**Decision hygiene**

- `@.claude/skills/decision_doc.md`

## Related tools

- **Heuristics Figma plugin** — same checklist IDs as `setup/agents/heuristics-review.md` (separate repo)
- **Critique prep Figma plugin** — form → Cursor prompt (separate repo)

## Regenerate this local export

From your local PD-OS checkout:

```bash
./setup/bin/export-agents-repo.sh ~/pd-os-agents-export
```

Contributions for the team should go to ai-native-knowledge-hub via PR.

## License

Internal Mozilla design ops — adjust before public release if needed.
EOF

if [[ ! -d "$DEST/.git" ]]; then
  git -C "$DEST" init -b main
  echo "  git init → $DEST"
fi

echo ""
echo "Standalone agents repo ready: $DEST"
echo ""
if [[ -d "$HOME/.cursor/skills" ]]; then
  ln -sfn "$DEST/.cursor/skills/accessibility" "$HOME/.cursor/skills/accessibility"
  echo "Global Cursor skill linked: ~/.cursor/skills/accessibility"
  echo ""
fi

# Remove skills not shipped in team export (stale from prior exports)
for name in $EXPORT_SKIP_SKILLS; do
  rm -rf "$DEST/.cursor/skills/$name"
done
rm -f "$DEST/.claude/skills/smart_window_design.md" 2>/dev/null || true
echo "Next steps:"
echo "  cd $DEST"
echo "  diff against canonical: "
echo "  contribute team changes via PR to ai-native-knowledge-hub (not a personal fork)"
