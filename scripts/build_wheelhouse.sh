#!/usr/bin/env bash
set -euo pipefail

# Build a wheelhouse (collection of wheels) for offline installation.
# Usage: ./scripts/build_wheelhouse.sh [PYTHON_EXECUTABLE] [WHEEL_DIR]
# Example: ./scripts/build_wheelhouse.sh python3.10 wheelhouse

PYTHON_BIN="${1:-python3}"
WHEEL_DIR="${2:-wheelhouse}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REQ_FILE="$ROOT_DIR/requirements.txt"

if [ ! -f "$REQ_FILE" ]; then
  echo "requirements.txt não encontrado em $ROOT_DIR"
  exit 1
fi

mkdir -p "$ROOT_DIR/$WHEEL_DIR"

echo "Usando $PYTHON_BIN para construir wheels..."
echo "Wheels serão salvos em: $ROOT_DIR/$WHEEL_DIR"

# Upgrade pip/setuptools/wheel first
"$PYTHON_BIN" -m pip install --upgrade pip setuptools wheel

# Build wheels into the wheel directory
"$PYTHON_BIN" -m pip wheel --wheel-dir "$ROOT_DIR/$WHEEL_DIR" -r "$REQ_FILE"

echo "Wheelhouse criado com sucesso em: $ROOT_DIR/$WHEEL_DIR"
echo "Copie esse diretório para o ambiente offline e instale com --no-index --find-links."

