#!/bin/bash
# Smart Window Design Skill — Setup for Claude Code
#
# Run this from wherever you cloned/downloaded the smart-window-design folder:
#
#   bash setup-claude-code.sh
#
# This copies the skill to your personal Claude Code skills directory
# so it's available across all your projects.

SKILL_DIR="$HOME/.claude/skills/smart-window-design"

echo "Installing Smart Window Design skill to Claude Code..."

# Create the skills directory if it doesn't exist
mkdir -p "$HOME/.claude/skills"

# Copy the skill
if [ -d "smart-window-design" ]; then
    cp -r smart-window-design "$HOME/.claude/skills/"
    echo "✓ Installed to $SKILL_DIR"
elif [ -f "SKILL.md" ]; then
    mkdir -p "$SKILL_DIR"
    cp -r . "$SKILL_DIR/"
    echo "✓ Installed to $SKILL_DIR"
else
    echo "✗ Error: Run this from the directory containing smart-window-design/ or SKILL.md"
    exit 1
fi

echo ""
echo "Skill structure:"
find "$SKILL_DIR" -type f | sed "s|$HOME|~|g"
echo ""
echo "Done. Claude Code will automatically discover this skill."
echo "To update later, just re-run this script."
