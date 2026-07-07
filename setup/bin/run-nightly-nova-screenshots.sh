#!/usr/bin/env bash
# Daily Nova punch-QA screenshots from Firefox Nightly (macOS).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# shellcheck source=pd-os-env.sh
source "$SCRIPT_DIR/pd-os-env.sh"

cd "$REPO_ROOT"

"$SCRIPT_DIR/check-nightly-capture-prereqs.sh"

if [[ ! -d "$REPO_ROOT/.venv" ]]; then
  echo "Creating .venv and installing dependencies…"
  python3 -m venv "$REPO_ROOT/.venv"
fi
PYTHON="$REPO_ROOT/.venv/bin/python3"
"$PYTHON" -m pip install -q -r "$REPO_ROOT/requirements.txt"

echo "[$(date -Iseconds)] pd-os nightly-nova-screenshots"
"$PYTHON" -m pd_os.cli nightly-nova-screenshots --sync-figjam "$@"
