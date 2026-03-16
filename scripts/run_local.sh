#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$ROOT_DIR/.venv"

echo "Projeto root: $ROOT_DIR"

if [ ! -d "$VENV_DIR" ]; then
  echo "Criando ambiente virtual em $VENV_DIR..."
  python3 -m venv "$VENV_DIR"
fi

echo "Ativando ambiente virtual..."
# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

echo "Instalando dependências (requirements.txt)..."
pip install --upgrade pip
pip install -r "$ROOT_DIR/requirements.txt"

CFG="${1:-experiments/configs/experiment_01.yaml}"
OUT_DIR="${2:-experiments/run_local}"

echo "Executando runner de exemplo com config: $CFG"
python -m src.optimize --config "$CFG" --output "$OUT_DIR"

echo "Pronto. Artefatos gravados em: $OUT_DIR"

