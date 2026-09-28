#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cat "$ROOT_DIR/data/samples/scheduling.csv" | python3 -m os_resource_sim schedule --algorithm fcfs --input -
