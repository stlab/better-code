#!/bin/bash
# Installs mdBook and plugins using versions from versions.toml.
#
# Reads tool versions from the repository root's versions.toml file and
# installs them via cargo. This ensures consistency between local development
# and CI environments.
#
# Usage: ./install-tools.sh
#
# Preconditions:
#   - Rust and Cargo are installed and in PATH
#   - versions.toml exists in the repository root
#   - versions.toml contains [mdbook] section with version key
#
# Complexity: O(N) where N is the number of plugins to install

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERSIONS_FILE="${SCRIPT_DIR}/../versions.toml"

# Extracts a version string from versions.toml.
#
# Parameters:
#   $1 (tool) - Tool name matching a TOML section header (e.g., "mdbook")
#   $2 (section) - Optional. Parent section name for nested keys (e.g., "mdbook-plugins")
#
# Returns: The version string on stdout, or empty if not found
#
# When section is empty:
#   - Searches for [tool] section header
#   - Returns value of version key within that section
#   - Handles comments and blank lines between section header and version key
#
# When section is provided:
#   - Searches for [section] header
#   - Returns value of "tool = version" within that section
#
# Example:
#   get_version "mdbook"              # Returns version from [mdbook]
#   get_version "mdbook-katex" "mdbook-plugins"  # Returns version from [mdbook-plugins]
get_version() {
    local tool=$1
    local section=$2
    
    if [ -z "$section" ]; then
        # Top-level tool like [mdbook]
        # Use awk to handle comments/blank lines between section header and version key
        awk -v tool="$tool" '
            BEGIN { in_section = 0 }
            $0 ~ ("^\\[" tool "\\]$") { in_section = 1; next }
            in_section && /^\[/ { exit }
            in_section && /^version[[:space:]]*=/ {
                match($0, /"([^"]+)"/, arr)
                print arr[1]
                exit
            }
        ' "$VERSIONS_FILE"
    else
        # Plugin in a section like [mdbook-plugins]
        awk -v section="$section" -v tool="$tool" '
            BEGIN { in_section = 0 }
            $0 ~ ("^\\[" section "\\]$") { in_section = 1; next }
            in_section && $0 ~ "^\\[" { exit }
            in_section && $1 == tool && $2 == "=" { print; exit }
        ' "$VERSIONS_FILE" | sed 's/.*"\(.*\)".*/\1/'
    fi
}

echo "Reading versions from ${VERSIONS_FILE}..."

# Install mdBook
MDBOOK_VERSION=$(get_version "mdbook")
if [ -n "$MDBOOK_VERSION" ]; then
    echo "Installing mdBook ${MDBOOK_VERSION}..."
    cargo install mdbook --version "${MDBOOK_VERSION}"
else
    echo "Error: Could not find mdbook version in versions.toml"
    exit 1
fi

# Install mdBook plugins
echo ""
echo "Installing mdBook plugins..."

# Extract all plugins from [mdbook-plugins] section
while IFS= read -r line; do
    if [[ $line =~ ^([a-zA-Z0-9_-]+)[[:space:]]*=[[:space:]]*\"([^\"]+)\" ]]; then
        plugin="${BASH_REMATCH[1]}"
        version="${BASH_REMATCH[2]}"
        echo "Installing ${plugin} ${version}..."
        cargo install "${plugin}" --version "${version}"
    fi
done < <(
    awk '
        BEGIN { in_section = 0 }
        /^\[mdbook-plugins\]$/ { in_section = 1; next }
        in_section && /^\[/ { exit }
        in_section && $0 ~ /^[a-zA-Z0-9_-]+[[:space:]]*=/ { print }
    ' "$VERSIONS_FILE"
)

echo ""
echo "✓ Installation complete!"
echo ""
echo "Installed versions:"
mdbook --version
# List installed plugins
cargo install --list | grep mdbook

