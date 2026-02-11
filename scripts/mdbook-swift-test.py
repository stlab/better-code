#!/usr/bin/env python3
"""
mdbook backend that verifies Swift code examples compile.

Configuration (book.toml):
    [output.swift-test]
    command = "python3 scripts/mdbook-swift-test.py"

Attributes:
    ```swift,ignore    - skip compilation

Hidden lines:
    # import Foundation    - compiled but hidden from readers
    #                      - becomes empty line
    \\#available(...)      - shown as #available(...), compiled

Placeholder bodies:
    { ... }  ->  { fatalError() }
"""

import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from itertools import chain
from typing import Iterator


@dataclass(frozen=True)
class CodeBlock:
    """A Swift code block extracted from markdown."""
    content: str
    start_line: int  # 1-indexed line number in source file
    path: str
    ignore: bool = False


@dataclass(frozen=True)
class TestResult:
    """Outcome of compiling a code block."""
    ok: bool
    error: str


def parse_attributes(info: str) -> tuple[str | None, bool]:
    """The (language, ignore) pair from a code fence info string."""
    parts = [p.strip() for p in info.split(",")] if info else []
    lang = parts[0].lower() if parts and parts[0] else None
    ignore = "ignore" in parts[1:]
    return lang, ignore


def unhide_line(line: str) -> str:
    """The line with hidden-line prefix stripped or literal # unescaped."""
    if line.startswith("# "):
        return line[2:]
    if line == "#":
        return ""
    if line.startswith("\\#"):
        return line[1:]
    return line


# Matches fenced code blocks: ```info\n...content...\n```
# Groups: (1) info string e.g. "swift,ignore", (2) content between fences
FENCE = re.compile(r'^[ \t]*```(\S*)\n(.*?)^[ \t]*```[ \t]*$', re.MULTILINE | re.DOTALL)


def extract_blocks(content: str, path: str) -> Iterator[CodeBlock]:
    """Yields Swift code blocks from markdown content."""
    for m in FENCE.finditer(content):
        lang, ignore = parse_attributes(m.group(1))
        if lang == "swift":
            start_line = content[:m.start()].count('\n') + 2
            yield CodeBlock(m.group(2).rstrip('\n'), start_line, path, ignore)


def extract_from_chapter(item: dict) -> Iterator[CodeBlock]:
    """Yields code blocks from a chapter and its sub-chapters."""
    if "Chapter" not in item:
        return
    ch = item["Chapter"]
    yield from extract_blocks(ch.get("content", ""), ch.get("path", "unknown.md"))
    yield from chain.from_iterable(extract_from_chapter(sub) for sub in ch.get("sub_items", []))


def compile_swift(source: str) -> TestResult:
    """Type-checks source via swiftc."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".swift", delete=False) as f:
        f.write(source)
        path = f.name
    try:
        r = subprocess.run(["swiftc", "-typecheck", path], capture_output=True, text=True, timeout=30)
        if r.returncode == 0:
            return TestResult(True, "")
        return TestResult(False, r.stderr or r.stdout or "Unknown error")
    except FileNotFoundError:
        return TestResult(False, "swiftc not found")
    except subprocess.TimeoutExpired:
        return TestResult(False, "Timeout (30s)")
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


def prepare_source(content: str) -> str:
    """The content with hidden lines revealed and placeholder bodies expanded."""
    processed = "\n".join(unhide_line(line) for line in content.split("\n"))
    return re.sub(r'\{\s*\.\.\.\s*\}', '{ fatalError() }', processed)


def test_block(block: CodeBlock) -> TestResult | None:
    """Compiles block; returns None if skipped or content is empty."""
    if block.ignore or not block.content.strip():
        return None
    source = prepare_source(block.content)
    if not source.strip():
        return None
    return compile_swift(source)


def line(char: str, count: int = 60) -> str:
    """A line of characters."""
    return char * count


def main():
    context = json.load(sys.stdin)
    book = context.get("book", {})
    blocks = list(chain.from_iterable(extract_from_chapter(s) for s in book.get("sections", [])))

    results = [(block, test_block(block)) for block in blocks]
    tested = [(block, result) for block, result in results if result is not None]
    failed = [(block, result) for block, result in tested if not result.ok]

    print(line("="), file=sys.stderr)
    print("Swift Code Example Testing", file=sys.stderr)
    print(line("="), file=sys.stderr)
    print(f"\nResults: {len(tested) - len(failed)} passed, {len(failed)} failed, {len(tested)} total", file=sys.stderr)

    if failed:
        print("\n" + line("-"), file=sys.stderr)
        print("FAILURES:", file=sys.stderr)
        print(line("-"), file=sys.stderr)
        for block, result in failed:
            print(f"\nFAIL: {block.path}:{block.start_line}\n{result.error}", file=sys.stderr)

    print(line("="), file=sys.stderr)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
