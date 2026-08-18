# Build every kiosk title. Prefers the Unix script (MSYS2 / Git Bash).
#
#   powershell -File tools/build-all.ps1
#   powershell -File tools/build-all.ps1 "Featured List"

$ErrorActionPreference = 'Stop'
. "$PSScriptRoot\env.ps1"

$bash = Get-Command bash -ErrorAction SilentlyContinue
if (-not $bash) {
    throw @"
No bash on PATH.

Wii U builds need the devkitPro MSYS2 shell (powerpc-eabi-cmake).
Run:  powershell -File tools/launch-msys2-wiiu.ps1
Then: bash tools/build-all.sh
See docs/HowToBuild.MD
"@
}

& $bash.Source "$PSScriptRoot/build-all.sh" @args
if ($null -ne $LASTEXITCODE) { exit $LASTEXITCODE }
exit 0
