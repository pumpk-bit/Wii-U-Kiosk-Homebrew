# Put devkitPro / wut on PATH for this shell session.
#
#   source tools/env.sh
#
# Honors DEVKITPRO / DEVKITPPC if they are already set. Otherwise looks in
# the usual install locations. Not tied to any one machine or username.

_dkp_unix() {
  case "$1" in
    [A-Za-z]:*)
      if command -v cygpath >/dev/null 2>&1; then
        cygpath -u "$1"
        return
      fi
      ;;
  esac
  printf '%s' "$1"
}

_dkp_is_root() {
  [ -n "$1" ] && [ -d "$1/devkitPPC" ]
}

_dkp_find() {
  set -- \
    "${DEVKITPRO:-}" \
    /opt/devkitpro \
    /opt/devkitPro \
    /c/devkitPro \
    /d/devkitPro \
    "$HOME/devkitpro" \
    "$HOME/devkitPro"

  for c in "$@"; do
    c="$(_dkp_unix "$c")"
    if _dkp_is_root "$c"; then
      (CDPATH= cd -- "$c" && pwd)
      return 0
    fi
  done
  return 1
}

if ! _dkp_is_root "${DEVKITPRO:-}"; then
  if _dkp_is_root "$(_dkp_unix "${DEVKITPRO:-}")"; then
    DEVKITPRO="$(_dkp_unix "$DEVKITPRO")"
  elif ! DEVKITPRO="$(_dkp_find)"; then
    echo "devkitPro not found." >&2
    echo "Install the Wii U tools from https://devkitpro.org/wiki/Getting_Started" >&2
    echo "then set DEVKITPRO (official default is /opt/devkitpro or C:\\devkitPro)." >&2
    unset -f _dkp_is_root _dkp_find _dkp_unix
    return 1 2>/dev/null || exit 1
  fi
fi

export DEVKITPRO
if [ -n "${DEVKITPPC:-}" ] && [ ! -d "$DEVKITPPC" ]; then
  _ppc_unix="$(_dkp_unix "$DEVKITPPC")"
  if [ -d "$_ppc_unix" ]; then
    DEVKITPPC="$_ppc_unix"
  fi
  unset _ppc_unix
fi
if [ -z "${DEVKITPPC:-}" ] || [ ! -d "$DEVKITPPC" ]; then
  DEVKITPPC="$DEVKITPRO/devkitPPC"
fi
export DEVKITPPC

# Current dkp CMake wrapper: $DEVKITPRO/portlibs/wiiu/bin/powerpc-eabi-cmake
# Older installs kept a copy under wut/usr/bin. Keep both.
for _dkp_bin in \
  "$DEVKITPRO/portlibs/wiiu/bin" \
  "$DEVKITPPC/bin" \
  "$DEVKITPRO/tools/bin" \
  "$DEVKITPRO/wut/usr/bin" \
  "$DEVKITPRO/msys2/usr/bin"
do
  if [ -d "$_dkp_bin" ]; then
    case ":$PATH:" in
      *":$_dkp_bin:"*) ;;
      *) PATH="$_dkp_bin:$PATH" ;;
    esac
  fi
done
export PATH
unset _dkp_bin
unset -f _dkp_is_root _dkp_find _dkp_unix

echo "DEVKITPRO = $DEVKITPRO"
echo "DEVKITPPC = $DEVKITPPC"
