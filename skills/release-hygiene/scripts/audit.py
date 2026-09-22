"""Read a repository's release hygiene: metadata agreement, versioning policy, notes.

Covers `R01` (package metadata is complete and agrees with the repository's),
`R02` (the versioning and compatibility policy is documented) and `R06` (the
latest release notes describe meaningful changes and upgrade concerns).

`R06` and `R01` are assessed on the *latest published release*, as the standard
says, so this reads the release through `gh` rather than guessing from the tree.

Usage:
    python3 audit.py --repo OWNER/NAME --path /path/to/checkout [--json]
"""

from __future__ import annotations

import argparse
import json
import pathlib
import plistlib
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

try:  # Python 3.11 and later
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None  # type: ignore[assignment]

VERSIONING_MARKERS = (
    "semver",
    "semantic versioning",
    "calendar versioning",
    "calver",
    "versioning policy",
    "versioning and compatibility",
    "breaking change",
)

UPGRADE_MARKERS = (
    "breaking",
    "migrat",
    "upgrade",
    "deprecat",
    "removed",
    "no longer",
    "requires ",
    "action required",
)

AUTO_ONLY = re.compile(r"^\s*(\*\*)?full changelog(\*\*)?:?\s*https?://\S+\s*$", re.I)


def gh(*arguments: str) -> tuple[int, str]:
    if not shutil.which("gh"):
        return 127, ""
    result = subprocess.run(["gh", *arguments], capture_output=True, text=True, check=False)
    return result.returncode, result.stdout.strip()


def finding(result: str, detail: str, action: str = "", evidence: list[str] | None = None) -> dict:
    return {"result": result, "detail": detail, "action": action, "evidence": evidence or []}


def repo_metadata(repo: str) -> dict | None:
    code, out = gh("repo", "view", repo, "--json", "description,licenseInfo,url,homepageUrl")
    if code != 0 or not out:
        return None
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return None


def latest_release(repo: str) -> dict | None:
    code, out = gh("release", "view", "--repo", repo, "--json", "tagName,body,publishedAt,isDraft")
    if code != 0 or not out:
        return None
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return None


def package_metadata(root: pathlib.Path) -> tuple[str, dict]:
    """Return the manifest kind and the metadata it carries."""
    if (root / "package.json").is_file():
        data = json.loads((root / "package.json").read_text())
        repository = data.get("repository")
        url = repository.get("url") if isinstance(repository, dict) else repository
        return "package.json", {
            "description": data.get("description"),
            "licence": data.get("license"),
            "repository": url,
        }
    if (root / "pyproject.toml").is_file() and tomllib is not None:
        project = (tomllib.loads((root / "pyproject.toml").read_text()).get("project")) or {}
        urls = {k.lower(): v for k, v in (project.get("urls") or {}).items()}
        licence = project.get("license")
        if isinstance(licence, dict):
            licence = licence.get("text") or licence.get("file")
        return "pyproject.toml", {
            "description": project.get("description"),
            "licence": licence,
            "repository": urls.get("repository") or urls.get("source") or urls.get("homepage"),
        }
    csproj = sorted(root.rglob("*.csproj"))
    if csproj:
        values: dict[str, str] = {}
        try:
            for element in ET.parse(csproj[0]).getroot().iter():
                if element.text and element.text.strip():
                    values[element.tag.split("}")[-1]] = element.text.strip()
        except ET.ParseError:
            pass
        return csproj[0].name, {
            "description": values.get("Description"),
            "licence": values.get("PackageLicenseExpression"),
            "repository": values.get("RepositoryUrl"),
        }
    if (root / "Package.swift").is_file():
        # SwiftPM has no field for a licence, a description, or a repository URL,
        # so `R01` asks the artifact's own metadata instead.
        found = {"description": None, "licence": None, "repository": None}
        plists = [p for p in root.rglob("Info.plist") if ".build" not in p.parts]
        if plists:
            try:
                data = plistlib.loads(plists[0].read_bytes())
            except Exception:  # noqa: BLE001
                data = {}
            if isinstance(data, dict):
                for key, value in data.items():
                    if not isinstance(value, str):
                        continue
                    lowered = key.lower()
                    # `NSMicrophoneUsageDescription` and its siblings are consent
                    # strings shown to a user, not a description of the product.
                    if lowered.endswith("usagedescription"):
                        continue
                    if "repositor" in lowered or "sourceurl" in lowered:
                        found["repository"] = value
                    elif "licen" in lowered:
                        found["licence"] = value
                    elif "description" in lowered or lowered == "cfbundlegetinfostring":
                        found["description"] = value
        return "Package.swift (+ Info.plist)", found
    return "", {}


def normalise(url: str | None) -> str:
    if not url:
        return ""
    return (
        re.sub(r"^(git\+)?(https?://|git@)", "", url)
        .replace("github.com:", "github.com/")
        .rstrip("/")
        .removesuffix(".git")
        .lower()
    )


def divergence(left: str, right: str, width: int = 44) -> str:
    """Show where two strings first differ, rather than their identical openings."""
    index = 0
    while index < min(len(left), len(right)) and left[index] == right[index]:
        index += 1
    start = max(0, index - 12)
    lead = "…" if start else ""
    return (
        f"from character {index}:\n"
        f"        manifest   {lead}{left[start : start + width]!r}\n"
        f"        repository {lead}{right[start : start + width]!r}"
    )


