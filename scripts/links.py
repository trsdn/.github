"""Validate internal Markdown links across the repository.

External links are deliberately out of scope. Checking them needs the network,
fails for reasons that have nothing to do with this repository, and would make
the check unreliable enough to be ignored. Internal links are fully decidable
from the checkout, so a failure here is always a real defect.

Anchors matter more than they look. This repository publishes a standard whose
criteria are cited from other repositories as `#s05` and similar. A heading that
is renamed silently breaks every one of those citations, and nothing else in the
toolchain would notice.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SKIP_DIRECTORIES = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    "node_modules",
    "out",
}

FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
INLINE_LINK = re.compile(
    r"\[(?:[^\[\]]|\[[^\[\]]*\])*\]\(\s*<?([^)\s>]+)>?(?:\s+[\"'][^\"']*[\"'])?\s*\)"
)
REFERENCE_DEFINITION = re.compile(r"^\s{0,3}\[([^\]]+)\]:\s*<?([^\s>]+)>?")
HTML_TARGET = re.compile(r"(?:href|src|srcset)\s*=\s*[\"']([^\"']+)[\"']", re.IGNORECASE)
EXPLICIT_ANCHOR = re.compile(r"<a\s+[^>]*\bid\s*=\s*[\"']([^\"']+)[\"']", re.IGNORECASE)
EXTERNAL = re.compile(r"^(?:[a-z][a-z0-9+.\-]*:|//|#!)", re.IGNORECASE)

MARKDOWN_LINK_TEXT = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")
HTML_TAG = re.compile(r"<[^>]+>")
EMPHASIS = re.compile(r"[`*_~]")


def slug(text: str) -> str:
    """Approximate GitHub's heading slug algorithm.

    GitHub lowercases, drops punctuation, and joins words with hyphens. The
    approximation is deliberate: it is close enough to catch renamed headings
    and simple enough to reason about without a Markdown parser.
    """
    text = HTML_TAG.sub("", text)
    text = MARKDOWN_LINK_TEXT.sub(r"\1", text)
    text = EMPHASIS.sub("", text)
    kept = [c for c in text.strip().lower() if c.isalnum() or c in "-_ "]
    return "".join(kept).replace(" ", "-")


def strip_code_fences(lines: list[str]) -> list[tuple[int, str]]:
    """Return numbered lines outside fenced code blocks.

    Documentation in this repository shows example Markdown that points at paths
    which do not exist here, because they exist in the repository the example is
    written for. Treating those as links would make the check cry wolf.
    """
    result: list[tuple[int, str]] = []
    fence: str | None = None
    for number, line in enumerate(lines, start=1):
        match = FENCE.match(line)
        if match:
            marker = match.group(1)[0]
            if fence is None:
                fence = marker
            elif fence == marker:
                fence = None
            continue
        if fence is None:
            result.append((number, line))
    return result


def anchors_of(lines: list[str]) -> set[str]:
    """Collect every anchor a link may legitimately target in one document."""
    found: set[str] = set()
    seen: dict[str, int] = {}
    for _, line in strip_code_fences(lines):
        for identifier in EXPLICIT_ANCHOR.findall(line):
            found.add(identifier.lower())
        heading = HEADING.match(line)
        if not heading:
            continue
        base = slug(heading.group(2))
        if not base:
            continue
        count = seen.get(base, 0)
        seen[base] = count + 1
        found.add(base if count == 0 else f"{base}-{count}")
    return found


def targets_of(lines: list[str]) -> list[tuple[int, str]]:
    """Collect every internal link target, with the line it appears on."""
    found: list[tuple[int, str]] = []
    for number, line in strip_code_fences(lines):
        candidates = list(INLINE_LINK.findall(line)) + list(HTML_TARGET.findall(line))
        definition = REFERENCE_DEFINITION.match(line)
        if definition:
            candidates.append(definition.group(2))
        for target in candidates:
            target = target.strip()
            if not target or EXTERNAL.match(target):
                continue
            found.append((number, target))
    return found


def markdown_files(repository: Path) -> list[Path]:
    files = []
    for path in sorted(repository.rglob("*.md")):
        if any(part in SKIP_DIRECTORIES for part in path.relative_to(repository).parts):
            continue
        files.append(path)
    return files


def check(repository: Path) -> list[str]:
    files = markdown_files(repository)
    contents = {path: path.read_text(encoding="utf-8").splitlines() for path in files}
    anchors = {path: anchors_of(lines) for path, lines in contents.items()}

    problems: list[str] = []
    for path, lines in contents.items():
        where = path.relative_to(repository)
        for number, target in targets_of(lines):
            document, _, fragment = target.partition("#")
            if document:
                resolved = (
                    repository / document.lstrip("/")
                    if document.startswith("/")
                    else (path.parent / document)
                ).resolve()
                if not resolved.exists():
                    problems.append(f"{where}:{number}: link target does not exist: {target}")
                    continue
            else:
                resolved = path

            if not fragment:
                continue
            if resolved.suffix != ".md":
                continue
            if resolved not in anchors:
                if resolved.is_file():
                    anchors[resolved] = anchors_of(
                        resolved.read_text(encoding="utf-8").splitlines()
                    )
                else:
                    continue
            if fragment.lower() not in anchors[resolved]:
                problems.append(
                    f"{where}:{number}: anchor not found in {document or where}: #{fragment}"
                )
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repository",
        default=".",
        help="Repository root to check. Defaults to the working directory.",
    )
    arguments = parser.parse_args(argv)
    repository = Path(arguments.repository).resolve()

    problems = check(repository)
    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        print(f"{len(problems)} broken internal link(s)", file=sys.stderr)
        return 1

    total = len(markdown_files(repository))
    print(f"internal links resolve across {total} Markdown files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
