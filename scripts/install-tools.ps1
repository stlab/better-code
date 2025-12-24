# Installs mdBook and plugins using versions from versions.toml.
#
# Reads tool versions from the repository root's versions.toml file and
# installs them via cargo. This ensures consistency between local development
# and CI environments.
#
# Usage: .\install-tools.ps1
#
# Preconditions:
#   - Rust and Cargo are installed and in PATH
#   - versions.toml exists in the repository root
#   - versions.toml contains [mdbook] section with version key

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$VersionsFile = Join-Path (Split-Path -Parent $ScriptDir) "versions.toml"

# Extracts a version string from versions.toml.
#
# Parameters:
#   Tool - Tool name matching a TOML section header (e.g., "mdbook")
#   Section - Optional. Parent section name for nested keys (e.g., "mdbook-plugins")
#
# Returns: The version string, or $null if not found
#
# When Section is empty:
#   - Searches for [Tool] section header
#   - Returns value of version key within that section
#   - Handles comments and blank lines between section header and version key
#
# When Section is provided:
#   - Searches for [Section] header
#   - Returns value of "Tool = version" within that section
#
# Example:
#   Get-ToolVersion -Tool "mdbook"
#   Get-ToolVersion -Tool "mdbook-katex" -Section "mdbook-plugins"
function Get-ToolVersion {
    param (
        [string]$Tool,
        [string]$Section = ""
    )
    
    $content = Get-Content $VersionsFile -Raw
    
    if ($Section) {
        # Extract from section like [mdbook-plugins]
        $pattern = "(?ms)\[$Section\].*?$Tool\s*=\s*`"([^`"]+)`""
    } else {
        # Extract from top-level section like [mdbook]
        $pattern = "(?ms)\[$Tool\].*?version\s*=\s*`"([^`"]+)`""
    }
    
    if ($content -match $pattern) {
        return $Matches[1]
    }
    return $null
}

# Extracts all plugin name-version pairs from [mdbook-plugins] section.
#
# Returns: A hashtable mapping plugin names to version strings
#
# The hashtable keys are plugin names (e.g., "mdbook-katex") and values
# are version strings (e.g., "0.10.0-alpha"). Returns an empty hashtable
# if the [mdbook-plugins] section is not found or contains no plugins.
#
# Example:
#   $plugins = Get-MdbookPlugins
#   foreach ($plugin in $plugins.GetEnumerator()) {
#       Write-Host "$($plugin.Key) version $($plugin.Value)"
#   }
function Get-MdbookPlugins {
    $content = Get-Content $VersionsFile -Raw
    $plugins = @{}
    
    # Capture everything *after* the header line up to (but not including) the next section header.
    # Use \z (end-of-string) instead of $ (end-of-line in multiline mode).
    if ($content -match '(?ms)^\[mdbook-plugins\]\s*\r?\n(.*?)(?=^\[|\z)') {
        $section = $Matches[1]
        $lines = $section -split "`n"
        
        foreach ($line in $lines) {
            if ($line -match '^([a-zA-Z0-9_-]+)\s*=\s*"([^"]+)"') {
                $plugins[$Matches[1]] = $Matches[2]
            }
        }
    }
    
    return $plugins
}

Write-Host "Reading versions from $VersionsFile..." -ForegroundColor Cyan

# Install mdBook
$MdbookVersion = Get-ToolVersion -Tool "mdbook"
if ($MdbookVersion) {
    Write-Host "`nInstalling mdBook $MdbookVersion..." -ForegroundColor Cyan
    cargo install mdbook --version $MdbookVersion
    if ($LASTEXITCODE -ne 0) {
        exit 1
    }
} else {
    Write-Host "Error: Could not find mdbook version in versions.toml" -ForegroundColor Red
    exit 1
}

# Install mdBook plugins
Write-Host "`nInstalling mdBook plugins..." -ForegroundColor Cyan

$plugins = Get-MdbookPlugins
foreach ($plugin in $plugins.GetEnumerator()) {
    $pluginName = $plugin.Key
    $pluginVersion = $plugin.Value
    
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
            continue
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

