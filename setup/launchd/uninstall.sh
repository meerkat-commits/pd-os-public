#!/usr/bin/env bash
# Remove PD-OS launchd jobs from macOS.
set -euo pipefail

LAUNCH_AGENTS="${HOME}/Library/LaunchAgents"
UID_NUM="$(id -u)"

for job in daily weekly; do
  label="com.pd-os.${job}"
  launchctl bootout "gui/${UID_NUM}/${label}" 2>/dev/null || true
  rm -f "${LAUNCH_AGENTS}/${label}.plist"
  echo "Removed ${label}"
done

echo "Done."
