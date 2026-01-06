# Installs mdBook and plugins using versions from versions.txt.
#
# Reads tool versions from the repository root's versions.txt file and
# installs them via cargo. This ensures consistency between local development
# and CI environments.
#
# Usage: .\install-tools.ps1
#
# Preconditions:
#   - Rust and Cargo are installed and in PATH
#   - versions.txt exists in the repository root

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$VersionsFile = Join-Path (Split-Path -Parent $ScriptDir) "versions.txt"

Write-Host "Reading versions from $VersionsFile..." -ForegroundColor Cyan

# Install mdBook
$mdbookLine = Get-Content $VersionsFile | Where-Object { $_ -match '^mdbook=' }
if ($mdbookLine) {
    $mdbookVersion = $mdbookLine.Split('=')[1]
    Write-Host "`nInstalling mdBook $mdbookVersion..." -ForegroundColor Cyan
    cargo install mdbook --version $mdbookVersion
    if ($LASTEXITCODE -ne 0) {
        exit 1
    }
} else {
    Write-Host "Error: Could not find mdbook version in versions.txt" -ForegroundColor Red
    exit 1
}

# Install mdBook plugins
Write-Host "`nInstalling mdBook plugins..." -ForegroundColor Cyan

# Process all lines starting with "mdbook-" (plugins)
Get-Content $VersionsFile | Where-Object { $_ -match '^mdbook-' } | ForEach-Object {
    $pluginName, $pluginVersion = $_ -split '=', 2
    
    # mdbook-katex requires special handling on Windows
    # See: https://github.com/lzanini/mdbook-katex#windows-users
    if ($pluginName -eq "mdbook-katex") {
        Write-Host "Installing $pluginName $pluginVersion with duktape backend (Windows)..." -ForegroundColor Cyan
        Write-Host "  Note: Using duktape backend. Some features like matrices may not work." -ForegroundColor Yellow
        Write-Host "  For full functionality, download pre-built binary from:" -ForegroundColor Yellow
        Write-Host "  https://github.com/lzanini/mdbook-katex/releases" -ForegroundColor Yellow
        cargo install $pluginName --version $pluginVersion --no-default-features --features duktape
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Failed to install $pluginName. Continuing without it..." -ForegroundColor Yellow
            return
        }
    } else {
        Write-Host "Installing $pluginName $pluginVersion..." -ForegroundColor Cyan
        cargo install $pluginName --version $pluginVersion
        if ($LASTEXITCODE -ne 0) {
            exit 1
        }
    }
}

Write-Host "`n✓ Installation complete!" -ForegroundColor Green
Write-Host "`nInstalled versions:" -ForegroundColor Cyan
mdbook --version
cargo install --list | Select-String "mdbook"

