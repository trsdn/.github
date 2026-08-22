#!/usr/bin/env python3
"""Generate and validate the machine-readable criteria catalog.

The Markdown standard is written by hand; `standard.yml` is derived from it.
Running this script with `--check` fails when the two disagree, when criterion
identifiers are malformed or duplicated, when a prefix is used without being
claimed in the prefix register, or when the declared version does not match the
changelog.

Usage:
    python3 scripts/standard.py            # regenerate standard.yml
    python3 scripts/standard.py --check    # verify, exit non-zero on drift
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
STANDARD_MD = ROOT / "docs" / "repository-quality-standard.md"
CATALOG = ROOT / "standard.yml"
CHANGELOG = ROOT / "CHANGELOG.md"

CRITERION_ROW = re.compile(
    r'^\| <a id="(?P<anchor>[a-z]\d{2})"></a>(?P<id>[A-Z]\d{2}) \| '
    r"(?P<requirement>.+?) \| (?P<evidence>.+?) \|\s*$"
)
HEADING = re.compile(r"^(#{2,3}) (.+?)\s*$")
VERSION_LINE = re.compile(r"^- Version: (?P<version>\d+\.\d+\.\d+)\s*$", re.M)
REVIEWED_LINE = re.compile(r"^- Last reviewed: (?P<date>\d{4}-\d{2}-\d{2})\s*$", re.M)
PREFIX_ROW = re.compile(r"^\| ([A-Z]) \| (.+?) \|\s*$", re.M)
CHANGELOG_HEADING = re.compile(r"^## (?P<version>\d+\.\d+\.\d+) - ", re.M)


def fail(message: str) -> None:
    print(f"standard: {message}", file=sys.stderr)


def escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def group_by_prefix(criteria: list[dict]) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = {}
    for criterion in criteria:
        grouped.setdefault(criterion["id"][0], []).append(criterion["id"])
    return grouped


def parse() -> tuple[dict, list[str]]:
    text = STANDARD_MD.read_text()
    errors: list[str] = []

    version_match = VERSION_LINE.search(text)
    reviewed_match = REVIEWED_LINE.search(text)
    if not version_match:
        errors.append("no `- Version: X.Y.Z` line found")
    if not reviewed_match:
        errors.append("no `- Last reviewed: YYYY-MM-DD` line found")

    register_parts = text.split("### Prefix Register", 1)
    claimed: dict[str, str] = {}
    if len(register_parts) == 2:
        block = register_parts[1].split("\n### ", 1)[0].split("\n## ", 1)[0]
        for prefix, section in PREFIX_ROW.findall(block):
            claimed[prefix] = section.strip()
    else:
        errors.append("prefix register section is missing")

    criteria: list[dict] = []
    seen: dict[str, int] = {}
    section = ""
    for number, line in enumerate(text.splitlines(), start=1):
        heading = HEADING.match(line)
        if heading and heading.group(1) == "##":
            section = heading.group(2)
            continue
        row = CRITERION_ROW.match(line)
        if not row:
            continue
        identifier = row.group("id")
        if row.group("anchor") != identifier.lower():
            errors.append(
                f"line {number}: anchor `{row.group('anchor')}` does not match "
                f"identifier `{identifier}`"
            )
        if identifier in seen:
            errors.append(
                f"line {number}: identifier `{identifier}` already defined on "
                f"line {seen[identifier]}"
            )
        seen[identifier] = number
        prefix = identifier[0]
        if prefix not in claimed:
            errors.append(
                f"line {number}: prefix `{prefix}` is not claimed in the prefix "
                "register"
            )
        criteria.append(
            {
                "id": identifier,
                "section": section,
                "requirement": row.group("requirement").strip(),
                "evidence": row.group("evidence").strip(),
            }
        )

    for prefix, identifiers in group_by_prefix(criteria).items():
        numbers = sorted(int(i[1:]) for i in identifiers)
        if numbers != list(range(1, len(numbers) + 1)):
            errors.append(
                f"prefix `{prefix}` is not contiguous from 01: found {numbers}"
            )

    document_version = version_match.group("version") if version_match else "0.0.0"
    changelog_match = CHANGELOG_HEADING.search(CHANGELOG.read_text())
    if not changelog_match:
        errors.append("changelog has no versioned heading")
    elif changelog_match.group("version") != document_version:
        errors.append(
            f"document version `{document_version}` does not match latest "
            f"changelog entry `{changelog_match.group('version')}`"
        )

    catalog = {
        "version": document_version,
        "last_reviewed": reviewed_match.group("date") if reviewed_match else "",
        "prefixes": claimed,
        "criteria": criteria,
    }
    return catalog, errors


def render(catalog: dict) -> str:
    lines = [
        "# Machine-readable catalog of the Repository Quality Standard.",
        "#",
        "# Generated by scripts/standard.py from",
        "# docs/repository-quality-standard.md. Do not edit by hand.",
        "",
        f'version: "{catalog["version"]}"',
        f'last_reviewed: "{catalog["last_reviewed"]}"',
        "",
        "prefixes:",
    ]
    for prefix, section in sorted(catalog["prefixes"].items()):
        lines.append(f'  {prefix}: "{escape(section)}"')
    lines.append("")
    lines.append("criteria:")
    for criterion in catalog["criteria"]:
        lines.append(f'  - id: "{criterion["id"]}"')
        lines.append(f'    section: "{escape(criterion["section"])}"')
        lines.append(f'    requirement: "{escape(criterion["requirement"])}"')
        lines.append(f'    evidence: "{escape(criterion["evidence"])}"')
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()

    catalog, errors = parse()
    rendered = render(catalog)

    if arguments.check:
        if not CATALOG.exists():
            errors.append("standard.yml is missing; run scripts/standard.py")
        elif CATALOG.read_text() != rendered:
            errors.append(
                "standard.yml is out of date; run scripts/standard.py and "
                "commit the result"
            )
        for error in errors:
            fail(error)
        if errors:
            return 1
        print(f"standard: {len(catalog['criteria'])} criteria, catalog in sync")
        return 0

    for error in errors:
        fail(error)
    CATALOG.write_text(rendered)
    print(f"standard: wrote {CATALOG.name} with {len(catalog['criteria'])} criteria")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
