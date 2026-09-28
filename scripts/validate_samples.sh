#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 -m os_resource_sim validate --type scheduling --input "$ROOT_DIR/data/samples/scheduling.json"
python3 -m os_resource_sim validate --type scheduling --input "$ROOT_DIR/data/samples/scheduling.csv"
python3 -m os_resource_sim validate --type memory --input "$ROOT_DIR/data/samples/memory.json"
python3 -m os_resource_sim validate --type deadlock --input "$ROOT_DIR/data/samples/deadlock_banker.json"
python3 -m os_resource_sim validate --type deadlock --input "$ROOT_DIR/data/samples/deadlock_detect.json"
python3 -m os_resource_sim validate --type storage --input "$ROOT_DIR/data/samples/storage.json"
python3 -m os_resource_sim validate --type storage --input "$ROOT_DIR/data/samples/storage.csv"

echo "All sample inputs are valid"
