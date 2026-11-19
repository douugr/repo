#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
bash tools/build-repo.sh
python3 tools/build-pages.py
