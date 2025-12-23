# Install mdBook and plugins using versions from ../versions.toml
# This ensures consistency between local development and CI

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$VersionsFile = Join-Path (Split-Path -Parent $ScriptDir) "versions.toml"

# Function to parse TOML and extract version
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

# Function to get all plugins from [mdbook-plugins] section
function Get-MdbookPlugins {
    $content = Get-Content $VersionsFile -Raw
    $plugins = @{}
    
    if ($content -match '(?ms)\[mdbook-plugins\](.*?)(\[|$)') {
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
} else {
    Write-Host "Error: Could not find mdbook version in versions.toml" -ForegroundColor Red
    exit 1
}

# Install mdBook plugins
Write-Host "`nInstalling mdBook plugins..." -ForegroundColor Cyan

$plugins = Get-MdbookPlugins
foreach ($plugin in $plugins.GetEnumerator()) {
    Write-Host "Installing $($plugin.Key) $($plugin.Value)..." -ForegroundColor Cyan
    cargo install $plugin.Key --version $plugin.Value
}

Write-Host "`n✓ Installation complete!" -ForegroundColor Green
Write-Host "`nInstalled versions:" -ForegroundColor Cyan
mdbook --version
cargo install --list | Select-String "mdbook"

