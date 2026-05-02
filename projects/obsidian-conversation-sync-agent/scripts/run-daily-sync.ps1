[CmdletBinding()]
param(
    [string]$ConfigPath = (Join-Path $PSScriptRoot "..\config.local.json"),
    [string]$PythonPath = ""
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")
$ResolvedConfig = Resolve-Path -LiteralPath $ConfigPath -ErrorAction SilentlyContinue

if (-not $ResolvedConfig) {
    throw "Missing config file. Copy config.example.json to config.local.json and set your source and vault paths."
}

function Resolve-Python {
    param([string]$PreferredPython)

    if ($PreferredPython) {
        if (-not (Test-Path -LiteralPath $PreferredPython)) {
            throw "PythonPath was provided but was not found: $PreferredPython"
        }
        return $PreferredPython
    }

    $python = Get-Command python -ErrorAction SilentlyContinue
    if ($python -and $python.Source -notlike "*\WindowsApps\*") {
        return $python.Source
    }

    $codexPython = Join-Path $env:USERPROFILE ".cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
    if (Test-Path -LiteralPath $codexPython) {
        return $codexPython
    }

    $pythonLauncher = Get-Command py -ErrorAction SilentlyContinue
    if ($pythonLauncher) {
        return $pythonLauncher.Source
    }

    throw "Python was not found. Install Python 3.10+ or pass -PythonPath with a full python.exe path."
}

$Python = Resolve-Python -PreferredPython $PythonPath
$PreviousPythonPath = $env:PYTHONPATH

Push-Location -LiteralPath $ProjectRoot
try {
    if ($PreviousPythonPath) {
        $env:PYTHONPATH = "src;$PreviousPythonPath"
    } else {
        $env:PYTHONPATH = "src"
    }

    if ((Split-Path -Leaf $Python) -eq "py.exe") {
        & $Python -3 -m obsidian_sync_agent --config $ResolvedConfig
    } else {
        & $Python -m obsidian_sync_agent --config $ResolvedConfig
    }

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}
finally {
    $env:PYTHONPATH = $PreviousPythonPath
    Pop-Location
}
