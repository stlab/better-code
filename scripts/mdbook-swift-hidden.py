#!/usr/bin/env python3
"""
mdbook-swift-hidden: A preprocessor that hides `# ` lines in Swift code blocks.

This preprocessor strips lines starting with `# ` from Swift code blocks
when rendering for HTML output, mimicking mdbook's behavior for Rust.

For the swift-test backend, lines are passed through unchanged so the
test backend can compile the full code including hidden setup.

Usage:
    Configured in book.toml as:
    
    [preprocessor.swift-hidden]
    command = "python3 scripts/mdbook-swift-hidden.py"

Hidden Line Syntax:
    Lines starting with `# ` (hash + space) are hidden from readers.
    A line that is just `#` becomes a blank line (for spacing).
    
    Example input:
        ```swift
        # import Foundation
        # struct Point { var x: Int; var y: Int }
        let p = Point(x: 1, y: 2)
        print(p)
        ```
    
    Rendered output (for HTML):
        ```swift
        let p = Point(x: 1, y: 2)
        print(p)
        ```
"""

import json
import re
import sys


def strip_hidden_lines(content: str) -> str:
    """
    Remove hidden lines from Swift code blocks.
    
    Lines starting with `# ` are removed entirely.
    Lines that are exactly `#` are also removed.
    """
    result_lines = []
    in_swift_block = False
    
    for line in content.split("\n"):
        # Check for Swift code fence start
        if re.match(r'^(\s*)```swift', line):
            in_swift_block = True
            result_lines.append(line)
            continue
        
        # Check for code fence end
        if in_swift_block and line.strip() == "```":
            in_swift_block = False
            result_lines.append(line)
            continue
        
        # Process lines inside Swift blocks
        if in_swift_block:
            # Skip lines starting with `# ` or exactly `#`
            stripped = line.lstrip()
            if stripped.startswith("# ") or stripped == "#":
                continue
            result_lines.append(line)
        else:
            result_lines.append(line)
    
    return "\n".join(result_lines)


def process_book(book: dict) -> dict:
    """Process all chapters in the book, stripping hidden lines."""
    
    def process_item(item: dict) -> dict:
        """Recursively process book items."""
        if "Chapter" in item:
            chapter = item["Chapter"]
            if "content" in chapter:
                chapter["content"] = strip_hidden_lines(chapter["content"])
            
            # Process nested items (sub-chapters)
            if "sub_items" in chapter:
                chapter["sub_items"] = [process_item(sub) for sub in chapter["sub_items"]]
        
        return item
    
    # Process all sections
    if "sections" in book:
        book["sections"] = [process_item(section) for section in book["sections"]]
    
    return book


def main():
    # Handle the "supports" check from mdbook
    if len(sys.argv) > 2 and sys.argv[1] == "supports":
        renderer = sys.argv[2]
        # We support all renderers, but only modify content for html
        sys.exit(0)
    
    # Read the preprocessor context and book from stdin
    # mdbook sends [context, book] as a JSON array
    try:
        context, book = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON from stdin: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: Expected [context, book] array: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Check which renderer we're preprocessing for
    renderer = context.get("renderer", "")
    
    # Only strip hidden lines for HTML output
    # For swift-test, we want to keep the hidden lines for compilation
    if renderer == "html":
        book = process_book(book)
    
    # Output the (possibly modified) book as JSON
    json.dump(book, sys.stdout)


if __name__ == "__main__":
    main()
