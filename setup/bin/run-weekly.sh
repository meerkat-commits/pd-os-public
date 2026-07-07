#!/usr/bin/env bash
# Weekly automation: Granola sync (last week) + weekly rollup.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# shellcheck source=pd-os-env.sh
source "$SCRIPT_DIR/pd-os-env.sh"

cd "$REPO_ROOT"

if [[ -x "$REPO_ROOT/.venv/bin/python3" ]]; then
  PYTHON="$REPO_ROOT/.venv/bin/python3"
else
  PYTHON="python3"
fi

echo "[$(date -Iseconds)] pd-os weekly: sync-granola + weekly-rollup"
"$PYTHON" -m pd_os.cli run-weekly "$@"
