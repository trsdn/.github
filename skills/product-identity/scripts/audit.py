"""Report what identity a built artifact embeds, and where it comes from.

Covers `I01` (product name and version), `I02` (repository and issue tracker
URLs), `I03` (licence identifier and copyright holder) and `I06` (the values are
produced by the build rather than typed by hand). `I04` and `I05` need the
running product and its icons, so they are reported as judgement, not decided.

Read-only. It reads manifests and release workflows in a checkout and changes
nothing.

Usage:
    python3 audit.py --path /path/to/checkout [--json]
"""

from __future__ import annotations

import argparse
import json
import pathlib
import plistlib
import sys
import xml.etree.ElementTree as ET

try:  # Python 3.11 and later
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - older interpreters
    tomllib = None  # type: ignore[assignment]

FIELDS = ("name", "version", "repository", "issues", "licence", "copyright")

# What a release workflow reads from the tag or the repository. Where a manifest
# holds a literal instead, `I06` is the criterion that notices.
DERIVED_MARKERS = (
    "github.ref_name",
    "GITHUB_REF_NAME",
    "github.repository",
    "GITHUB_REPOSITORY",
    "git describe",
    "agvtool",
    "MARKETING_VERSION=",
    "CURRENT_PROJECT_VERSION=",
)

SKIP = {".git", "node_modules", ".build", "build", "dist", ".venv", "Pods", "Carthage"}


def blank() -> dict[str, str | None]:
    return dict.fromkeys(FIELDS)


def parse_package_json(path: pathlib.Path) -> dict:
    data = json.loads(path.read_text())
    found = blank()
    found["name"] = data.get("name")
    found["version"] = data.get("version")
    repository = data.get("repository")
    if isinstance(repository, dict):
        found["repository"] = repository.get("url")
    elif isinstance(repository, str):
        found["repository"] = repository
    bugs = data.get("bugs")
    if isinstance(bugs, dict):
        found["issues"] = bugs.get("url")
    elif isinstance(bugs, str):
        found["issues"] = bugs
    found["licence"] = data.get("license")
    if isinstance(data.get("author"), str):
        found["copyright"] = data["author"]
    return found


def parse_pyproject(path: pathlib.Path) -> dict:
    found = blank()
    if tomllib is None:
        return found
    data = tomllib.loads(path.read_text())
    project = data.get("project") or {}
    found["name"] = project.get("name")
    found["version"] = project.get("version")
    urls = {key.lower(): value for key, value in (project.get("urls") or {}).items()}
    found["repository"] = urls.get("repository") or urls.get("source") or urls.get("homepage")
    found["issues"] = urls.get("issues") or urls.get("bug tracker") or urls.get("tracker")
    licence = project.get("license")
    if isinstance(licence, dict):
        found["licence"] = licence.get("text") or licence.get("file")
    elif isinstance(licence, str):
        found["licence"] = licence
    authors = project.get("authors") or []
    if authors and isinstance(authors[0], dict):
        found["copyright"] = authors[0].get("name")
    return found


def parse_csproj(path: pathlib.Path) -> dict:
    found = blank()
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError:
        return found
    values: dict[str, str] = {}
    for element in root.iter():
        tag = element.tag.split("}")[-1]
        if element.text and element.text.strip():
            values[tag] = element.text.strip()
    found["name"] = values.get("AssemblyName") or values.get("PackageId")
    found["version"] = values.get("Version") or values.get("AssemblyVersion")
    found["repository"] = values.get("RepositoryUrl")
    found["licence"] = values.get("PackageLicenseExpression") or values.get("PackageLicenseFile")
    found["copyright"] = values.get("Copyright")
    return found


def parse_plist(path: pathlib.Path) -> dict:
    found = blank()
    try:
        data = plistlib.loads(path.read_bytes())
    except Exception:  # noqa: BLE001 - a malformed plist is a finding, not a crash
        return found
    if not isinstance(data, dict):
        return found
    found["name"] = data.get("CFBundleDisplayName") or data.get("CFBundleName")
    found["version"] = data.get("CFBundleShortVersionString")
    found["copyright"] = data.get("NSHumanReadableCopyright")
    # There is no standard Info.plist key for either URL, so only an account
    # convention can be looked for. Report what is there; do not invent a key.
    for key, value in data.items():
        if not isinstance(value, str):
            continue
        lowered = key.lower()
        if "repositor" in lowered or "sourceurl" in lowered:
            found["repository"] = value
        if "issue" in lowered or "bugs" in lowered or "support" in lowered:
            found["issues"] = value
    return found


PARSERS = (
    ("package.json", parse_package_json),
    ("pyproject.toml", parse_pyproject),
    ("Info.plist", parse_plist),
)


