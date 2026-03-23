#!/usr/bin/env python3
"""
mdbook backend that verifies Swift code examples compile with `swiftc -typecheck`.

Code blocks beginning with ```swift are compiled, unless it is ignored (```swift,ignore).
In those blocks,
- lines beginning with # are hidden from readers but are compiled.
- lines beginning with \\# are shown and compiled, including the # (e.g. \\#available(...)).
- placeholder bodies `{ ... }` are replaced with `{ fatalError() }`.

Usage (book.toml):
    [output.swift-test]
    command = "python3 path/to/mdbook-swift-test.py"
    supported-platforms = ["linux", "darwin"]   # optional; sys.platform values to run on
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
class Attributes:
    """Attributes of a code block."""

    language: str | None
    ignore: bool

    @classmethod
    def parse(cls, info: str) -> "Attributes":
        """Parses a code block's attributes string (e.g. "swift,ignore")."""
        parts = [p.strip() for p in info.split(",")] if info else []
        lang = parts[0].lower() if parts and parts[0] else None
        ignore = "ignore" in parts[1:]
        return cls(lang, ignore)


@dataclass(frozen=True)
class CodeBlock:
    """A code block extracted from a markdown file."""

    content: str
    start_line: int  # 1-indexed line number in source file
    path: str
    attributes: Attributes


@dataclass(frozen=True)
class TestResult:
    """Outcome of compiling a code block."""

    ok: bool
    error: str


def unhide_line(line: str) -> str:
    """The line with hidden-line prefix stripped or literal # unescaped."""
    if line.startswith("# "):
        return line[2:]
    if line == "#":
        return ""
    if line.startswith("\\#"):
        return line[1:]
    return line


# Matches code blocks: ```info\n...content...\n```
# Groups: (1) info string e.g. "swift,ignore", (2) block content
CODE_BLOCK = re.compile(
    r"^[ \t]*```(\S*)\n(.*?)^[ \t]*```[ \t]*$", re.MULTILINE | re.DOTALL
)


def extract_blocks(content: str, path: str) -> Iterator[CodeBlock]:
    """Yields Swift code blocks from markdown content."""
    for m in CODE_BLOCK.finditer(content):
        attrs = Attributes.parse(m.group(1))
        if attrs.language == "swift":
            start_line = content[: m.start()].count("\n") + 2
            yield CodeBlock(m.group(2).rstrip("\n"), start_line, path, attrs)


def extract_from_chapter(item: dict) -> Iterator[CodeBlock]:
    """Yields code blocks from a chapter and its sub-chapters."""
    if "Chapter" not in item:
        return
    ch = item["Chapter"]
    yield from extract_blocks(ch.get("content", ""), ch.get("path", "unknown.md"))
    yield from chain.from_iterable(
        extract_from_chapter(sub) for sub in ch.get("sub_items", [])
    )


def compile_swift(source: str) -> TestResult:
    """Type-checks source via swiftc."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".swift", delete=False) as f:
        f.write(source)
        path = f.name
    try:
        subprocess.run(
            ["swiftc", "-typecheck", path],
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except FileNotFoundError:
        return TestResult(False, "swiftc not found")
    except subprocess.TimeoutExpired:
        return TestResult(False, "Timeout (30s)")
    except subprocess.CalledProcessError as e:
        return TestResult(False, e.stderr or e.stdout or "Unknown error")
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass
    return TestResult(True, "")


def prepare_source(code: str) -> str:
    """A code block's source code with hidden lines revealed and placeholder bodies expanded."""
    unhidden = "\n".join(unhide_line(line) for line in code.split("\n"))
    return re.sub(r"\{\s*\.\.\.\s*\}", "{ fatalError() }", unhidden)


def line(char: str, count: int = 60) -> str:
    """A line of characters."""
    return char * count


def main():
    context = json.load(sys.stdin)
    cfg = (
        context.get("config", {})
        .get("output", {})
        .get("swift-test", {})
    )
    platforms = [str(p).strip() for p in cfg.get("supported-platforms", [])]
    if platforms and sys.platform not in platforms:
        print(
            f"Skipping Swift code example tests ({sys.platform!r} not in supported-platforms)",
            file=sys.stderr,
        )
        sys.exit(0)

    book = context.get("book", {})
    blocks = list(
        chain.from_iterable(extract_from_chapter(s) for s in book.get("sections", []))
    )

    results = [
        (block, compile_swift(prepare_source(block.content)))
        for block in blocks
        if not block.attributes.ignore
    ]
    tested = [(block, result) for block, result in results]
    failed = [(block, result) for block, result in tested if not result.ok]

    print(line("="), file=sys.stderr)
    print("Swift Code Example Testing", file=sys.stderr)
    print(line("="), file=sys.stderr)
    print(
        f"\nResults: {len(tested) - len(failed)} passed, {len(failed)} failed, {len(tested)} total",
        file=sys.stderr,
    )

    if failed:
        print("\n" + line("-"), file=sys.stderr)
        print("FAILURES:", file=sys.stderr)
        print(line("-"), file=sys.stderr)
        for block, result in failed:
            print(
                f"\nFAIL: {block.path}:{block.start_line}\n{result.error}",
                file=sys.stderr,
            )

    print(line("="), file=sys.stderr)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
