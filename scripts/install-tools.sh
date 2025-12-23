#!/bin/bash
# Install mdBook and plugins using versions from ../versions.toml
# This ensures consistency between local development and CI

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERSIONS_FILE="${SCRIPT_DIR}/../versions.toml"

# Function to extract version from TOML file
get_version() {
    local tool=$1
    local section=$2
    
    if [ -z "$section" ]; then
        # Top-level tool like [mdbook]
        grep -A 1 "^\[$tool\]" "$VERSIONS_FILE" | grep "version" | sed 's/.*"\(.*\)".*/\1/'
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

