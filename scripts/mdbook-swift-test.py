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
    supported-platforms = ["linux", "darwin", "win32"]   # optional; sys.platform values to run on

Do not run this script directly in a terminal: mdbook pipes JSON into stdin.
Use `mdbook build` from the book directory (or `mdbook-swift-test.py --help`).

Debugging (see what mdBook sent):
    Set MDBOOK_SWIFT_TEST_DUMP_CONTEXT to a file path, then run `mdbook build`.
    The full renderer context JSON is written there; search for "content" or ```swift.
"""

import json
import os
import re
import shutil
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
    # mdBook may pass CRLF on Windows; the fence regex only matches LF after ```info.
    if "\r" in content:
        content = content.replace("\r\n", "\n").replace("\r", "\n")
    for m in CODE_BLOCK.finditer(content):
        attrs = Attributes.parse(m.group(1))
        if attrs.language == "swift":
            start_line = content[: m.start()].count("\n") + 2
            yield CodeBlock(m.group(2).rstrip("\n\r"), start_line, path, attrs)


def _book_roots(book: dict) -> list:
    """Top-level spine entries: mdBook 0.5+ uses `items`, older versions use `sections`."""
    return book.get("items") or book.get("sections", [])


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
    unhidden = "\n".join(unhide_line(line) for line in code.splitlines())
    return re.sub(r"\{\s*\.\.\.\s*\}", "{ fatalError() }", unhidden)


def line(char: str, count: int = 60) -> str:
    """A line of characters."""
    return char * count


def _usage_stderr() -> None:
    print(
        "mdbook-swift-test.py is an mdbook backend: it reads the book JSON from stdin.\n"
        "Run from the book directory:\n"
        "  mdbook build\n"
        "mdbook will invoke this command when [output.swift-test] is set in book.toml.\n"
        "On Windows, use the same `command` as in book.toml (e.g. python path\\to\\mdbook-swift-test.py).",
        file=sys.stderr,
    )


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print(__doc__.strip(), file=sys.stderr)
        sys.exit(0)

    # Interactive terminal has no piped JSON; json.load would block until EOF (Ctrl+C).
    if sys.stdin.isatty():
        _usage_stderr()
        sys.exit(2)

    context = json.load(sys.stdin)

    dump_path = os.environ.get("MDBOOK_SWIFT_TEST_DUMP_CONTEXT", "").strip()
    if dump_path:
        # ensure_ascii=True so lone surrogates from mdBook/Rust still serialize (UTF-8 cannot store them).
        with open(dump_path, "w", encoding="utf-8") as df:
            json.dump(context, df, indent=2, ensure_ascii=True)
        print(
            f"Wrote mdBook renderer context to {dump_path!r} "
            "(MDBOOK_SWIFT_TEST_DUMP_CONTEXT)",
            file=sys.stderr,
        )

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

    # CI and many dev machines have no Swift on Windows; skip instead of failing every block.
    if sys.platform == "win32" and not shutil.which("swiftc"):
        print(
            "Skipping Swift code example tests (swiftc not on PATH; install Swift for Windows to enable)",
            file=sys.stderr,
        )
        sys.exit(0)

    book = context.get("book", {})
    blocks = list(
        chain.from_iterable(extract_from_chapter(s) for s in _book_roots(book))
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
