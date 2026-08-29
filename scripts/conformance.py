#!/usr/bin/env python3
"""Validate a conformance record and render its badge.

The record at `.github/conformance.yml` is the source of truth for a
repository's assessment result. The badge is generated from it, so the two
cannot disagree and no badge value is editable on its own.

A record older than the review cadence renders as stale rather than as its last
known result. Because the badge is committed, time passing eventually turns the
check red. That is intentional: a red check means reassessment is due.

Usage:
    python3 scripts/conformance.py            # write the badge
    python3 scripts/conformance.py --check    # verify, exit non-zero on drift
"""

from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_RECORD = pathlib.Path(".github/conformance.yml")
DEFAULT_BADGE = pathlib.Path(".github/badges/conformance.svg")
DEFAULT_CATALOG = pathlib.Path("standard.yml")

STALE_AFTER_DAYS = 183

RESULTS = {"pass", "partial", "fail", "na", "unknown"}
STATES = {
    "Healthy": "#2ea043",
    "Needs work": "#bf8700",
    "At risk": "#d1242f",
    "Archive candidate": "#6e7781",
    "Archived": "#6e7781",
}
STALE_COLOUR = "#8250df"

SCALAR = re.compile(r'^(?P<key>[a-z_]+):\s*"?(?P<value>[^"]*)"?\s*$')
ENTRY = re.compile(r'^  (?P<key>[A-Z]\d{2}):\s*"?(?P<value>[a-z]+)"?\s*$')
CATALOG_ID = re.compile(r'^  - id: "([A-Z]\d{2})"\s*$', re.M)
CATALOG_VERSION = re.compile(r'^version: "(?P<version>[^"]+)"\s*$', re.M)


def fail(message: str) -> None:
    print(f"conformance: {message}", file=sys.stderr)


def parse_record(text: str) -> tuple[dict, dict[str, str], list[str]]:
    """Parse the restricted record shape without a YAML dependency."""
    scalars: dict[str, str] = {}
    criteria: dict[str, str] = {}
    errors: list[str] = []
    in_criteria = False

    for number, raw in enumerate(text.splitlines(), start=1):
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line == "criteria:":
            in_criteria = True
            continue
        if in_criteria and line.startswith("  "):
            entry = ENTRY.match(line)
            if not entry:
                errors.append(f"line {number}: cannot parse criterion entry")
                continue
            criteria[entry.group("key")] = entry.group("value")
            continue
        in_criteria = False
        scalar = SCALAR.match(line)
        if not scalar:
            errors.append(f"line {number}: cannot parse `{line.strip()}`")
            continue
        scalars[scalar.group("key")] = scalar.group("value")

    return scalars, criteria, errors


def validate(
    scalars: dict, criteria: dict[str, str], catalog: pathlib.Path
) -> tuple[list[str], bool]:
    errors: list[str] = []

    for field in ("standard_version", "assessed_on", "state", "evidence"):
        if not scalars.get(field):
            errors.append(f"required field `{field}` is missing")

    state = scalars.get("state", "")
    if state and state not in STATES:
        errors.append(f"state `{state}` is not a defined state")

    assessed_on = scalars.get("assessed_on", "")
    stale = False
    if assessed_on:
        try:
            assessed = dt.date.fromisoformat(assessed_on)
        except ValueError:
            errors.append(f"assessed_on `{assessed_on}` is not an ISO date")
        else:
            age = (dt.date.today() - assessed).days
            if age < 0:
                errors.append("assessed_on is in the future")
            stale = age > STALE_AFTER_DAYS

    catalog_text = catalog.read_text()
    catalog_ids = set(CATALOG_ID.findall(catalog_text))
    catalog_version_match = CATALOG_VERSION.search(catalog_text)
    catalog_version = catalog_version_match.group("version") if catalog_version_match else ""

    if scalars.get("standard_version") != catalog_version:
        errors.append(
            f"record assesses standard `{scalars.get('standard_version')}` but the "
            f"catalog in this repository is `{catalog_version}`; reassess or pin "
            "the record to a published tag of that version"
        )

    for identifier, result in sorted(criteria.items()):
        if result not in RESULTS:
            errors.append(f"{identifier}: `{result}` is not a defined result")
        if identifier not in catalog_ids:
            errors.append(f"{identifier} is not a criterion in the catalog")

    for missing in sorted(catalog_ids - set(criteria)):
        errors.append(f"{missing} is missing from the record")

    if state == "Healthy" and "fail" in criteria.values():
        failed = sorted(i for i, r in criteria.items() if r == "fail")
        errors.append(
            "state `Healthy` is not consistent with failing criteria: " + ", ".join(failed)
        )

    return errors, stale


