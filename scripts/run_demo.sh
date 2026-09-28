#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 -m os_resource_sim demo --root "$ROOT_DIR" --output-dir "$ROOT_DIR/reports/generated"
