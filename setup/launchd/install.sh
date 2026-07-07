#!/usr/bin/env bash
# Install PD-OS daily + weekly launchd jobs on macOS.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LAUNCH_AGENTS="${HOME}/Library/LaunchAgents"
ENV_DIR="${HOME}/.config/pd-os"
ENV_FILE="${ENV_DIR}/env"

echo "PD-OS launchd install"
echo "  Repo:          ${REPO_ROOT}"
echo "  LaunchAgents:  ${LAUNCH_AGENTS}"
echo ""

# Python venv
if [[ ! -x "${REPO_ROOT}/.venv/bin/python3" ]]; then
  echo "Creating venv at ${REPO_ROOT}/.venv ..."
  python3 -m venv "${REPO_ROOT}/.venv"
  "${REPO_ROOT}/.venv/bin/pip" install -r "${REPO_ROOT}/requirements.txt"
else
  echo "Using existing venv: ${REPO_ROOT}/.venv"
fi

# Secrets file (outside git)
if [[ ! -f "${ENV_FILE}" ]]; then
  mkdir -p "${ENV_DIR}"
  cp "${REPO_ROOT}/setup/config/env.example" "${ENV_FILE}"
  chmod 600 "${ENV_FILE}"
  echo ""
  echo "Created ${ENV_FILE}"
  echo "  → Edit it and set GRANOLA_API_KEY, then re-run this installer (or load jobs below)."
  echo ""
else
  echo "Secrets file exists: ${ENV_FILE}"
fi

# Executable runners
chmod +x "${REPO_ROOT}/setup/bin/"*.sh

mkdir -p "${LAUNCH_AGENTS}"

for job in daily weekly; do
  src="${SCRIPT_DIR}/com.pd-os.${job}.plist"
  dest="${LAUNCH_AGENTS}/com.pd-os.${job}.plist"
  sed "s|@REPO_ROOT@|${REPO_ROOT}|g" "${src}" > "${dest}"
  echo "Wrote ${dest}"
done

echo ""
echo "Loading launch agents ..."
launchctl bootout "gui/$(id -u)/com.pd-os.daily" 2>/dev/null || true
launchctl bootout "gui/$(id -u)/com.pd-os.weekly" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "${LAUNCH_AGENTS}/com.pd-os.daily.plist"
launchctl bootstrap "gui/$(id -u)" "${LAUNCH_AGENTS}/com.pd-os.weekly.plist"

echo ""
echo "Installed."
echo "  Daily:  every day 16:00 — Granola sync (24h) + digest + commitments + project hygiene"
echo "  Weekly: Mondays 07:30 — Granola sync (last week) + rollup + commitments + project hygiene"
echo ""
echo "Test now:"
echo "  ${REPO_ROOT}/setup/bin/run-daily.sh"
echo "  ${REPO_ROOT}/setup/bin/run-weekly.sh"
echo ""
echo "Logs:"
echo "  tail -f /tmp/pd-os.daily.log"
echo "  tail -f /tmp/pd-os.weekly.log"
