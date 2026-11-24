#!/usr/bin/env sh
# Publish DevWorkbench skills for macOS, Linux, and Git Bash.
set -eu
ROOT=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
SCRIPT="$ROOT/scripts/setup.py"

if command -v python3 >/dev/null 2>&1; then
    exec python3 "$SCRIPT" "$@"
fi
if command -v py >/dev/null 2>&1; then
    exec py -3 "$SCRIPT" "$@"
fi
if command -v python >/dev/null 2>&1; then
    exec python "$SCRIPT" "$@"
fi

echo "DevWorkbench setup needs Python 3." >&2
exit 1
