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


def profile(repo: str) -> dict | None:
    code, out = gh("api", f"repos/{repo}/community/profile")
    if code != 0 or not out:
        return None
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return None


def inherited(owner: str) -> set[str]:
    """Which community files the account's .github repository publishes.

    A public repository inherits these where it ships none of its own, and the
    community profile does not report inherited issue forms, so asking the
    account directly is the only way to tell an inherited template from a
    missing one.
    """
    code, out = gh("api", f"repos/{owner}/.github/contents/.github")
    names: set[str] = set()
    if code == 0 and out:
        try:
            names |= {entry["name"].lower() for entry in json.loads(out)}
        except (json.JSONDecodeError, KeyError, TypeError):
            pass
    code, out = gh("api", f"repos/{owner}/.github/contents/")
    if code == 0 and out:
        try:
            names |= {entry["name"].lower() for entry in json.loads(out)}
        except (json.JSONDecodeError, KeyError, TypeError):
            pass
    return names


def check_p01(root: pathlib.Path, meta: dict | None) -> dict:
    licence = (meta or {}).get("licenseInfo") or {}
    # `gh repo view --json licenseInfo` returns key/name/nickname, not an SPDX id.
    key = (licence.get("key") or "").lower()
    name = licence.get("name") or ""
    if key and key not in ("other", "noassertion"):
        return finding("met", f"GitHub detects {name or key}")
    if read(root, "LICENSE", "LICENSE.md"):
        return finding(
            "judgement",
            f"a licence file exists but GitHub reports {name or key or 'nothing'}",
            "GitHub only detects an unmodified licence text; check it was not edited",
        )
    return finding(
        "gap",
        "no OSI-approved licence GitHub can detect",
        "ask the maintainer which licence, then add the unmodified text as LICENSE",
    )


def check_p02(root: pathlib.Path, account: set[str]) -> dict:
    own = [
        name
        for name in ("CONTRIBUTING.md", "CODE_OF_CONDUCT.md")
        if read(root, name, f".github/{name}")
    ]
    from_account = [
        name
        for name in ("contributing.md", "code_of_conduct.md")
        if name in account and name.upper().replace(".MD", ".md") not in own
    ]
    if len(own) == 2:
        return finding("met", "both files are in the repository")
    if own or from_account:
        return finding(
            "met",
            f"own: {own or 'none'}; inherited from the account: {from_account or 'none'}",
        )
    return finding("gap", "neither file is present nor inherited", "inherit them from the account")


def check_p04(root: pathlib.Path, account: set[str]) -> dict:
    own_issue = (root / ".github" / "ISSUE_TEMPLATE").is_dir()
    own_pr = bool(
        read(root, ".github/pull_request_template.md", ".github/PULL_REQUEST_TEMPLATE.md")
    )
    issue = own_issue or "issue_template" in account
    pull = own_pr or "pull_request_template.md" in account
    if issue and pull:
        return finding(
            "met",
            f"issue intake {'own' if own_issue else 'inherited'}, "
            f"pull-request intake {'own' if own_pr else 'inherited'}",
        )
    missing = [
        label
        for label, present in (("issue templates", issue), ("a PR template", pull))
        if not present
    ]
    return finding("gap", f"no {' and no '.join(missing)}", "inherit them from the account")


def check_p05(root: pathlib.Path) -> dict:
    found = read(root, "README.md")
    if not found:
        return finding("gap", "no README", "write one covering the six topics P05 names")
    text = found[1].lower()
    topics = {
        "install": ("install", "download", "brew ", "pip install", "npm i"),
        "configuration": ("config", "settings", "environment variable"),
        "examples": ("example", "usage", "```"),
        "compatibility": ("requires", "macos", "python 3", "node ", "supported"),
        "security": ("security", "secret", "permission", "sandbox"),
        "support status": ("status", "maintained", "experimental", "support"),
    }
    missing = [name for name, words in topics.items() if not any(w in text for w in words)]
    if missing:
        return finding(
            "judgement",
            f"README may not cover: {', '.join(missing)}",
            "one sentence or one link each is enough; read it before adding anything",
        )
    return finding("judgement", "README appears to cover all six", "confirm by reading it")


