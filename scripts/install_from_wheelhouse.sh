#!/usr/bin/env bash
set -euo pipefail

# Install dependencies from a local wheelhouse (offline)
# Usage: ./scripts/install_from_wheelhouse.sh [WHEEL_DIR] [VENV_DIR]
# Example: ./scripts/install_from_wheelhouse.sh wheelhouse .venv

WHEEL_DIR="${1:-wheelhouse}"
VENV_DIR="${2:-.venv}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REQ_FILE="$ROOT_DIR/requirements.txt"

if [ ! -d "$ROOT_DIR/$WHEEL_DIR" ]; then
  echo "Diretório de wheels não encontrado: $ROOT_DIR/$WHEEL_DIR"
  exit 1
fi

if [ ! -d "$ROOT_DIR/$VENV_DIR" ]; then
  echo "Criando ambiente virtual em $ROOT_DIR/$VENV_DIR..."
  python3 -m venv "$ROOT_DIR/$VENV_DIR"
fi

echo "Ativando venv..."
# shellcheck disable=SC1090
source "$ROOT_DIR/$VENV_DIR/bin/activate"

echo "Instalando pacotes a partir do wheelhouse..."
pip install --upgrade pip
pip install --no-index --find-links="$ROOT_DIR/$WHEEL_DIR" -r "$REQ_FILE"

echo "Instalação concluída."

