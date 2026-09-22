"""Check localization catalogs for missing and orphaned keys.

This is the validation command `L04` asks for: it exits non-zero when a catalog
is incomplete, so it can be the documented check a repository runs, by hand or
in CI.

It understands the catalogs these repositories actually use:

- `.xcstrings` string catalogs, including the translation state Xcode records
- `.lproj/*.strings` files, compared against the development-language directory
- locale JSON files under `locales/`, `i18n/`, or `lang/`

Usage:
    python3 catalog-check.py --path /path/to/checkout [--locales de,en] [--json]

Without `--locales` it checks every locale each catalog already contains, so it
reports drift without being told what to expect. With `--locales` it also reports
a declared locale the catalog does not carry at all, which is the `L03` claim
and the `L04` reality disagreeing.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

SKIP_DIRS = {".git", "node_modules", ".build", "build", "dist", ".venv", "Pods", "DerivedData"}

STRINGS_ENTRY = re.compile(r'^\s*"((?:[^"\\]|\\.)*)"\s*=\s*"((?:[^"\\]|\\.)*)"\s*;', re.M)

# States Xcode records for a translation that is present but not finished.
UNFINISHED = {"new", "needs_review", "stale"}


def walk(root: pathlib.Path, pattern: str) -> list[pathlib.Path]:
    return [p for p in root.rglob(pattern) if not (set(p.parts) & SKIP_DIRS)]


def check_xcstrings(path: pathlib.Path) -> dict:
    data = json.loads(path.read_text())
    source = data.get("sourceLanguage") or "en"
    strings = data.get("strings") or {}
    locales: set[str] = set()
    for entry in strings.values():
        locales |= set((entry.get("localizations") or {}).keys())

    missing: dict[str, list[str]] = {locale: [] for locale in locales}
    unfinished: dict[str, list[str]] = {locale: [] for locale in locales}
    stale: list[str] = []

    for key, entry in strings.items():
        if entry.get("extractionState") == "stale":
            stale.append(key)
        localizations = entry.get("localizations") or {}
        for locale in locales:
            unit = (localizations.get(locale) or {}).get("stringUnit") or {}
            if not unit:
                # A variation-based entry (plurals, device) stores units deeper.
                if localizations.get(locale):
                    continue
                missing[locale].append(key)
            elif unit.get("state") in UNFINISHED:
                unfinished[locale].append(key)

    return {
        "catalog": str(path),
        "kind": "xcstrings",
        "source_language": source,
        "locales": sorted(locales),
        "total": len(strings),
        "missing": {k: v for k, v in missing.items() if v},
        "unfinished": {k: v for k, v in unfinished.items() if v},
        "orphaned": stale,
    }


def check_lproj(root: pathlib.Path) -> list[dict]:
    groups: dict[pathlib.Path, dict[str, set[str]]] = {}
    for path in walk(root, "*.lproj"):
        if not path.is_dir():
            continue
        locale = path.name.removesuffix(".lproj")
        for table in path.glob("*.strings"):
            try:
                keys = {match.group(1) for match in STRINGS_ENTRY.finditer(table.read_text())}
            except OSError:
                continue
            groups.setdefault(path.parent / table.name, {})[locale] = keys

    reports: list[dict] = []
    for table, by_locale in groups.items():
        base = "Base" if "Base" in by_locale else ("en" if "en" in by_locale else None)
        if base is None or len(by_locale) < 2:
            continue
        reference = by_locale[base]
        missing = {
            locale: sorted(reference - keys)
            for locale, keys in by_locale.items()
            if locale != base and reference - keys
        }
        orphaned = sorted(
            {
                key
                for locale, keys in by_locale.items()
                if locale != base
                for key in keys - reference
            }
        )
        reports.append(
            {
                "catalog": str(table),
                "kind": "strings",
                "source_language": base,
                "locales": sorted(by_locale),
                "total": len(reference),
                "missing": missing,
                "unfinished": {},
                "orphaned": orphaned,
            }
        )
    return reports


def flatten(value: object, prefix: str = "") -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if isinstance(nested, dict):
                keys |= flatten(nested, path)
            else:
                keys.add(path)
    return keys


def check_json_locales(root: pathlib.Path) -> list[dict]:
    reports: list[dict] = []
    for directory in ("locales", "i18n", "lang"):
        for folder in walk(root, directory):
            if not folder.is_dir():
                continue
            by_locale: dict[str, set[str]] = {}
            for path in sorted(folder.glob("*.json")):
                try:
                    by_locale[path.stem] = flatten(json.loads(path.read_text()))
                except (OSError, json.JSONDecodeError):
                    continue
            if len(by_locale) < 2:
                continue
            base = "en" if "en" in by_locale else sorted(by_locale)[0]
            reference = by_locale[base]
            missing = {
                locale: sorted(reference - keys)
                for locale, keys in by_locale.items()
                if locale != base and reference - keys
            }
            orphaned = sorted(
                {
                    key
                    for locale, keys in by_locale.items()
                    if locale != base
                    for key in keys - reference
                }
            )
            reports.append(
                {
                    "catalog": str(folder),
                    "kind": "json",
                    "source_language": base,
                    "locales": sorted(by_locale),
                    "total": len(reference),
                    "missing": missing,
                    "unfinished": {},
                    "orphaned": orphaned,
                }
            )
    return reports


def collect(root: pathlib.Path) -> list[dict]:
    reports: list[dict] = []
    for path in walk(root, "*.xcstrings"):
        try:
            reports.append(check_xcstrings(path))
        except (OSError, json.JSONDecodeError) as error:
            reports.append({"catalog": str(path), "kind": "xcstrings", "error": str(error)})
    reports += check_lproj(root)
    reports += check_json_locales(root)
    return reports


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", type=pathlib.Path, default=pathlib.Path("."))
    parser.add_argument("--locales", default="", help="comma-separated locales L03 declares")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()

    root = arguments.path.resolve()
    if not root.is_dir():
        print(f"localization: {root} is not a directory", file=sys.stderr)
        return 1

    declared = [locale.strip() for locale in arguments.locales.split(",") if locale.strip()]
    reports = collect(root)

    if arguments.json:
        print(json.dumps({"declared": declared, "catalogs": reports}, indent=2))
        return 0

    if not reports:
        print("localization: no string catalogs found.")
        print(
            "If the product ships one language, L03 is met by saying so in the README "
            "and L04 is Not applicable. Say what you looked for."
        )
        return 0

    incomplete = False
    for report in reports:
        if report.get("error"):
            print(f"{report['catalog']}: could not be read: {report['error']}")
            incomplete = True
            continue
        relative = report["catalog"].replace(str(root) + "/", "")
        print(
            f"{relative}  [{report['kind']}]  source {report['source_language']}, "
            f"{report['total']} strings, locales: {', '.join(report['locales']) or 'none'}"
        )
        for locale, keys in sorted(report["missing"].items()):
            incomplete = True
            print(f"  {locale}: {len(keys)} missing")
            for key in keys[:5]:
                print(f"      {key!r}")
            if len(keys) > 5:
                print(f"      … and {len(keys) - 5} more")
        for locale, keys in sorted(report["unfinished"].items()):
            incomplete = True
            print(f"  {locale}: {len(keys)} present but not finished (new, needs review, or stale)")
            for key in keys[:5]:
                print(f"      {key!r}")
        if report["orphaned"]:
            incomplete = True
            print(f"  {len(report['orphaned'])} orphaned (no longer in the source)")
            for key in report["orphaned"][:5]:
                print(f"      {key!r}")
        for locale in declared:
            if locale not in report["locales"] and locale != report["source_language"]:
                incomplete = True
                print(f"  {locale}: declared, but this catalog carries nothing for it")
        if not any((report["missing"], report["unfinished"], report["orphaned"])) and all(
            locale in report["locales"] or locale == report["source_language"]
            for locale in declared
        ):
            print("  complete")

    if incomplete:
        print("\nlocalization: catalogs are incomplete")
        return 1
    print("\nlocalization: every catalog is complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
