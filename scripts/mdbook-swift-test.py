#!/usr/bin/env python3
"""
mdbook-swift-test: An mdbook backend that tests Swift code examples.

This backend extracts Swift code blocks from mdbook chapters and verifies
they compile using `swiftc -typecheck`.

Usage:
    Configured in book.toml as:
    
    [output.swift-test]
    command = "python3 scripts/mdbook-swift-test.py"

Code Block Attributes:
    ```swift,ignore          - Skip this block (incomplete/illustrative)

Placeholder Bodies:
    The pattern `{ ... }` is automatically replaced with `{ fatalError() }`
    before compilation. This allows documentation to show elided implementations
    while still compiling:
    
        func doSomething() -> Int { ... }
    
    Compiles as:
    
        func doSomething() -> Int { fatalError() }

Hidden Lines (mdbook-style):
    Lines starting with `# ` are included in compilation but can be used
    to provide context (imports, type definitions, etc.) that readers
    don't need to see in the rendered book.
    
    Example:
        ```swift
        # import Foundation
        # struct Point { var x: Int; var y: Int }
        let p = Point(x: 1, y: 2)
        print(p)
        ```
    
    The `# ` prefix is stripped before compilation, so all lines are
    compiled together.

Note: Unlike Rust code blocks, mdbook does not automatically hide `# `
lines for Swift. If you want them hidden in the rendered output, you'll
need a preprocessor or keep the context minimal.
"""

import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CodeBlock:
    """A Swift code block extracted from a markdown chapter."""
    content: str
    line_number: int
    chapter_name: str
    chapter_path: str
    ignore: bool = False


def parse_attributes(info_string: str) -> dict:
    """
    Parse code block attributes from the info string.
    
    Examples:
        "swift" -> {"lang": "swift", "ignore": False}
        "swift,ignore" -> {"lang": "swift", "ignore": True}
    """
    attrs = {"lang": None, "ignore": False}
    
    if not info_string:
        return attrs
    
    parts = info_string.split(",")
    if parts:
        attrs["lang"] = parts[0].strip().lower()
    
    for part in parts[1:]:
        part = part.strip()
        if part == "ignore":
            attrs["ignore"] = True
    
    return attrs


def process_hidden_lines(content: str) -> str:
    """
    Process hidden lines in the mdbook style.
    
    Lines starting with `# ` have the prefix stripped.
    Lines that are exactly `#` become empty lines.
    All other lines are kept as-is.
    
    This allows authors to include setup code (imports, type definitions)
    that is compiled but could be hidden from readers.
    """
    processed_lines = []
    for line in content.split("\n"):
        if line.startswith("# "):
            # Strip the `# ` prefix
            processed_lines.append(line[2:])
        elif line == "#":
            # A lone `#` becomes an empty line
            processed_lines.append("")
        else:
            # Keep the line as-is
            processed_lines.append(line)
    return "\n".join(processed_lines)


def replace_placeholder_bodies(content: str) -> str:
    """
    Replace placeholder function bodies with fatalError().
    
    This allows authors to write `{ ... }` in documentation to indicate
    an elided implementation, while still allowing the code to compile.
    
    Patterns replaced:
        { ... }  ->  { fatalError() }
        {...}    ->  { fatalError() }
    """
    # Replace `{ ... }` (with optional whitespace) with `{ fatalError() }`
    content = re.sub(r'\{\s*\.\.\.\s*\}', '{ fatalError() }', content)
    return content


def extract_code_blocks(content: str, chapter_name: str, chapter_path: str) -> list[CodeBlock]:
    """
    Extract all Swift code blocks from markdown content.
    
    Handles fenced code blocks with ``` markers.
    """
    blocks = []
    lines = content.split("\n")
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check for code fence start
        if line.strip().startswith("```"):
            fence_match = re.match(r'^(\s*)```(\S*)', line)
            if fence_match:
                indent = fence_match.group(1)
                info_string = fence_match.group(2)
                attrs = parse_attributes(info_string)
                
                if attrs["lang"] == "swift":
                    # Found a Swift block, collect its content
                    start_line = i + 1  # 1-indexed for human readability
                    code_lines = []
                    i += 1
                    
                    # Find the closing fence
                    while i < len(lines):
                        if lines[i].strip() == "```":
                            break
                        code_lines.append(lines[i])
                        i += 1
                    
                    block = CodeBlock(
                        content="\n".join(code_lines),
                        line_number=start_line,
                        chapter_name=chapter_name,
                        chapter_path=chapter_path,
                        ignore=attrs["ignore"],
                    )
                    blocks.append(block)
        i += 1
    
    return blocks


