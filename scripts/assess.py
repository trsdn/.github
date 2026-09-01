#!/usr/bin/env python3
"""Draft a conformance record for a repository from evidence a script can read.

The backlog this exists for is arithmetic: `B12` makes the assessed set
discoverable, and the difference between that set and the account is the work
outstanding. Transcribing a hundred records by hand is what keeps that number
from moving.

What this script will and will not claim is the whole design. A script can prove
that something is absent. It cannot judge whether a README explains the purpose,
whether tests cover failure paths, or whether an issue form collects enough to
triage. So it decides only the criteria that are settled by a fact it can read —
a topic, a licence, a `permissions` block, an action reference — and leaves
every other criterion `unknown`, which is not a result and is rejected by
`conformance.py --check` until a person replaces it.

The draft keeps the `YYYY-MM-DD` placeholder in `assessed_on` for the same
reason. A record is produced by a person looking at a repository, and a
generated file must not be able to pass for one. The draft removes the
transcription, not the assessment.

Collection is separated from decision so that the decisions are testable without
a network: `--save-facts` writes what was read, and `--facts` decides from a
saved file.

Usage:
    python3 scripts/assess.py --repo trsdn/agent-trestle
    python3 scripts/assess.py --repo trsdn/agent-trestle --out drafts/
    python3 scripts/assess.py --repo trsdn/agent-trestle --save-facts facts.json
    python3 scripts/assess.py --facts facts.json
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import re
import subprocess
import sys
import urllib.error
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import conformance  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_CATALOG = pathlib.Path("standard.yml")

API = "https://api.github.com"
TOPIC = "trsdn-standard"

# Licences GitHub reports that the Open Source Initiative approves. GitHub's own
# `license.spdx_id` is the input, so this list only has to cover what it emits
# for the repositories being assessed; anything else is left undecided rather
# than guessed at.
OSI_APPROVED = {
    "AGPL-3.0",
    "Apache-2.0",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "BSL-1.0",
    "EPL-2.0",
    "GPL-2.0",
    "GPL-3.0",
    "ISC",
    "LGPL-2.1",
    "LGPL-3.0",
    "MIT",
    "MPL-2.0",
    "Unlicense",
    "Zlib",
}

WORKFLOW = re.compile(r"^\.github/workflows/[^/]+\.ya?ml$")
ISSUE_FORM = re.compile(r"^\.github/ISSUE_TEMPLATE/[^/]+\.(ya?ml|md)$")
PR_TEMPLATE = re.compile(
    r"^(\.github/|docs/)?(pull_request_template\.md|PULL_REQUEST_TEMPLATE\.md)$"
)
USES = re.compile(r"^\s*(?:-\s*)?uses:\s*['\"]?([^'\"\s#]+)", re.M)
PERMISSIONS = re.compile(r"^\s*permissions:", re.M)
SHA = re.compile(r"^[0-9a-f]{40}$")
UNTRUSTED_TRIGGER = re.compile(r"^\s*(pull_request_target|workflow_run)\s*:", re.M)
SECRET_USE = re.compile(r"secrets\.([A-Za-z_][A-Za-z0-9_]*)")

UNDECIDED = "unknown"


def note(message: str) -> None:
    print(f"assess: {message}", file=sys.stderr)


# --------------------------------------------------------------------------
# Collection
# --------------------------------------------------------------------------


def token() -> str | None:
    """Find a token without requiring one to be exported by hand."""
    for name in ("GH_TOKEN", "GITHUB_TOKEN"):
        value = os.environ.get(name)
        if value:
            return value
    try:
        result = subprocess.run(
            ["gh", "auth", "token"], capture_output=True, text=True, check=False
        )
    except OSError:
        return None
    return result.stdout.strip() or None


class GitHub:
    """The smallest client that answers the questions below."""

    def __init__(self, auth: str | None) -> None:
        self.auth = auth

    def _get(self, path: str, accept: str) -> tuple[int, bytes]:
        request = urllib.request.Request(f"{API}{path}")
        request.add_header("Accept", accept)
        request.add_header("User-Agent", "trsdn-standard-assessor")
        if self.auth:
            request.add_header("Authorization", f"Bearer {self.auth}")
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return response.status, response.read()
        except urllib.error.HTTPError as error:
            return error.code, b""
        except urllib.error.URLError as error:
            raise SystemExit(f"assess: cannot reach the GitHub API: {error.reason}") from error

    def json(self, path: str) -> tuple[int, object]:
        status, body = self._get(path, "application/vnd.github+json")
        if status != 200 or not body:
            return status, None
        return status, json.loads(body)

    def text(self, path: str) -> str | None:
        status, body = self._get(path, "application/vnd.github.raw")
        if status != 200:
            return None
        return body.decode("utf-8", errors="replace")


def required_checks_from_rulesets(client: GitHub, repository: str) -> dict:
    """Read required checks from rulesets, which have replaced branch protection.

    A repository can require checks through either mechanism, and increasingly
    does so through rulesets alone. Reading only branch protection reports a
    protected branch as unprotected, which is the worst kind of wrong answer: a
    confident one. `readable` separates "no ruleset requires a check" from "the
    rulesets could not be read", so that the second stays undecided.
    """
    status, rulesets = client.json(f"/repos/{repository}/rulesets?includes_parents=true")
    if status != 200 or not isinstance(rulesets, list):
        return {"readable": False, "checks": []}

    checks: set[str] = set()
    for summary in rulesets:
        if not isinstance(summary, dict) or summary.get("target") != "branch":
            continue
        if summary.get("enforcement") != "active":
            continue
        detail_status, detail = client.json(f"/repos/{repository}/rulesets/{summary.get('id')}")
        if detail_status != 200 or not isinstance(detail, dict):
            continue
        for rule in detail.get("rules") or []:
            if not isinstance(rule, dict) or rule.get("type") != "required_status_checks":
                continue
            parameters = rule.get("parameters") or {}
            for entry in parameters.get("required_status_checks") or []:
                context = (entry or {}).get("context")
                if context:
                    checks.add(context)
    return {"readable": True, "checks": sorted(checks)}


def collect(client: GitHub, repository: str) -> dict:
    """Read every fact the decisions below depend on, and nothing else."""
    status, meta = client.json(f"/repos/{repository}")
    if status == 404:
        raise SystemExit(f"assess: {repository} was not found, or the token cannot see it")
    if not isinstance(meta, dict):
        raise SystemExit(f"assess: unexpected response for {repository} (HTTP {status})")

    branch = meta.get("default_branch") or "main"
    _, profile = client.json(f"/repos/{repository}/community/profile")
    _, tree = client.json(f"/repos/{repository}/git/trees/{branch}?recursive=1")

    paths: list[str] = []
    if isinstance(tree, dict):
        paths = [item["path"] for item in tree.get("tree", []) if item.get("type") == "blob"]

    contents: dict[str, str] = {}
    for path in paths:
        if WORKFLOW.match(path) or ISSUE_FORM.match(path) or PR_TEMPLATE.match(path):
            body = client.text(f"/repos/{repository}/contents/{path}?ref={branch}")
            if body is not None:
                contents[path] = body

    protection_status, protection = client.json(f"/repos/{repository}/branches/{branch}/protection")
    ruleset_checks = required_checks_from_rulesets(client, repository)
    reporting_status, reporting = client.json(
        f"/repos/{repository}/private-vulnerability-reporting"
    )

    owner = repository.split("/")[0]
    inherited_policy = False
    if not bool(meta.get("private")):
        for path in ("SECURITY.md", ".github/SECURITY.md", "docs/SECURITY.md"):
            found, _ = client.json(f"/repos/{owner}/.github/contents/{path}")
            if found == 200:
                inherited_policy = True
                break

    licence = meta.get("license") or {}
    analysis = meta.get("security_and_analysis") or {}
    files = (profile or {}).get("files") or {} if isinstance(profile, dict) else {}

    return {
        "repository": repository,
        "collected_on": dt.date.today().isoformat(),
        "owner": repository.split("/")[0],
        "private": bool(meta.get("private")),
        "archived": bool(meta.get("archived")),
        "description": meta.get("description") or "",
        "homepage": meta.get("homepage") or "",
        "topics": meta.get("topics") or [],
        "default_branch": branch,
        "licence": licence.get("spdx_id") or "",
        "truncated_tree": bool(tree.get("truncated")) if isinstance(tree, dict) else False,
        "paths": paths,
        "contents": contents,
        "community_files": {key: bool(value) for key, value in files.items()},
        "secret_scanning": (analysis.get("secret_scanning") or {}).get("status", ""),
        "inherited_security_policy": inherited_policy,
        "private_reporting": (
            ""
            if reporting_status != 200 or not isinstance(reporting, dict)
            else ("enabled" if reporting.get("enabled") else "disabled")
        ),
        "ruleset_checks": ruleset_checks,
        "protection": {
            "visible": protection_status == 200,
            "required_checks": sorted(
                ((protection or {}).get("required_status_checks") or {}).get("contexts", [])
            )
            if isinstance(protection, dict)
            else [],
        },
    }


# --------------------------------------------------------------------------
# Decision
# --------------------------------------------------------------------------


def workflows(facts: dict) -> dict[str, str]:
    return {path: body for path, body in facts["contents"].items() if WORKFLOW.match(path)}


def reference_is_pinned(reference: str, owner: str) -> bool:
    """Apply the `S12` table: the required form depends on who controls the target."""
    if reference.startswith("./") or reference.startswith("docker://"):
        return True
    name, _, version = reference.partition("@")
    account = name.split("/")[0].lower()
    if account == owner.lower():
        return True
    if account == "actions" or account == "github":
        return bool(version)
    return bool(SHA.match(version))


def decide_s11(facts: dict) -> tuple[str, str]:
    found = workflows(facts)
    if not found:
        return "na", "no workflows exist, so there is no token to scope"
    declared = [path for path, body in found.items() if PERMISSIONS.search(body)]
    if len(declared) == len(found):
        return "pass", f"all {len(found)} workflows declare `permissions`"
    if not declared:
        return "fail", f"none of the {len(found)} workflows declare `permissions`"
    missing = sorted(set(found) - set(declared))
    return (
        "partial",
        f"{len(declared)} of {len(found)} declare `permissions`; missing: " + ", ".join(missing),
    )


def decide_s12(facts: dict) -> tuple[str, str]:
    found = workflows(facts)
    if not found:
        return "na", "no workflows exist, so there is no reference to pin"
    unpinned: list[str] = []
    total = 0
    for path, body in found.items():
        for reference in USES.findall(body):
            total += 1
            if not reference_is_pinned(reference, facts["owner"]):
                unpinned.append(f"{path}: {reference}")
    if not total:
        return "na", "no workflow references an action or a reusable workflow"
    if not unpinned:
        return "pass", f"all {total} references satisfy the table"
    return "fail", f"{len(unpinned)} of {total} references can move: " + ", ".join(sorted(unpinned))


def decide_s13(facts: dict) -> tuple[str, str]:
    found = workflows(facts)
    exposed: list[str] = []
    untrusted: list[str] = []
    for path, body in found.items():
        if not UNTRUSTED_TRIGGER.search(body):
            continue
        untrusted.append(path)
        secrets = {name for name in SECRET_USE.findall(body) if name != "GITHUB_TOKEN"}
        if secrets:
            exposed.append(f"{path}: {', '.join(sorted(secrets))}")
    if not untrusted:
        return "na", "no workflow uses `pull_request_target` or `workflow_run`"
    if exposed:
        return "fail", "untrusted trigger reads repository secrets: " + ", ".join(sorted(exposed))
    return "pass", "untrusted triggers exist but read no repository secret: " + ", ".join(
        sorted(untrusted)
    )


def decide_licence(facts: dict) -> dict[str, tuple[str, str]]:
    spdx = facts["licence"]
    decided: dict[str, tuple[str, str]] = {}
    if spdx and spdx not in {"NOASSERTION", "NONE"}:
        decided["B03"] = ("pass", f"GitHub detects `{spdx}`")
        if spdx in OSI_APPROVED:
            decided["P01"] = ("pass", f"`{spdx}` is OSI approved")
        else:
            decided["P01"] = (UNDECIDED, f"`{spdx}` detected; confirm OSI approval by hand")
        return decided
    if facts["private"]:
        decided["B03"] = (UNDECIDED, "no licence file; look for an internal-use statement")
        return decided
    decided["B03"] = ("fail", "public repository with no licence GitHub can detect")
    decided["P01"] = ("fail", "no licence file")
    return decided


def decide(facts: dict, catalog_ids: list[str]) -> dict[str, tuple[str, str]]:
    """Return only the results a fact settles. Everything else stays undecided."""
    decided: dict[str, tuple[str, str]] = {}
    paths = set(facts["paths"])
    community = facts["community_files"]

    decided["B12"] = (
        ("pass", f"carries the `{TOPIC}` topic")
        if TOPIC in facts["topics"]
        else ("fail", f"the `{TOPIC}` topic is missing, so the repository is not discoverable")
    )

    record = ".github/conformance.yml"
    decided["B11"] = (
        ("pass", f"`{record}` exists")
        if record in paths
        else ("fail", f"no `{record}`, so no assessed version or date is recorded")
    )

    if not facts["description"]:
        decided["B01"] = ("fail", "the repository has no description")

    decided.update(decide_licence(facts))

    decided["G01"] = (
        ("pass", "`AGENTS.md` is at the repository root")
        if "AGENTS.md" in paths
        else ("fail", "no `AGENTS.md` at the root")
    )

    decided["S11"] = decide_s11(facts)
    decided["S12"] = decide_s12(facts)
    decided["S13"] = decide_s13(facts)

    if facts["secret_scanning"] == "enabled":
        decided["S05"] = ("pass", "secret scanning is enabled")
    elif facts["secret_scanning"] == "disabled":
        decided["S05"] = ("fail", "secret scanning is disabled")

    ruleset = facts.get("ruleset_checks") or {"readable": False, "checks": []}
    checks = sorted(set(facts["protection"]["required_checks"]) | set(ruleset["checks"]))
    if checks:
        decided["S09"] = ("pass", "required checks on the default branch: " + ", ".join(checks))
    elif facts["protection"]["visible"] and ruleset["readable"]:
        decided["S09"] = (
            "fail",
            "the default branch is protected and no ruleset or protection requires a check",
        )

    forms = [path for path in paths if ISSUE_FORM.match(path)]
    template = [path for path in paths if PR_TEMPLATE.match(path)]
    if not forms and not template:
        decided["P04"] = ("fail", "no issue template and no pull-request template")
        decided["P10"] = ("fail", "no issue template of any kind")
        decided["P11"] = ("fail", "no pull-request template")
    elif forms and template:
        decided["P04"] = ("pass", "issue and pull-request templates are present")

    if community:
        expected = ("readme", "license", "contributing", "code_of_conduct")
        missing = [name for name in expected if not community.get(name)]
        decided["P02"] = (
            ("pass", "contributing and conduct files are recognised by GitHub")
            if not {"contributing", "code_of_conduct"} & set(missing)
            else (
                "fail",
                "GitHub recognises no "
                + " or ".join(sorted({"contributing", "code_of_conduct"} & set(missing))),
            )
        )
        decided["P06"] = (
            ("pass", "GitHub recognises every community health file")
            if not missing
            else ("partial", "GitHub recognises no " + ", ".join(missing))
        )

    policy_in_tree = any(path.upper().endswith("SECURITY.MD") for path in paths)
    policy = policy_in_tree or bool(facts.get("inherited_security_policy"))
    reporting = facts.get("private_reporting", "")
    if not policy:
        decided["P03"] = (
            "fail",
            "no security policy in the repository and none inherited from the account",
        )
    elif reporting == "disabled":
        where = "the repository" if policy_in_tree else "the account"
        decided["P03"] = (
            "fail",
            f"a policy is published by {where} but private vulnerability reporting is disabled",
        )
    elif reporting == "enabled":
        where = "the repository" if policy_in_tree else "inherited from the account"
        decided["P03"] = (
            "pass",
            f"private reporting is enabled and a policy is published ({where})",
        )

    if facts["archived"]:
        decided["B09"] = ("pass", "the repository is archived, which is an intentional state")

    if facts["private"]:
        for identifier in catalog_ids:
            if identifier.startswith("P"):
                decided[identifier] = (
                    "na",
                    "the repository is private, so the Public profile does not apply",
                )

    return decided


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------


def render_record(catalog: pathlib.Path, decided: dict[str, tuple[str, str]]) -> str:
    """Fill the generated scaffold, so the criteria list cannot drift from the catalog."""
    scaffold = conformance.scaffold(catalog)
    lines = []
    for line in scaffold.splitlines():
        match = re.match(r"^  ([A-Z]\d{2}): unknown$", line)
        if match and match.group(1) in decided:
            lines.append(f"  {match.group(1)}: {decided[match.group(1)][0]}")
        else:
            lines.append(line)
    return "\n".join(lines) + "\n"


def render_notes(facts: dict, decided: dict[str, tuple[str, str]], undecided: list[str]) -> str:
    """Write the evidence the record has to point at."""
    lines = [
        f"# Draft assessment of {facts['repository']}",
        "",
        f"- Collected on: {facts['collected_on']}",
        f"- Default branch: `{facts['default_branch']}`",
        f"- Visibility: {'private' if facts['private'] else 'public'}",
        "",
        "This file is a draft. Every result below was decided by",
        "`scripts/assess.py` from a fact it could read, and every other criterion",
        "is still `unknown`. Finish the assessment by hand before the record is",
        "worth anything: replace the remaining results, replace `assessed_on`,",
        "and rewrite this file as the evidence a reader can check.",
        "",
        "## Decided from evidence",
        "",
        "| Criterion | Result | Evidence |",
        "|---|---|---|",
    ]
    for identifier in sorted(decided):
        result, why = decided[identifier]
        if result == UNDECIDED:
            continue
        lines.append(f"| `{identifier}` | {result} | {why} |")

    lines += [
        "",
        "## Left to a person",
        "",
        "These criteria turn on judgement a script cannot make — whether a README",
        "explains the purpose, whether tests cover failure paths, whether an",
        "intake form collects enough to act on. They remain `unknown`, which",
        "`conformance.py --check` rejects until each one is replaced.",
        "",
        "`" + "`, `".join(undecided) + "`",
        "",
    ]
    if facts["truncated_tree"]:
        lines += [
            "> The file listing was truncated by the API, so a path-based result",
            "> may be wrong. Check by hand.",
            "",
        ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", help="Repository as owner/name.")
    parser.add_argument("--facts", help="Decide from a saved facts file instead of the API.")
    parser.add_argument("--save-facts", help="Write the collected facts to this path.")
    parser.add_argument("--out", help="Directory to write the draft record and notes into.")
    parser.add_argument(
        "--repository",
        default=str(ROOT),
        help="Repository holding the catalog. Defaults to this one.",
    )
    arguments = parser.parse_args()

    if not arguments.repo and not arguments.facts:
        note("give either --repo owner/name or --facts FILE")
        return 2

    catalog = pathlib.Path(arguments.repository) / DEFAULT_CATALOG
    if not catalog.is_file():
        note(f"no catalog at {catalog}")
        return 1

    if arguments.facts:
        facts = json.loads(pathlib.Path(arguments.facts).read_text(encoding="utf-8"))
    else:
        facts = collect(GitHub(token()), arguments.repo)

    if arguments.save_facts:
        pathlib.Path(arguments.save_facts).write_text(
            json.dumps(facts, indent=2) + "\n", encoding="utf-8"
        )

    catalog_ids = conformance.CATALOG_ID.findall(catalog.read_text(encoding="utf-8"))
    decided = {
        identifier: value
        for identifier, value in decide(facts, catalog_ids).items()
        if value[0] != UNDECIDED and identifier in catalog_ids
    }
    undecided = [identifier for identifier in catalog_ids if identifier not in decided]

    record = render_record(catalog, decided)
    notes = render_notes(facts, decided, undecided)

    if arguments.out:
        directory = pathlib.Path(arguments.out)
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "conformance.yml").write_text(record, encoding="utf-8")
        (directory / "assessment.md").write_text(notes, encoding="utf-8")
        note(f"wrote a draft record and notes to {directory}")
    else:
        print(record)

    note(
        f"decided {len(decided)} of {len(catalog_ids)} criteria; {len(undecided)} left to a person"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
