#!/usr/bin/env bash
# Build every kiosk title and write Cafe XML into Release/.
#
# Run from a shell that has wut (MSYS2 / Linux / macOS):
#   bash tools/build-all.sh
#   bash tools/build-all.sh "Featured List"

set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
# shellcheck source=env.sh
. "$ROOT/tools/env.sh"

need() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing '$1'." >&2
    echo "Install from https://devkitpro.org/wiki/Getting_Started" >&2
    echo "Then re-run from that environment, or: source tools/env.sh" >&2
    exit 1
  fi
}

need powerpc-eabi-cmake
need cmake
need elf2rpl

if command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON=python
else
  echo "Missing Python 3." >&2
  echo "Install Python 3.8+ and re-run. See docs/HowToBuild.MD" >&2
  exit 1
fi

if ! "$PYTHON" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 8) else 1)'; then
  echo "Python 3.8 or newer is required (found $($PYTHON --version 2>&1))." >&2
  exit 1
fi

ALL_TITLES=(
  "Featured List"
  "New Releases"
  "About Wii U"
  "Attract Mode"
  "About Amiibo"
)

if [ "$#" -eq 0 ]; then
  TITLES=("${ALL_TITLES[@]}")
else
  TITLES=("$@")
fi

for title in "${TITLES[@]}"; do
  src="$ROOT/$title"
  if [ ! -f "$src/CMakeLists.txt" ]; then
    echo "No CMakeLists.txt in $src" >&2
    echo "Known titles:" >&2
    printf '  %s\n' "${ALL_TITLES[@]}" >&2
    exit 1
  fi
  echo "==> $title"
  powerpc-eabi-cmake -S "$src" -B "$src/build"
  cmake --build "$src/build"
done

"$PYTHON" "$ROOT/tools/generate_title_xml.py"
echo "Done. FTP folders are under $ROOT/Release/"
