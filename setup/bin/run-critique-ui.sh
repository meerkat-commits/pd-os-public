#!/usr/bin/env bash
# Critique prep UI — keep this terminal open while you use the browser.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$REPO_ROOT"

if [[ -x "$REPO_ROOT/.venv/bin/python3" ]]; then
  PYTHON="$REPO_ROOT/.venv/bin/python3"
else
  PYTHON="python3"
fi

PORT="${PORT:-8767}"
OPEN_FLAG=()
if [[ "${1:-}" == "--open" ]] || [[ "${OPEN:-}" == "1" ]]; then
  OPEN_FLAG=(--open)
fi

echo "Starting critique prep UI on http://127.0.0.1:${PORT}/"
echo "Leave this terminal running. Press Ctrl+C to stop."
"$PYTHON" -m pd_os.cli critique-dashboard --port "$PORT" "${OPEN_FLAG[@]}"
