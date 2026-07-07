#!/usr/bin/env bash
# Daily automation: Granola sync (last 24h) + daily digest.
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

echo "[$(date -Iseconds)] pd-os daily: sync-granola + daily-digest"
"$PYTHON" -m pd_os.cli run-daily "$@"
