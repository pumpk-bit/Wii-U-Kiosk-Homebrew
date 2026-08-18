# Open the DevkitPro MSYS2 shell in this repo so powerpc-eabi-cmake is on PATH.
#
# Usage:
#   powershell -File tools/launch-msys2-wiiu.ps1

$ErrorActionPreference = 'Stop'

if (-not $IsWindows -and $PSVersionTable.PSVersion.Major -ge 6) {
    throw "This launcher is for Windows. On Linux/macOS use a normal shell: source tools/env.sh"
}

. "$PSScriptRoot\env.ps1"

$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path

$candidates = @(
    (Join-Path $env:DEVKITPRO 'msys2\msys2_shell.cmd')
    'C:\devkitPro\msys2\msys2_shell.cmd'
    'C:\msys64\msys2_shell.cmd'
    'D:\msys64\msys2_shell.cmd'
)

$msys = $candidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $msys) {
    throw @"
MSYS2 launcher not found.

devkitPro on Windows ships MSYS2 next to the toolchain:
  $($env:DEVKITPRO)\msys2\msys2_shell.cmd

Install it from https://devkitpro.org/wiki/Getting_Started then re-run.
If you already have a Unix shell with wut, you do not need this script —
run bash tools/build-all.sh there instead.
"@
}

Start-Process -FilePath $msys -ArgumentList @('-defterm', '-no-start', '-use-full-path', '-here') -WorkingDirectory $repo
Write-Host "Opened MSYS2 in $repo"
