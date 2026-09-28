#!/usr/bin/env bash
set -euo pipefail

command -v python3 >/dev/null 2>&1 || { echo "python3 is required" >&2; exit 1; }
command -v pytest >/dev/null 2>&1 || { echo "pytest is required" >&2; exit 1; }

echo "Environment OK"
python3 --version
pytest --version
