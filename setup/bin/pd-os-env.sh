#!/usr/bin/env bash
# Shared env for PD-OS launchd jobs and setup/bin runners.
set -euo pipefail

PD_OS_ENV_FILE="${PD_OS_ENV_FILE:-$HOME/.config/pd-os/env}"
if [[ -f "$PD_OS_ENV_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$PD_OS_ENV_FILE"
fi
