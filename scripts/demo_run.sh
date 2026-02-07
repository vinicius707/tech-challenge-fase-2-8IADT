#!/usr/bin/env bash
set -euo pipefail

echo "Demo run: quick GA -> export -> generate instructions"
PYTHONPATH=. python3 scripts/run_ga_example.py
RUN_DIR=$(ls -dt experiments/run_* | head -n1)
echo "Run dir: $RUN_DIR"
PYTHONPATH=. python3 scripts/export_artifacts.py "$RUN_DIR"
PYTHONPATH=. python3 scripts/generate_instructions.py "$RUN_DIR"
echo "Demo completed. Open $RUN_DIR/route_map.html in your browser."

