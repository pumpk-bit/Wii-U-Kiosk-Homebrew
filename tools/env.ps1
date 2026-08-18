# Put devkitPro / wut on PATH for this PowerShell session.
#
# Dot-source it (so the variables stick):
#   . .\tools\env.ps1
#
# Honors DEVKITPRO / DEVKITPPC if they are already set. Otherwise looks in
# the usual install locations. Not tied to any one machine or username.

$ErrorActionPreference = 'Stop'

function Test-DevkitRoot([string]$Path) {
    if (-not $Path) { return $false }
    return (Test-Path -LiteralPath (Join-Path $Path 'devkitPPC'))
}

function Find-DevkitPro {
    $candidates = @()
    if ($env:DEVKITPRO) { $candidates += $env:DEVKITPRO }
    $candidates += @(
        'C:\devkitPro'
        'D:\devkitPro'
        '/opt/devkitpro'
        (Join-Path $HOME 'devkitpro')
        (Join-Path $HOME 'devkitPro')
    )
    foreach ($c in $candidates) {
        if (Test-DevkitRoot $c) {
            return [System.IO.Path]::GetFullPath($c)
        }
    }
    return $null
}

$dkp = Find-DevkitPro
if (-not $dkp) {
    throw @"
devkitPro not found.

Install the Wii U tools from https://devkitpro.org/wiki/Getting_Started
then either:
  - set DEVKITPRO to that folder (official default is C:\devkitPro or /opt/devkitpro), or
  - re-run this script after installing to a standard path.
"@
}

$env:DEVKITPRO = $dkp
if (-not $env:DEVKITPPC -or -not (Test-Path -LiteralPath $env:DEVKITPPC)) {
    $env:DEVKITPPC = Join-Path $dkp 'devkitPPC'
}

function Join-DKP([string]$Root, [string[]]$Parts) {
    $p = $Root
    foreach ($part in $Parts) { $p = Join-Path $p $part }
    return $p
}

$prepend = @(
    (Join-DKP $dkp @('portlibs', 'wiiu', 'bin'))
    (Join-DKP $env:DEVKITPPC @('bin'))
    (Join-DKP $dkp @('tools', 'bin'))
    (Join-DKP $dkp @('wut', 'usr', 'bin'))
    (Join-DKP $dkp @('msys2', 'usr', 'bin'))
) | Where-Object { Test-Path -LiteralPath $_ }

$parts = $env:PATH -split [IO.Path]::PathSeparator | Where-Object { $_ }
$env:PATH = ($prepend + $parts | Select-Object -Unique) -join [IO.Path]::PathSeparator

Write-Host "DEVKITPRO = $env:DEVKITPRO"
Write-Host "DEVKITPPC = $env:DEVKITPPC"