def compile_swift(source: str, block: CodeBlock) -> tuple[bool, str]:
    """
    Compile Swift source using swiftc -typecheck.
    
    Returns (success, error_message).
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".swift", delete=False) as f:
        f.write(source)
        temp_path = f.name
    
    try:
        result = subprocess.run(
            ["swiftc", "-typecheck", temp_path],
            capture_output=True,
            text=True,
            timeout=30,
        )
        
        if result.returncode == 0:
            return True, ""
        else:
            # Combine stderr and stdout for error output
            error = result.stderr or result.stdout or "Unknown compilation error"
            return False, error
    except FileNotFoundError:
        return False, "swiftc not found in PATH"
    except subprocess.TimeoutExpired:
        return False, "Compilation timed out (30s)"
    finally:
        try:
            os.unlink(temp_path)
        except OSError:
            pass


def process_book(book_data: dict) -> tuple[int, int, list[str]]:
    """
    Process all chapters in the book and test Swift code blocks.
    
    Returns (passed_count, failed_count, error_messages).
    """
    all_blocks: list[CodeBlock] = []
    errors: list[str] = []
    
    def process_item(item: dict):
        """Recursively process book items."""
        if "Chapter" in item:
            chapter = item["Chapter"]
            name = chapter.get("name", "Unknown")
            path = chapter.get("path") or "unknown.md"
            content = chapter.get("content", "")
            
            # Extract blocks from this chapter
            blocks = extract_code_blocks(content, name, path)
            all_blocks.extend(blocks)
            
            # Process nested items (sub-chapters)
            for sub_item in chapter.get("sub_items", []):
                process_item(sub_item)
    
    # Process all sections
    sections = book_data.get("sections", [])
    for section in sections:
        process_item(section)
    
    # Now test all non-ignored blocks
    passed = 0
    failed = 0
    
    for block in all_blocks:
        if block.ignore:
            continue
        
        # Skip empty blocks
        if not block.content.strip():
            continue
        
        # Process hidden lines and placeholder bodies, then compile
        source = process_hidden_lines(block.content)
        source = replace_placeholder_bodies(source)
        
        # Skip if the processed source is empty (all hidden lines)
        if not source.strip():
            continue
        
        success, error = compile_swift(source, block)
        
        if success:
            passed += 1
        else:
            failed += 1
            location = f"{block.chapter_path}:{block.line_number}"
            errors.append(f"FAIL: {location}\n{error}")
    
    return passed, failed, errors


def main():
    # Handle the "supports" check from mdbook
    if len(sys.argv) > 1:
        if sys.argv[1] == "supports":
            # We support all renderers (we're a validation backend)
            sys.exit(0)
    
    # Read the render context from stdin
    try:
        context = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON from stdin: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Extract the book data
    book = context.get("book", {})
    config = context.get("config", {})
    
    # Get configuration options
    swift_test_config = config.get("output", {}).get("swift-test", {})
    verbose = swift_test_config.get("verbose", False)
    
    print("=" * 60, file=sys.stderr)
    print("Swift Code Example Testing", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    
    # Process the book
    passed, failed, errors = process_book(book)
    
    # Report results
    total = passed + failed
    if total == 0:
        print("No Swift code blocks found to test.", file=sys.stderr)
        sys.exit(0)
    
    print(f"\nResults: {passed} passed, {failed} failed, {total} total", file=sys.stderr)
    
    if errors:
        print("\n" + "-" * 60, file=sys.stderr)
        print("FAILURES:", file=sys.stderr)
        print("-" * 60, file=sys.stderr)
        for error in errors:
            print(f"\n{error}", file=sys.stderr)
    
    print("=" * 60, file=sys.stderr)
    
    # Exit with appropriate code
    if failed > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
