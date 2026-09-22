"""Report deployment evidence for a repository that runs something standing.

Covers the Deployable criteria: `D01` (target, prerequisites, configuration and
deployment command documented), `D02` (secrets referenced, never committed, and
their safe location documented), `D03` (health verification and the way back),
`D04` (runtime and infrastructure dependencies constrained), `D05` (operational
changes have durable history) and `D06` (backup, migration and destructive
operations addressed when stateful).

Five of those six are criteria whose failure the standard calls critical, which
is why this is explicit about what it could not read rather than quiet about it.

It understands the shapes these repositories use: launchd agents and daemons,
Docker and Compose, and systemd units.

Usage:
    python3 audit.py --path /path/to/checkout [--json]
"""

from __future__ import annotations

import argparse
import json
import pathlib
import plistlib
import re
import sys

SKIP = {".git", "node_modules", ".build", "build", "dist", ".venv", "DerivedData"}

RUNBOOK_WORDS = ("deploy", "install", "runbook", "operations", "setup", "rollout")
RUNBOOK_TEXT_WORDS = (
    "deployment command",
    "to deploy",
    "to install",
    "## install",
    "# install",
    "launchctl",
    "systemctl",
    "docker compose up",
    "docker run",
)
HEALTH_WORDS = ("health", "verify", "smoke", "status", "check that", "confirm")
ROLLBACK_WORDS = ("rollback", "roll back", "revert", "previous version", "uninstall", "restore")
BACKUP_WORDS = ("backup", "back up", "restore", "snapshot", "migrat", "retention")
SECRET_LOCATION_WORDS = ("keychain", "secret", "environment variable", "1password", "vault", ".env")

SECRET_VALUE = re.compile(
    r"""(?ix)\b(token|secret|password|api[_-]?key|apikey|client[_-]?secret)\b\s*[:=]\s*["']?"""
    r"""([A-Za-z0-9_\-/+]{16,})["']?"""
)
PLACEHOLDER = re.compile(r"(?i)(__[A-Z_]+__|\$\{?[A-Z_]+\}?|<[a-z_ -]+>|xxx+|changeme|your[_-])")
FLOATING_IMAGE = re.compile(r"(?im)^\s*(?:FROM|image:)\s*([^\s#]+)")
SECRET_SCAN_SUFFIXES = {
    ".plist",
    ".yml",
    ".yaml",
    ".env",
    ".json",
    ".sh",
    ".toml",
    ".ini",
    ".cfg",
    ".swift",
    ".py",
    ".ts",
    ".js",
    ".mjs",
    ".go",
    ".rs",
    ".rb",
    ".java",
    ".kt",
    ".cs",
    ".c",
    ".cc",
    ".cpp",
    ".m",
    ".mm",
    ".php",
}
SECRET_REFERENCE = re.compile(
    r"""(?ix)\b(token|secret|password|api[_-]?key|apikey|credential|keychain|"""
    r"""SecItemCopyMatching|getenv|os\.environ|process\.env)\b"""
)


def walk(root: pathlib.Path) -> list[pathlib.Path]:
    return [p for p in root.rglob("*") if p.is_file() and not (set(p.parts) & SKIP)]


def finding(result: str, detail: str, action: str = "", evidence: list[str] | None = None) -> dict:
    return {"result": result, "detail": detail, "action": action, "evidence": evidence or []}


def discover(paths: list[pathlib.Path]) -> dict:
    """What kind of standing deployment, if any, this repository describes."""
    launchd: list[pathlib.Path] = []
    containers: list[pathlib.Path] = []
    systemd: list[pathlib.Path] = []
    for path in paths:
        name = path.name.lower()
        if path.suffix == ".plist":
            try:
                data = plistlib.loads(path.read_bytes())
            except Exception:  # noqa: BLE001
                continue
            if isinstance(data, dict) and ("RunAtLoad" in data or "ProgramArguments" in data):
                launchd.append(path)
        elif name in ("dockerfile", "docker-compose.yml", "docker-compose.yaml", "compose.yml"):
            containers.append(path)
        elif path.suffix == ".service":
            systemd.append(path)
    return {"launchd": launchd, "containers": containers, "systemd": systemd}


def documents(root: pathlib.Path, paths: list[pathlib.Path]) -> dict[str, str]:
    out: dict[str, str] = {}
    for path in paths:
        if path.suffix.lower() != ".md":
            continue
        try:
            out[str(path.relative_to(root))] = path.read_text(errors="replace").lower()
        except OSError:
            continue
    return out