def manifests(root: pathlib.Path) -> list[tuple[pathlib.Path, dict]]:
    """Find manifests describing a built artifact, nearest the root first."""
    results: list[tuple[pathlib.Path, dict]] = []
    for name, parser in PARSERS:
        candidates = sorted(root.rglob(name), key=lambda p: len(p.parts))
        for candidate in candidates[:4]:
            if set(candidate.parts) & SKIP:
                continue
            try:
                results.append((candidate, parser(candidate)))
            except (OSError, ValueError, json.JSONDecodeError):
                continue
    for candidate in sorted(root.rglob("*.csproj"), key=lambda p: len(p.parts))[:3]:
        if set(candidate.parts) & SKIP:
            continue
        results.append((candidate, parse_csproj(candidate)))
    return results


def workflow_derivation(root: pathlib.Path) -> list[str]:
    """Which workflows or build scripts derive identity from the tag or repository."""
    seen: list[str] = []
    places = list((root / ".github" / "workflows").glob("*.yml"))
    places += list((root / ".github" / "workflows").glob("*.yaml"))
    if (root / "scripts").is_dir():
        places += [path for path in (root / "scripts").iterdir() if path.is_file()]
    for path in places:
        try:
            text = path.read_text(errors="replace")
        except OSError:
            continue
        for marker in DERIVED_MARKERS:
            if marker in text:
                seen.append(f"{path.relative_to(root)} ({marker})")
                break
    return seen


def finding(result: str, detail: str, action: str = "") -> dict:
    return {"result": result, "detail": detail, "action": action}


def judgement_criteria() -> dict:
    return {
        "I04": finding(
            "judgement",
            "needs the running product: an About window, --version, --help, or a site footer",
            "check it shows the version and links to the repository and issue tracker",
        ),
        "I05": finding(
            "judgement",
            "needs the icons the product ships and any store or site surface",
        ),
    }


def audit(root: pathlib.Path) -> dict:
    found = manifests(root)
    if not found:
        unknown = finding(
            "unknown",
            "no manifest describing a built artifact was found",
            "if this repository builds nothing, I01-I06 are Not applicable; say what you "
            "looked for",
        )
        criteria = {identifier: unknown for identifier in ("I01", "I02", "I03", "I06")}
        criteria.update(judgement_criteria())
        return {"path": str(root), "criteria": criteria, "manifests": [], "embedded": blank()}

    merged = blank()
    for _, values in found:
        for field in FIELDS:
            if merged[field] is None and values.get(field):
                merged[field] = values[field]

    evidence = workflow_derivation(root)
    names = [str(path.relative_to(root)) for path, _ in found]

    def state(fields: tuple[str, ...], identifier: str, what: str) -> dict:
        missing = [field for field in fields if not merged[field]]
        if not missing:
            return finding("met", f"{what} embedded")
        if identifier == "I03" and missing == ["licence"]:
            copyright_text = (merged.get("copyright") or "").lower()
            named = [
                licence
                for licence in ("mit", "apache", "gpl", "bsd", "mpl", "proprietary")
                if licence in copyright_text
            ]
            if named:
                return finding(
                    "judgement",
                    f"no licence field, but the copyright string names {named[0].upper()}",
                    "decide whether that satisfies the criterion here, or add the identifier "
                    "as its own field",
                )
        if len(missing) == len(fields):
            return finding(
                "gap",
                f"neither {' nor '.join(fields)} is embedded",
                f"add {what} to {names[0]}",
            )
        return finding("gap", f"missing {', '.join(missing)}", f"add them to {names[0]}")

    criteria = {
        "I01": state(("name", "version"), "I01", "product name and version"),
        "I02": state(("repository", "issues"), "I02", "repository and issue tracker URLs"),
        "I03": state(("licence", "copyright"), "I03", "licence identifier and copyright holder"),
        "I06": finding("met", "derived by the build: " + "; ".join(evidence[:3]))
        if evidence
        else finding(
            "gap",
            "no workflow or build script derives the version or repository from the tag",
            "derive it at build time; a hand-typed version is the one that goes stale",
        ),
    }
    criteria.update(judgement_criteria())
    return {"path": str(root), "criteria": criteria, "manifests": names, "embedded": merged}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", type=pathlib.Path, default=pathlib.Path("."))
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()

    root = arguments.path.resolve()
    if not root.is_dir():
        print(f"identity: {root} is not a directory", file=sys.stderr)
        return 1

    report = audit(root)
    if arguments.json:
        print(json.dumps(report, indent=2, default=str))
        return 0

    if report["manifests"]:
        print("manifests: " + ", ".join(report["manifests"]))
        for field in FIELDS:
            value = (report["embedded"] or {}).get(field)
            print(f"  {field:11s} {value if value else '—'}")
        print()

    order = {"gap": 0, "judgement": 1, "unknown": 2, "met": 3}
    for identifier, entry in sorted(
        report["criteria"].items(), key=lambda kv: (order[kv[1]["result"]], kv[0])
    ):
        print(f"{identifier}  {entry['result'].upper():10s} {entry['detail']}")
        if entry["action"]:
            print(f"     → {entry['action']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
