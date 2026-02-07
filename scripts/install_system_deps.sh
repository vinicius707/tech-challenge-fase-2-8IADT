#!/usr/bin/env bash
set -euo pipefail

# Instala dependências de sistema necessárias para bibliotecas geoespaciais
# Suporta: Ubuntu/Debian (apt) e macOS (Homebrew).
# Windows: recomenda-se usar Conda/Miniconda (ver README).
#
# Uso:
#   ./scripts/install_system_deps.sh [ubuntu|macos]
# Ex.: ./scripts/install_system_deps.sh ubuntu

OS_ARG="${1:-}"

function ensure_sudo() {
  if [ "$EUID" -ne 0 ]; then
    echo "Alguns comandos exigem privilégios de sudo. Você será solicitado a fornecer sua senha."
  fi
}

if [ -z "$OS_ARG" ]; then
  echo "Detectando sistema operacional..."
  UNAME="$(uname -s)"
  case "$UNAME" in
    Linux*)   OS="ubuntu" ;;
    Darwin*)  OS="macos" ;;
    *)        echo "SO não reconhecido: $UNAME. Passe 'ubuntu' ou 'macos' como argumento."; exit 1 ;;
  esac
else
  OS="$(echo "$OS_ARG" | tr '[:upper:]' '[:lower:]')"
fi

echo "Instalando dependências de sistema para: $OS"

if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
  ensure_sudo
  echo "Atualizando repositórios e instalando pacotes (apt)..."
  sudo apt-get update
  sudo apt-get install -y --no-install-recommends \
    build-essential python3-dev python3-venv \
    gdal-bin libgdal-dev libpq-dev \
    libgeos-dev libproj-dev
  echo "Instalação concluída. Se for usar o wheelhouse, gere-o em uma máquina com internet (scripts/build_wheelhouse.sh)."

elif [ "$OS" = "macos" ] || [ "$OS" = "darwin" ]; then
  echo "Verificando Homebrew..."
  if ! command -v brew >/dev/null 2>&1; then
    echo "Homebrew não encontrado. Instalando Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    echo "Após a instalação do Homebrew, pode ser necessário adicionar brew ao PATH."
  fi
  echo "Instalando pacotes via Homebrew..."
  brew update
  brew install gdal proj geos
  echo "Instalação concluída. Em Apple Silicon, verifique se está usando o Homebrew corretamente em /opt/homebrew."

else
  echo "SO / opção não suportada: $OS"
  exit 1
fi

echo "Pronto."

