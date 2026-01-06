#!/bin/bash
# Installs mdBook and plugins using versions from versions.txt.
#
# Reads tool versions from the repository root's versions.txt file and
# installs them via cargo. This ensures consistency between local development
# and CI environments.
#
# Usage: ./install-tools.sh
#
# Preconditions:
#   - Rust and Cargo are installed and in PATH
#   - versions.txt exists in the repository root

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERSIONS_FILE="${SCRIPT_DIR}/../versions.txt"

echo "Reading versions from ${VERSIONS_FILE}..."

# Install mdBook
MDBOOK_VERSION=$(grep "^mdbook=" "$VERSIONS_FILE" | cut -d'=' -f2)
if [ -n "$MDBOOK_VERSION" ]; then
    echo "Installing mdBook ${MDBOOK_VERSION}..."
    cargo install mdbook --version "${MDBOOK_VERSION}"
else
    echo "Error: Could not find mdbook version in versions.txt"
    exit 1
fi

# Install mdBook plugins
echo ""
echo "Installing mdBook plugins..."

# Process all lines starting with "mdbook-" (plugins)
while IFS='=' read -r plugin version; do
    echo "Installing ${plugin} ${version}..."
    cargo install "${plugin}" --version "${version}"
done < <(grep "^mdbook-" "$VERSIONS_FILE")

echo ""
echo "✓ Installation complete!"
echo ""
echo "Installed versions:"
mdbook --version
# List installed plugins
cargo install --list | grep mdbook

