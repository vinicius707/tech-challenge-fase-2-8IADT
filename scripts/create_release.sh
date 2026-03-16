#!/usr/bin/env bash
set -euo pipefail

RELEASE_DIR="releases"
TIMESTAMP="$(date +%s)"
RELEASE_NAME="tech-challenge-v0.1.0-${TIMESTAMP}.zip"
OUT_PATH="${RELEASE_DIR}/${RELEASE_NAME}"

mkdir -p "${RELEASE_DIR}"

echo "Creating release bundle: ${OUT_PATH}"

# Files to include
INCLUDES=(
  "README.md"
  "docs/"
  "src/"
  "scripts/"
  "notebooks/"
  "requirements.txt"
  "pyproject.toml"
)

zip -r "${OUT_PATH}" "${INCLUDES[@]}"

echo "Release bundle created: ${OUT_PATH}"
echo "Size: $(du -h ${OUT_PATH} | cut -f1)"