def check_d01(docs: dict[str, str], root: pathlib.Path) -> dict:
    hits = [
        name
        for name, text in docs.items()
        if any(word in name.lower() for word in RUNBOOK_WORDS)
        or any(word in text for word in RUNBOOK_TEXT_WORDS)
    ]
    installers = [
        str(p.relative_to(root))
        for p in root.glob("*.sh")
        if any(word in p.name.lower() for word in ("install", "deploy", "setup"))
    ]
    if hits or installers:
        return finding(
            "judgement",
            "documentation or an installer that may carry the runbook exists",
            "D01 wants four things: target, prerequisites, configuration, and the command. "
            "Check all four are there, not only the command",
            evidence=(hits[:3] + installers[:3]),
        )
    return finding(
        "gap",
        "no runbook, deployment document, or installer found",
        "write where it runs, what it needs, how it is configured, and the command",
    )


def check_d02(root: pathlib.Path, paths: list[pathlib.Path], docs: dict[str, str]) -> dict:
    committed: list[str] = []
    references: list[str] = []
    for path in paths:
        if path.suffix.lower() not in SECRET_SCAN_SUFFIXES:
            continue
        try:
            text = path.read_text(errors="replace")
        except OSError:
            continue
        for number, line in enumerate(text.splitlines(), start=1):
            match = SECRET_VALUE.search(line)
            if match and not PLACEHOLDER.search(line):
                committed.append(f"{path.relative_to(root)}:{number}  {match.group(1)}")
            elif SECRET_REFERENCE.search(line):
                references.append(f"{path.relative_to(root)}:{number}")
    if committed:
        return finding(
            "gap",
            f"{len(committed)} line(s) look like a committed secret value",
            "stop and tell the maintainer which credential and what it unlocks. Do not rotate, "
            "delete, or rewrite history yourself",
            evidence=committed[:5],
        )
    if not references:
        return finding(
            "unknown",
            "nothing seen that uses a secret",
            "D02 is Not applicable where the deployment needs none; say what you looked for",
        )
    stated = [name for name, text in docs.items() if any(w in text for w in SECRET_LOCATION_WORDS)]
    if stated:
        return finding(
            "met",
            "secrets are referenced, none is committed, and a safe location is described",
            evidence=stated[:3],
        )
    return finding(
        "gap",
        f"{len(references)} secret reference(s), none committed, but no documented safe location",
        "say where they live: the Keychain, a file outside the repository, or a manager",
        evidence=references[:4],
    )


def check_d03(docs: dict[str, str], kinds: dict, root: pathlib.Path) -> dict:
    health = [name for name, text in docs.items() if any(w in text for w in HEALTH_WORDS)]
    back = [name for name, text in docs.items() if any(w in text for w in ROLLBACK_WORDS)]
    for path in kinds["containers"]:
        try:
            if "healthcheck" in path.read_text(errors="replace").lower():
                health.append(str(path.relative_to(root)))
        except OSError:
            continue
    if health and back:
        return finding(
            "judgement",
            "both a health step and a way back are described somewhere",
            "check the health step is a command or an observable, not 'make sure it works'",
            evidence=sorted(set(health))[:2] + sorted(set(back))[:2],
        )
    if health:
        return finding(
            "gap",
            "a health check is described, but no way back to the previous working state",
            "D03 wants both. For a launchd agent the way back is usually the previous binary "
            "and a reload command",
            evidence=sorted(set(health))[:3],
        )
    if back:
        return finding(
            "gap", "a way back is described, but no health verification", evidence=back[:3]
        )
    return finding(
        "gap",
        "neither a health verification nor a way back was found",
        "one command that says it is working, and one that puts the previous version back",
    )


def check_d04(kinds: dict, root: pathlib.Path) -> dict:
    problems: list[str] = []
    fine: list[str] = []
    templates: list[str] = []
    for path in kinds["containers"]:
        try:
            text = path.read_text(errors="replace")
        except OSError:
            continue
        for match in FLOATING_IMAGE.finditer(text):
            image = match.group(1)
            if image.endswith(":latest") or ":" not in image.rsplit("/", 1)[-1]:
                problems.append(f"{path.relative_to(root)}: {image} is unpinned")
            else:
                fine.append(f"{path.relative_to(root)}: {image}")
    for path in kinds["launchd"]:
        try:
            data = plistlib.loads(path.read_bytes())
        except Exception:  # noqa: BLE001
            continue
        arguments = data.get("ProgramArguments") or []
        if arguments and isinstance(arguments[0], str):
            program = arguments[0]
            if PLACEHOLDER.search(program):
                templates.append(f"{path.relative_to(root)}: {program}")
            elif program.startswith("/usr/bin/env"):
                problems.append(
                    f"{path.relative_to(root)}: runs through /usr/bin/env, so the interpreter "
                    "is whatever the PATH finds"
                )
            else:
                fine.append(f"{path.relative_to(root)}: {program}")
    if problems:
        return finding(
            "gap",
            "a runtime or image is not constrained",
            "pin the image to a tag or digest, and name the interpreter by absolute path",
            evidence=problems[:5],
        )
    if templates:
        return finding(
            "judgement",
            "the unit file is a template whose program path is substituted at install time",
            "read the installer to see what it puts there; the constraint is whatever that is, "
            "not what the template says",
            evidence=templates[:4],
        )
    if fine:
        return finding("met", "runtimes and images are pinned", evidence=fine[:4])
    return finding(
        "unknown",
        "no image or program declaration was read",
        "say what the deployment runs on and how that is constrained",
    )


