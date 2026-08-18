# Verify the Wii U homebrew toolchain is usable on this machine.
#
#   powershell -File tools/check-toolchain.ps1
#
# On Windows the real compiler lives in MSYS2. This script prefers bash
# (Git Bash / MSYS2). If bash is missing it only checks that files exist
# and tells you how to open a build shell.

$ErrorActionPreference = 'Stop'
. "$PSScriptRoot\env.ps1"

$bash = Get-Command bash -ErrorAction SilentlyContinue
if ($bash) {
    & $bash.Source "$PSScriptRoot/check-toolchain.sh"
    exit $LASTEXITCODE
}

function Test-ToolFile([string]$Label, [string[]]$Paths, [switch]$Optional) {
    $hit = $Paths | Where-Object { $_ -and (Test-Path -LiteralPath $_) } | Select-Object -First 1
    if ($hit) {
        Write-Host ("{0,-22} {1}" -f $Label, $hit)
        return $true
    }
    if ($Optional) {
        Write-Host ("{0,-22} not found (optional)" -f $Label)
        return $true
    }
    Write-Host ("{0,-22} MISSING" -f $Label)
    return $false
}

Write-Host 'DEVKITPRO =' $env:DEVKITPRO
Write-Host 'DEVKITPPC =' $env:DEVKITPPC
Write-Host ''

$ok = $true
$ok = (Test-ToolFile 'powerpc-eabi-gcc' @(
    (Join-Path $env:DEVKITPPC 'bin\powerpc-eabi-gcc.exe')
    (Join-Path $env:DEVKITPPC 'bin\powerpc-eabi-gcc')
)) -and $ok
$ok = (Test-ToolFile 'powerpc-eabi-cmake' @(
    (Join-Path $env:DEVKITPRO 'portlibs\wiiu\bin\powerpc-eabi-cmake')
    (Join-Path $env:DEVKITPRO 'portlibs\wiiu\bin\powerpc-eabi-cmake.exe')
    (Join-Path $env:DEVKITPRO 'portlibs\wiiu\bin\powerpc-eabi-cmake.bat')
    (Join-Path $env:DEVKITPRO 'wut\usr\bin\powerpc-eabi-cmake')
    (Join-Path $env:DEVKITPRO 'wut\usr\bin\powerpc-eabi-cmake.bat')
)) -and $ok
$ok = (Test-ToolFile 'elf2rpl' @(
    (Join-Path $env:DEVKITPRO 'tools\bin\elf2rpl.exe')
    (Join-Path $env:DEVKITPRO 'tools\bin\elf2rpl')
)) -and $ok

$py = Get-Command python3, python, python3.exe, python.exe -ErrorAction SilentlyContinue | Select-Object -First 1
if ($py) {
    Write-Host ("{0,-22} {1}" -f 'python', $py.Source)
} else {
    Write-Host ("{0,-22} MISSING" -f 'python')
    $ok = $false
}

Test-ToolFile 'wuhbtool' @(
    (Join-Path $env:DEVKITPRO 'tools\bin\wuhbtool.exe')
    (Join-Path $env:DEVKITPRO 'tools\bin\wuhbtool')
) -Optional | Out-Null

if (-not $ok) {
    throw @"

Toolchain files are missing.

Install from https://devkitpro.org/wiki/Getting_Started
Then in the MSYS2 shell:
  pacman -Syu --needed wiiu-dev cmake python

See docs/HowToBuild.MD
"@
}

Write-Host ''
Write-Host 'Files look present. Windows builds still need the MSYS2 shell:'
Write-Host '  powershell -File tools/launch-msys2-wiiu.ps1'
Write-Host 'Then:  bash tools/check-toolchain.sh'
Write-Host '       bash tools/build-all.sh'