def render(scalars: dict, stale: bool) -> str:
    state = scalars["state"]
    version = scalars["standard_version"]
    label = "trsdn standard"
    if stale:
        value = f"v{version} - stale"
        colour = STALE_COLOUR
    else:
        value = f"v{version} - {state}"
        colour = STATES[state]

    label_width = 7 * len(label) + 16
    value_width = 7 * len(value) + 16
    total = label_width + value_width

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{total}" height="20" \
role="img" aria-label="{label}: {value}">
  <title>{label}: {value}</title>
  <rect width="{label_width}" height="20" rx="3" fill="#24292f"/>
  <rect x="{label_width}" width="{value_width}" height="20" rx="3" fill="{colour}"/>
  <rect x="{label_width}" width="4" height="20" fill="{colour}"/>
  <g fill="#ffffff" font-family="DejaVu Sans,Verdana,sans-serif" font-size="11">
    <text x="{label_width / 2}" y="14" text-anchor="middle">{label}</text>
    <text x="{label_width + value_width / 2}" y="14" text-anchor="middle">\
{value}</text>
  </g>
</svg>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--repository",
        type=pathlib.Path,
        default=ROOT,
        help="repository to assess; defaults to the one holding this script",
    )
    parser.add_argument(
        "--catalog",
        type=pathlib.Path,
        help="criteria catalog to validate against; defaults to the repository's own standard.yml",
    )
    arguments = parser.parse_args()

    repository = arguments.repository.resolve()
    record_path = repository / DEFAULT_RECORD
    badge_path = repository / DEFAULT_BADGE
    catalog_path = (
        arguments.catalog.resolve() if arguments.catalog else repository / DEFAULT_CATALOG
    )

    if not catalog_path.exists():
        fail(f"no criteria catalog at {catalog_path}")
        return 1

    if not record_path.exists():
        if badge_path.exists():
            fail("no conformance record exists, so no badge may be published")
            return 1
        print("conformance: no record, no badge")
        return 0

    scalars, criteria, errors = parse_record(record_path.read_text())
    if not errors:
        validation_errors, stale = validate(scalars, criteria, catalog_path)
        errors.extend(validation_errors)
    else:
        stale = False

    if errors:
        for error in errors:
            fail(error)
        return 1

    rendered = render(scalars, stale)
    summary = {result: list(criteria.values()).count(result) for result in RESULTS}
    summary_text = ", ".join(f"{k}={v}" for k, v in sorted(summary.items()) if v)

    if arguments.check:
        if not badge_path.exists():
            fail("badge is missing; run scripts/conformance.py")
            return 1
        problems: list[str] = []
        if badge_path.read_text() != rendered:
            problems.append(
                "badge does not match the record; run scripts/conformance.py and commit the result"
            )
        if stale:
            problems.append(
                f"the record was assessed on {scalars['assessed_on']}, which is "
                f"older than the review cadence of {STALE_AFTER_DAYS} days; "
                "reassess the repository and update the record"
            )
        for problem in problems:
            fail(problem)
        if problems:
            return 1
        print(f"conformance: {scalars['state']} ({summary_text}), badge in sync")
        return 0

    badge_path.parent.mkdir(parents=True, exist_ok=True)
    badge_path.write_text(rendered)
    print(f"conformance: wrote badge for {scalars['state']} ({summary_text})")
    if stale:
        fail(
            "the badge now renders as stale, but regenerating it does not refresh "
            "the assessment; --check stays red until the repository is reassessed"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
