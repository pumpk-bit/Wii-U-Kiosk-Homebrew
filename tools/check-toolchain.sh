#!/usr/bin/env bash
# Verify the Wii U homebrew toolchain is usable on this machine.
#
#   bash tools/check-toolchain.sh

set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
# shellcheck source=env.sh
. "$ROOT/tools/env.sh"

missing=""
PYTHON_CMD=""

have() { command -v "$1" >/dev/null 2>&1; }

check() {
  label="$1"
  shift
  for n in "$@"; do
    if have "$n"; then
      printf '%-22s %s\n' "$label" "$(command -v "$n")"
      return 0
    fi
  done
  printf '%-22s MISSING\n' "$label"
  missing="$missing $label"
}

check_python() {
  label="$1"
  shift
  for n in "$@"; do
    if have "$n"; then
      PYTHON_CMD="$n"
      printf '%-22s %s\n' "$label" "$(command -v "$n")"
      return 0
    fi
  done
  printf '%-22s MISSING\n' "$label"
  missing="$missing $label"
}

check_opt() {
  label="$1"
  shift
  for n in "$@"; do
    if have "$n"; then
      printf '%-22s %s\n' "$label" "$(command -v "$n")"
      return 0
    fi
  done
  printf '%-22s not found (optional)\n' "$label"
}

echo "DEVKITPRO = $DEVKITPRO"
echo "DEVKITPPC = $DEVKITPPC"
echo

check powerpc-eabi-gcc powerpc-eabi-gcc
check powerpc-eabi-cmake powerpc-eabi-cmake
check elf2rpl elf2rpl
check cmake cmake
check_python python python3 python
check_opt wuhbtool wuhbtool

if [ -n "$missing" ]; then
  echo >&2
  echo "Missing:$missing" >&2
  echo >&2
  echo "Install from https://devkitpro.org/wiki/Getting_Started" >&2
  echo "Then:" >&2
  echo "  Windows MSYS2:  pacman -Syu --needed wiiu-dev cmake python" >&2
  echo "  Linux/macOS:    sudo dkp-pacman -Syu --needed wiiu-dev" >&2
  echo "                  (install cmake and python3 from your OS as well)" >&2
  echo "See docs/HowToBuild.MD" >&2
  exit 1
fi

if ! "$PYTHON_CMD" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 8) else 1)'; then
  echo "Python 3.8 or newer is required (found $($PYTHON_CMD --version 2>&1))." >&2
  exit 1
fi

gcc_ver="$(powerpc-eabi-gcc --version)"
printf '%s\n' "$gcc_ver" | sed -n '1p'
echo "Toolchain check passed."