def check_d05(root: pathlib.Path) -> dict:
    if (root / "CHANGELOG.md").is_file():
        return finding("met", "a changelog records changes")
    if (root / "docs" / "decisions").is_dir():
        return finding("met", "decision records exist")
    return finding(
        "judgement",
        "no changelog or decision records found",
        "releases or linked issues also satisfy D05; check before adding a file",
    )


def check_d06(kinds: dict, docs: dict[str, str], root: pathlib.Path) -> dict:
    stateful: list[str] = []
    for path in kinds["containers"]:
        try:
            text = path.read_text(errors="replace").lower()
        except OSError:
            continue
        if "volumes:" in text:
            stateful.append(f"{path.relative_to(root)} declares volumes")
    for path in kinds["launchd"]:
        try:
            data = plistlib.loads(path.read_bytes())
        except Exception:  # noqa: BLE001
            continue
        if data.get("WorkingDirectory"):
            stateful.append(
                f"{path.relative_to(root)}: WorkingDirectory {data['WorkingDirectory']}"
            )
    addressed = [name for name, text in docs.items() if any(w in text for w in BACKUP_WORDS)]
    if not stateful:
        return finding(
            "unknown",
            "nothing seen that holds state",
            "D06 applies when stateful; if it holds nothing that cannot be rebuilt, say so",
        )
    if addressed:
        return finding(
            "judgement",
            "it holds state, and backup or migration is mentioned",
            "check what is described covers the state actually at risk",
            evidence=stateful[:3] + addressed[:2],
        )
    return finding(
        "gap",
        "it holds state, and no backup, restore, or migration is described",
        "say what would be lost and how it is recovered",
        evidence=stateful[:4],
    )


def audit(root: pathlib.Path) -> dict:
    paths = walk(root)
    kinds = discover(paths)
    docs = documents(root, paths)
    if not (kinds["launchd"] or kinds["containers"] or kinds["systemd"]):
        return {
            "path": str(root),
            "deployment": {},
            "criteria": {
                identifier: finding(
                    "unknown",
                    "no launchd agent, container, or unit file found",
                    "the Deployable profile applies where the maintainer operates a standing "
                    "deployment. If nobody does, D01-D06 are Not applicable",
                )
                for identifier in ("D01", "D02", "D03", "D04", "D05", "D06")
            },
        }
    return {
        "path": str(root),
        "deployment": {
            kind: [str(p.relative_to(root)) for p in found]
            for kind, found in kinds.items()
            if found
        },
        "criteria": {
            "D01": check_d01(docs, root),
            "D02": check_d02(root, paths, docs),
            "D03": check_d03(docs, kinds, root),
            "D04": check_d04(kinds, root),
            "D05": check_d05(root),
            "D06": check_d06(kinds, docs, root),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", type=pathlib.Path, default=pathlib.Path("."))
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()

    root = arguments.path.resolve()
    if not root.is_dir():
        print(f"deployment: {root} is not a directory", file=sys.stderr)
        return 1

    report = audit(root)
    if arguments.json:
        print(json.dumps(report, indent=2))
        return 0

    for kind, found in report["deployment"].items():
        print(f"{kind}: {', '.join(found)}")
    if report["deployment"]:
        print()

    order = {"gap": 0, "judgement": 1, "unknown": 2, "met": 3}
    critical = {"D01", "D02", "D03", "D04", "D06"}
    for identifier, entry in sorted(
        report["criteria"].items(), key=lambda kv: (order[kv[1]["result"]], kv[0])
    ):
        mark = " (critical)" if identifier in critical and entry["result"] == "gap" else ""
        print(f"{identifier}  {entry['result'].upper():10s} {entry['detail']}{mark}")
        for line in entry["evidence"]:
            print(f"      {line}")
        if entry["action"]:
            print(f"     → {entry['action']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
