#!/usr/bin/env bash
# Install daily Firefox Nightly Nova screenshot launchd job.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LAUNCH_AGENTS="${HOME}/Library/LaunchAgents"

if [[ ! -x "${REPO_ROOT}/.venv/bin/python3" ]]; then
  echo "Creating venv at ${REPO_ROOT}/.venv ..."
  python3 -m venv "${REPO_ROOT}/.venv"
  "${REPO_ROOT}/.venv/bin/pip" install -r "${REPO_ROOT}/requirements.txt"
fi

chmod +x "${REPO_ROOT}/setup/bin/run-nightly-nova-screenshots.sh"

src="${SCRIPT_DIR}/com.pd-os.nightly-nova.plist"
dest="${LAUNCH_AGENTS}/com.pd-os.nightly-nova.plist"
mkdir -p "${LAUNCH_AGENTS}"
sed "s|@REPO_ROOT@|${REPO_ROOT}|g" "${src}" > "${dest}"
echo "Wrote ${dest}"

echo ""
echo "Loading launch agent ..."
launchctl bootout "gui/$(id -u)/com.pd-os.nightly-nova" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "${dest}"

echo ""
echo "Installed nightly Nova screenshots."
echo "  Daily: 06:30 — Firefox Nightly punch-QA captures"
echo ""
echo "Test:"
echo "  ${REPO_ROOT}/setup/bin/run-nightly-nova-screenshots.sh --dry-run"
echo "  ${REPO_ROOT}/setup/bin/run-nightly-nova-screenshots.sh --only chrome"
echo ""
echo "Uninstall: ./setup/launchd/uninstall-nightly-nova.sh"
