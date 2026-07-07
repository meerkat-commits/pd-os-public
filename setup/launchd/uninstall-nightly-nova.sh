#!/usr/bin/env bash
set -euo pipefail

LAUNCH_AGENTS="${HOME}/Library/LaunchAgents"
dest="${LAUNCH_AGENTS}/com.pd-os.nightly-nova.plist"

launchctl bootout "gui/$(id -u)/com.pd-os.nightly-nova" 2>/dev/null || true
rm -f "${dest}"
echo "Removed com.pd-os.nightly-nova"
