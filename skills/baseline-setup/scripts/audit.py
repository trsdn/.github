"""Report which Baseline criteria a repository already meets, and which it does not.

Read-only. It changes nothing, and it decides nothing that needs judgement: where
a criterion turns on whether a sentence says the right thing, this reports what it
found and leaves the reading to the agent that called it.

Usage:
    python3 audit.py --repo OWNER/NAME [--path .] [--json]

`--repo` is read through `gh`, so the GitHub half needs an authenticated session.
`--path` is the local checkout, for the half that lives in files. Either half may
be skipped: without `--repo` the metadata checks report `unknown`, and without a
readable checkout so do the file checks.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import shutil
import subprocess
import sys

MANIFESTS = (
    "package.json",
    "pyproject.toml",
    "requirements.txt",
    "Package.swift",
    "go.mod",
    "Cargo.toml",
    "Gemfile",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
)

# Patterns whose absence from .gitignore is worth reporting. This is not a secret
# scanner: `S05` owns that. It reports only what a starting .gitignore usually has.
IGNORE_HINTS = (".env", "*.log", "node_modules", "__pycache__", ".DS_Store", "dist", "build")

SECRET_LOOKALIKES = (".env", ".env.local", "secrets.json", "credentials.json", "id_rsa")


def gh(*arguments: str) -> tuple[int, str]:
    """Run a gh command, returning its exit code and stdout."""
    if not shutil.which("gh"):
        return 127, ""
    result = subprocess.run(["gh", *arguments], capture_output=True, text=True, check=False)
    return result.returncode, result.stdout.strip()


def metadata(repo: str) -> dict | None:
    code, out = gh(
        "repo",
        "view",
        repo,
        "--json",
        "name,description,homepageUrl,repositoryTopics,visibility,isArchived,"
        "licenseInfo,defaultBranchRef",
    )
    if code != 0 or not out:
        return None
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return None


def read(root: pathlib.Path, *names: str) -> tuple[str, str] | None:
    """Return the first of `names` that exists, as (name, text)."""
    for name in names:
        candidate = root / name
        if candidate.is_file():
            try:
                return name, candidate.read_text(errors="replace")
            except OSError:
                continue
    return None


def tracked(root: pathlib.Path) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files"], capture_output=True, text=True, check=False
    )
    return result.stdout.splitlines() if result.returncode == 0 else []


def finding(result: str, detail: str, action: str = "") -> dict:
    return {"result": result, "detail": detail, "action": action}


def check_b01(meta: dict | None) -> dict:
    if meta is None:
        return finding("unknown", "repository metadata was not readable")
    description = (meta.get("description") or "").strip()
    if not description:
        return finding(
            "gap",
            "the repository has no description",
            "write one sentence saying what this is for, then apply.py --description",
        )
    if len(description) < 15:
        return finding(
            "judgement",
            f"description is very short: {description!r}",
            "decide whether it states the purpose; replace it if it does not",
        )
    return finding("met", f"description: {description!r}")


def check_b02(root: pathlib.Path) -> dict:
    found = read(root, "README.md", "README.rst", "README.txt")
    if not found:
        return finding("gap", "no README", "write one covering the five parts B02 names")
    name, text = found
    parts = {
        "purpose": any(w in text.lower() for w in ("what it", "purpose", "this is", "provides")),
        "audience": any(w in text.lower() for w in ("for ", "audience", "who ")),
        "status": any(
            w in text.lower() for w in ("status", "experimental", "maintained", "archived", "beta")
        ),
        "setup or usage": any(
            w in text.lower() for w in ("install", "usage", "getting started", "run ", "build")
        ),
        "key links": "](" in text,
    }
    missing = [key for key, present in parts.items() if not present]
    if missing:
        return finding(
            "judgement",
            f"{name} may not cover: {', '.join(missing)} (searched for the usual wording)",
            "read it and decide; these are word matches, not an assessment",
        )
    return finding("judgement", f"{name} appears to cover all five parts", "confirm by reading it")


def check_b03(root: pathlib.Path, meta: dict | None) -> dict:
    if read(root, "LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"):
        return finding("met", "a licence file is present")
    licence = (meta or {}).get("licenseInfo") or {}
    if licence.get("name"):
        return finding("met", f"GitHub reports the licence as {licence['name']}")
    readme = read(root, "README.md")
    if readme and "licen" in readme[1].lower():
        return finding("judgement", "no licence file, but the README mentions licensing")
    return finding(
        "gap",
        "no licence file and no licensing statement",
        "add a LICENSE, or state in the README that it is internal-use only",
    )


def check_b04(root: pathlib.Path) -> dict:
    found = read(root, ".gitignore")
    files = tracked(root)
    committed = sorted(path for path in files if pathlib.PurePath(path).name in SECRET_LOOKALIKES)
    if committed:
        return finding(
            "gap",
            f"these look like committed secrets or local state: {', '.join(committed)}",
            "stop and tell the operator. Do not delete or rotate anything yourself",
        )
    if not found:
        return finding("gap", "no .gitignore", "add one for this ecosystem")
    missing = [hint for hint in IGNORE_HINTS if hint not in found[1]]
    if missing:
        return finding(
            "judgement",
            f".gitignore does not mention: {', '.join(missing)}",
            "add only the ones this repository's ecosystem actually produces",
        )
    return finding("met", ".gitignore covers the usual local state")


def check_b06(repo: str, meta: dict | None, root: pathlib.Path) -> dict:
    stated = False
    for name in ("CONTRIBUTING.md", "AGENTS.md", "README.md"):
        found = read(root, name)
        if found and any(
            phrase in found[1].lower()
            for phrase in ("pull request", "merge", "review", "branch protection")
        ):
            stated = True
            break
    code, out = gh("api", f"repos/{repo}/dependabot/alerts?state=open&per_page=1")
    if code == 0:
        try:
            alerts = "open alerts exist" if json.loads(out) else "no open alerts"
        except json.JSONDecodeError:
            alerts = "alert API returned something unreadable"
    else:
        alerts = "alert API was not readable (often off, or not available here)"
    if not stated:
        return finding(
            "gap",
            f"no merge policy found in CONTRIBUTING, AGENTS.md or README; {alerts}",
            "state how changes reach the default branch, in one sentence",
        )
    return finding("judgement", f"a merge policy appears to be stated; {alerts}")


def check_b07(root: pathlib.Path) -> dict:
    present = [name for name in MANIFESTS if (root / name).is_file()]
    if present:
        return finding("met", f"manifest present: {', '.join(present)}")
    readme = read(root, "README.md")
    if readme and any(word in readme[1].lower() for word in ("requires", "python 3", "node ")):
        return finding("judgement", "no manifest, but the README mentions a runtime")
    return finding(
        "judgement",
        "no dependency manifest found",
        "if this repository has no dependencies, B07 is Not applicable; say so in the evidence",
    )


def check_b08(root: pathlib.Path) -> dict:
    if read(root, "CHANGELOG.md", "CHANGES.md", "HISTORY.md"):
        return finding("met", "a changelog is present")
    if (root / "docs" / "decisions").is_dir():
        return finding("met", "docs/decisions/ records decisions")
    return finding(
        "judgement",
        "no changelog and no decision records",
        "releases or linked issues also satisfy B08; check before adding a file",
    )


def check_b09(meta: dict | None, root: pathlib.Path) -> dict:
    if meta is None:
        return finding("unknown", "repository metadata was not readable")
    topics = [
        entry.get("name") or entry.get("topic", {}).get("name", "")
        for entry in meta.get("repositoryTopics") or []
    ]
    topics = [topic for topic in topics if topic]
    gaps = []
    if not topics:
        gaps.append("no topics")
    if not (meta.get("homepageUrl") or "").strip():
        gaps.append("no homepage")
    if gaps:
        return finding(
            "gap",
            ", ".join(gaps),
            "apply.py --topics ... --homepage ... once you have read the README",
        )
    return finding(
        "judgement",
        f"topics {topics}, homepage {meta.get('homepageUrl')}",
        "confirm they agree with what the README says",
    )


def check_b10(root: pathlib.Path) -> dict:
    if read(root, "CODEOWNERS", ".github/CODEOWNERS", "docs/CODEOWNERS"):
        return finding("met", "CODEOWNERS is present")
    for name in ("README.md", "CONTRIBUTING.md", "AGENTS.md"):
        found = read(root, name)
        if found and any(
            word in found[1].lower()
            for word in ("maintainer", "maintained by", "unmaintained", "owner")
        ):
            return finding("judgement", f"{name} mentions ownership or maintenance status")
    return finding(
        "gap",
        "no CODEOWNERS and no ownership or maintenance statement",
        "one line in the README saying who maintains it and whether it is active",
    )


def audit(repo: str, root: pathlib.Path) -> dict:
    meta = metadata(repo) if repo else None
    return {
        "repository": repo,
        "path": str(root),
        "criteria": {
            "B01": check_b01(meta),
            "B02": check_b02(root),
            "B03": check_b03(root, meta),
            "B04": check_b04(root),
            "B06": check_b06(repo, meta, root) if repo else finding("unknown", "no --repo given"),
            "B07": check_b07(root),
            "B08": check_b08(root),
            "B09": check_b09(meta, root),
            "B10": check_b10(root),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default="", help="OWNER/NAME, read through gh")
    parser.add_argument("--path", type=pathlib.Path, default=pathlib.Path("."))
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    arguments = parser.parse_args()

    root = arguments.path.resolve()
    if not root.is_dir():
        print(f"baseline: {root} is not a directory", file=sys.stderr)
        return 1

    report = audit(arguments.repo, root)

    if arguments.json:
        print(json.dumps(report, indent=2))
        return 0

    order = {"gap": 0, "judgement": 1, "unknown": 2, "met": 3}
    rows = sorted(report["criteria"].items(), key=lambda kv: (order[kv[1]["result"]], kv[0]))
    for identifier, entry in rows:
        print(f"{identifier}  {entry['result'].upper():10s} {entry['detail']}")
        if entry["action"]:
            print(f"     → {entry['action']}")
    counts = {name: 0 for name in order}
    for entry in report["criteria"].values():
        counts[entry["result"]] += 1
    print(
        f"\n{counts['gap']} gaps, {counts['judgement']} need your reading, "
        f"{counts['met']} met, {counts['unknown']} unreadable"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
