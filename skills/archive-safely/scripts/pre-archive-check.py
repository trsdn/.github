"""Check whether a repository is safe to archive.

`A04` asks that no active deployment and no undocumented dependency remains. The
dangerous case is specific and this finds it: a launchd agent belonging to this
repository is **still loaded on this machine**, so archiving the repository stops
nobody from running it, and the next person to wonder why something is still
happening has no repository to read.

Also reports the readable half of `A01`-`A03`: the archive state, the reason and
date, and a successor link.

Usage:
    python3 pre-archive-check.py --path /path/to/checkout [--repo OWNER/NAME]

The loaded-agent check reads `launchctl` on the machine it runs on, so run it on
the machine that operates the deployment. It only ever reads.
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

SKIP = {".git", "node_modules", ".build", "build", "dist", ".venv", "DerivedData"}

ENDED_WORDS = (
    "archiv",
    "no longer maintained",
    "unmaintained",
    "discontinued",
    "sunset",
    "end of life",
)
SUCCESSOR_WORDS = (
    "superseded",
    "replaced by",
    "successor",
    "moved to",
    "continues at",
    "see instead",
)
DATE = re.compile(r"\b(20\d{2})([-/](0[1-9]|1[0-2]))?\b")


def finding(result: str, detail: str, action: str = "", evidence: list[str] | None = None) -> dict:
    return {"result": result, "detail": detail, "action": action, "evidence": evidence or []}


def loaded_labels() -> set[str] | None:
    """Labels launchd currently knows about, or None where it cannot be read."""
    if not shutil.which("launchctl"):
        return None
    result = subprocess.run(["launchctl", "list"], capture_output=True, text=True, check=False)
    if result.returncode != 0:
        return None
    labels: set[str] = set()
    for line in result.stdout.splitlines()[1:]:
        parts = line.split("\t")
        if parts:
            labels.add(parts[-1].strip())
    return labels


def repository_agents(root: pathlib.Path) -> list[tuple[str, str]]:
    """(label, path) for every launchd job this repository defines."""
    found: list[tuple[str, str]] = []
    for path in root.rglob("*.plist"):
        if set(path.parts) & SKIP:
            continue
        try:
            data = plistlib.loads(path.read_bytes())
        except Exception:  # noqa: BLE001
            continue
        if isinstance(data, dict) and data.get("Label"):
            found.append((str(data["Label"]), str(path.relative_to(root))))
    return found


def check_a04(root: pathlib.Path) -> dict:
    agents = repository_agents(root)
    containers = [
        str(p.relative_to(root))
        for p in root.rglob("*")
        if p.is_file()
        and p.name.lower() in ("dockerfile", "docker-compose.yml", "compose.yml")
        and not (set(p.parts) & SKIP)
    ]
    if not agents and not containers:
        return finding(
            "met",
            "no launchd job or container definition found in the repository",
            evidence=[],
        )

    labels = loaded_labels()
    if labels is None:
        return finding(
            "unknown",
            f"{len(agents)} launchd job(s) defined, and launchctl could not be read here",
            "run this on the machine that operates the deployment; a job loaded there is the "
            "thing A04 is about",
            evidence=[f"{label}  ({path})" for label, path in agents],
        )

    still_loaded = [(label, path) for label, path in agents if label in labels]
    if still_loaded:
        return finding(
            "gap",
            f"{len(still_loaded)} job(s) defined here are STILL LOADED on this machine",
            "unload them before archiving, or the repository is archived and the thing keeps "
            "running with nowhere to read about it: launchctl bootout gui/$UID/<label>",
            evidence=[f"{label}  ({path})" for label, path in still_loaded],
        )
    unloaded = [f"{label}  ({path})" for label, path in agents]
    return finding(
        "judgement",
        f"{len(agents)} launchd job(s) defined, none loaded here"
        + (f"; {len(containers)} container definition(s)" if containers else ""),
        "check any other machine that ran this, and anything that consumes its output",
        evidence=unloaded + containers,
    )


def check_a01(repo: str) -> dict:
    if not repo or not shutil.which("gh"):
        return finding("unknown", "no --repo given, so the archive state was not read")
    result = subprocess.run(
        ["gh", "repo", "view", repo, "--json", "isArchived"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return finding("unknown", "the repository state was not readable")
    try:
        archived = json.loads(result.stdout).get("isArchived")
    except json.JSONDecodeError:
        return finding("unknown", "the repository state was not readable")
    if archived:
        return finding("met", "GitHub reports the repository archived")
    return finding(
        "judgement",
        "the repository is not archived yet",
        "A01 is met by the archive switch; everything else here is what to do first",
    )


def check_a02_a03(root: pathlib.Path) -> tuple[dict, dict]:
    readme = root / "README.md"
    if not readme.is_file():
        return (
            finding("gap", "no README to state why and when maintenance ended"),
            finding("unknown", "no README to carry a successor link"),
        )
    text = readme.read_text(errors="replace")
    lowered = text.lower()
    said = [word for word in ENDED_WORDS if word in lowered]
    dated = DATE.search(text)
    if said and dated:
        a02 = finding(
            "judgement",
            f"the README mentions {said[0]!r} and a date ({dated.group(0)})",
            "check it says why, not only that it ended",
        )
    elif said:
        a02 = finding(
            "gap", f"the README says {said[0]!r} but names no date", "say when maintenance ended"
        )
    else:
        a02 = finding("gap", "the README does not say maintenance ended", "state why and when")
    successor = [word for word in SUCCESSOR_WORDS if word in lowered]
    if successor:
        a03 = finding("met", f"the README points somewhere: {successor[0]!r}")
    else:
        a03 = finding(
            "judgement",
            "no successor or migration destination linked",
            "A03 applies only where one exists; if nothing replaced it, that is Not applicable",
        )
    return a02, a03


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", type=pathlib.Path, default=pathlib.Path("."))
    parser.add_argument("--repo", default="", help="OWNER/NAME, to read the archive state")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()

    root = arguments.path.resolve()
    if not root.is_dir():
        print(f"archive: {root} is not a directory", file=sys.stderr)
        return 1

    a02, a03 = check_a02_a03(root)
    report = {
        "path": str(root),
        "criteria": {
            "A01": check_a01(arguments.repo),
            "A02": a02,
            "A03": a03,
            "A04": check_a04(root),
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

    if report["criteria"]["A04"]["result"] == "gap":
        print("\narchive: do not archive this repository yet")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