def check_p06(repo: str, community: dict | None, account: set[str]) -> dict:
    if community is None:
        return finding("unknown", "the community profile was not readable")
    files = community.get("files") or {}
    recognised = [
        name for name in ("readme", "license", "contributing", "code_of_conduct") if files.get(name)
    ]
    missing = [
        name
        for name in ("readme", "license", "contributing", "code_of_conduct")
        if not files.get(name)
    ]
    note = ""
    if not files.get("issue_template") and "issue_template" in account:
        note = (
            " (the profile reports no issue template, but the account publishes forms "
            "this repository inherits; the API does not report inherited forms)"
        )
    if missing:
        return finding(
            "gap",
            f"the community profile does not recognise: {', '.join(missing)}{note}",
            "a file GitHub does not recognise is usually in the wrong place or misnamed",
        )
    return finding("met", f"the profile recognises {', '.join(recognised)}{note}")


def check_p07(meta: dict | None, root: pathlib.Path) -> dict:
    if meta is None:
        return finding("unknown", "repository metadata was not readable")
    description = (meta.get("description") or "").strip()
    topics = [
        entry.get("name") or entry.get("topic", {}).get("name", "")
        for entry in meta.get("repositoryTopics") or []
    ]
    homepage = (meta.get("homepageUrl") or "").strip()
    gaps = []
    if not description:
        gaps.append("no description")
    if not [t for t in topics if t]:
        gaps.append("no topic")
    if gaps:
        return finding("gap", ", ".join(gaps), "apply.py --description ... --topics ...")
    has_site = (root / "docs").is_dir() or (root / "site").is_dir()
    if has_site and not homepage:
        return finding(
            "gap",
            "the repository looks like it publishes a site but names no homepage",
            "apply.py --homepage ... once you know the published URL",
        )
    return finding("met", f"description, {len(topics)} topics, homepage {homepage or 'not set'}")


def audit(repo: str, root: pathlib.Path, public: bool) -> dict:
    meta = metadata(repo) if repo else None
    criteria = {
        "B01": check_b01(meta),
        "B02": check_b02(root),
        "B03": check_b03(root, meta),
        "B04": check_b04(root),
        "B06": check_b06(repo, meta, root) if repo else finding("unknown", "no --repo given"),
        "B07": check_b07(root),
        "B08": check_b08(root),
        "B09": check_b09(meta, root),
        "B10": check_b10(root),
    }

    visibility = (meta or {}).get("visibility", "")
    is_public = public or visibility.upper() == "PUBLIC"
    if is_public and repo:
        owner = repo.split("/")[0]
        account = inherited(owner)
        community = profile(repo)
        criteria.update(
            {
                "P01": check_p01(root, meta),
                "P02": check_p02(root, account),
                "P04": check_p04(root, account),
                "P05": check_p05(root),
                "P06": check_p06(repo, community, account),
                "P07": check_p07(meta, root),
            }
        )
    elif is_public:
        for identifier in ("P01", "P02", "P04", "P05", "P06", "P07"):
            criteria[identifier] = finding("unknown", "the public checks need --repo")

    return {
        "repository": repo,
        "path": str(root),
        "public": is_public,
        "criteria": criteria,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default="", help="OWNER/NAME, read through gh")
    parser.add_argument("--path", type=pathlib.Path, default=pathlib.Path("."))
    parser.add_argument(
        "--public",
        action="store_true",
        help="also check the Public criteria; implied when gh reports the repository public",
    )
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    arguments = parser.parse_args()

    root = arguments.path.resolve()
    if not root.is_dir():
        print(f"repo-setup: {root} is not a directory", file=sys.stderr)
        return 1

    report = audit(arguments.repo, root, arguments.public)

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