def check_r01(root: pathlib.Path, meta: dict | None) -> dict:
    kind, package = package_metadata(root)
    if not kind:
        return finding(
            "unknown",
            "no package manifest was found",
            "R01 is Not applicable where the repository publishes no package; say what you "
            "looked for",
        )
    missing = [
        field for field in ("description", "licence", "repository") if not package.get(field)
    ]
    disagreements: list[str] = []
    if meta:
        repo_description = (meta.get("description") or "").strip()
        if package.get("description") and repo_description:
            if package["description"].strip().lower() != repo_description.lower():
                disagreements.append(
                    "description differs "
                    + divergence(package["description"].strip(), repo_description)
                )
        repo_url = normalise(meta.get("url"))
        if package.get("repository") and repo_url and normalise(package["repository"]) != repo_url:
            disagreements.append(
                f"repository URL: manifest {package['repository']} vs repository {meta.get('url')}"
            )
        repo_licence = ((meta.get("licenseInfo") or {}).get("key") or "").lower()
        manifest_licence = (package.get("licence") or "").lower()
        if repo_licence and manifest_licence and repo_licence not in manifest_licence:
            disagreements.append(
                f"licence: manifest {package['licence'][:40]!r} vs repository {repo_licence}"
            )
    if disagreements:
        return finding(
            "gap",
            f"{kind} disagrees with the repository's own metadata",
            "R01 asks them to agree; decide which is right and change the other",
            evidence=disagreements,
        )
    if missing:
        return finding(
            "gap",
            f"{kind} carries no {', '.join(missing)}",
            "where the manifest format has no field for it, put it in the artifact's own "
            "metadata instead",
        )
    return finding("met", f"{kind} is complete and agrees with the repository")


def check_r02(root: pathlib.Path) -> dict:
    for name in ("README.md", "CHANGELOG.md", "CONTRIBUTING.md"):
        path = root / name
        if not path.is_file():
            continue
        text = path.read_text(errors="replace").lower()
        for marker in VERSIONING_MARKERS:
            if marker in text:
                return finding(
                    "judgement",
                    f"{name} mentions {marker!r}",
                    "naming SemVer is enough on its own; another scheme needs a sentence saying "
                    "what a consumer can rely on",
                )
    for path in sorted((root / "docs").rglob("*.md")) if (root / "docs").is_dir() else []:
        text = path.read_text(errors="replace").lower()
        if any(marker in text for marker in VERSIONING_MARKERS):
            return finding("judgement", f"{path.relative_to(root)} mentions a versioning scheme")
    return finding(
        "gap",
        "no versioning or compatibility statement found",
        "one line naming the scheme, in the README or at the head of the changelog",
    )


def check_r06(release: dict | None) -> dict:
    if release is None:
        return finding(
            "unknown",
            "no published release was readable",
            "R06 is assessed on the latest published release; a repository with none is "
            "Not applicable",
        )
    body = (release.get("body") or "").strip()
    tag = release.get("tagName", "")
    if not body:
        return finding("gap", f"release {tag} has empty notes", "describe what changed and why")
    lines = [line for line in body.splitlines() if line.strip()]
    if all(AUTO_ONLY.match(line) for line in lines):
        return finding(
            "gap",
            f"release {tag} carries only an auto-generated changelog link",
            "a link to a commit list is not a description of what changed",
        )
    if len(body) < 60:
        return finding(
            "judgement",
            f"release {tag} notes are {len(body)} characters",
            "short is fine for a small release; check it names what changed",
            evidence=[body[:120]],
        )
    upgrade = [marker for marker in UPGRADE_MARKERS if marker in body.lower()]
    if upgrade:
        return finding(
            "met",
            f"release {tag} describes changes and mentions upgrade concerns ({upgrade[0]})",
        )
    return finding(
        "judgement",
        f"release {tag} describes changes but names no upgrade concern",
        "if nothing needed action from a consumer, that is a pass; if something did, say it",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default="", help="OWNER/NAME, read through gh")
    parser.add_argument("--path", type=pathlib.Path, default=pathlib.Path("."))
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()

    root = arguments.path.resolve()
    if not root.is_dir():
        print(f"release: {root} is not a directory", file=sys.stderr)
        return 1

    meta = repo_metadata(arguments.repo) if arguments.repo else None
    release = latest_release(arguments.repo) if arguments.repo else None

    report = {
        "repository": arguments.repo,
        "criteria": {
            "R01": check_r01(root, meta),
            "R02": check_r02(root),
            "R06": check_r06(release),
        },
    }

    if arguments.json:
        print(json.dumps(report, indent=2))
        return 0

    order = {"gap": 0, "judgement": 1, "unknown": 2, "met": 3}
    for identifier, entry in sorted(
        report["criteria"].items(), key=lambda kv: (order[kv[1]["result"]], kv[0])
    ):
        print(f"{identifier}  {entry['result'].upper():10s} {entry['detail']}")
        for line in entry["evidence"]:
            print(f"      {line}")
        if entry["action"]:
            print(f"     → {entry['action']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
