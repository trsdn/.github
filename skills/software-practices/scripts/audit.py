"""Report evidence for the Software practices a repository can be read for.

Covers `S01` (setup is reproducible), `S06` (configuration is environment-driven
and its defaults expose nothing), `S07` (errors and logs are actionable and leak
nothing) and `S10` (architecture and non-obvious constraints are documented).

It reads. Whether a message is *actionable*, and whether a document names the
constraints that matter, are readings it reports evidence for rather than
decides.

Usage:
    python3 audit.py --path /path/to/checkout [--json]
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

SKIP_DIRS = {
    ".git",
    "node_modules",
    ".build",
    "build",
    "dist",
    ".venv",
    "venv",
    "Pods",
    "Carthage",
    "vendor",
    "DerivedData",
    "__pycache__",
    ".next",
    "target",
    ".worktrees",
}

CODE_SUFFIXES = {
    ".swift",
    ".m",
    ".mm",
    ".py",
    ".js",
    ".mjs",
    ".ts",
    ".tsx",
    ".jsx",
    ".go",
    ".rs",
    ".rb",
    ".java",
    ".kt",
    ".cs",
    ".sh",
}
CONFIG_SUFFIXES = {".yml", ".yaml", ".json", ".toml", ".ini", ".cfg", ".plist", ".env", ".xcconfig"}

LOCKFILES = (
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "Package.resolved",
    "poetry.lock",
    "uv.lock",
    "Cargo.lock",
    "go.sum",
    "Gemfile.lock",
    "packages.lock.json",
)
MANIFESTS = (
    "package.json",
    "pyproject.toml",
    "requirements.txt",
    "Package.swift",
    "go.mod",
    "Cargo.toml",
    "Gemfile",
)

COMMAND_WORDS = ("install", "build", "test", "run", "make", "swift ", "npm ", "pip ", "python")

LOG_CALLS = re.compile(
    r"\b(print|NSLog|os_log|Logger|logger|log|console\.(log|warn|error|info)|"
    r"logging\.(debug|info|warning|error|critical)|fmt\.Print\w*|Console\.Write\w*)\s*[(.]"
)
SENSITIVE = re.compile(
    r"\b(token|password|passwd|secret|api[_-]?key|apikey|credential|authorization|bearer|"
    r"cookie|session[_-]?id|private[_-]?key|connection[_-]?string|dsn|email|e-mail)\b",
    re.I,
)
BARE_MESSAGE = re.compile(
    r"""["'](error|failed|failure|something went wrong|unknown error|oops|error!|"""
    r"""an error occurred)[.!]?["']""",
    re.I,
)

HOME_PATH = re.compile(
    r"(/Users/[A-Za-z0-9._-]+|/home/[A-Za-z0-9._-]+|C:\\\\Users\\\\[A-Za-z0-9._-]+)"
)
EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
ENV_READ = re.compile(
    r"(os\.environ|getenv|ProcessInfo\.processInfo\.environment|process\.env|"
    r"Environment\.GetEnvironmentVariable|ENV\[)"
)

ARCHITECTURE_WORDS = (
    "architecture",
    "design",
    "overview",
    "how it works",
    "structure",
    "components",
)

PLACEHOLDER_EMAILS = ("example.com", "example.org", "noreply", "users.noreply.github.com")

# X04: colour and decoration in terminal output. ANSI escapes are fine when the
# program also honours a way to turn them off; box-drawing and symbols are fine
# when they are not the only thing carrying the meaning.
ANSI = re.compile(r"\\033\[|\\x1b\[|\\u001b\[|\\e\[|chalk\.|colorama|termcolor|ANSIColor")
NO_COLOUR = re.compile(r"(?i)NO_COLOR|isatty|is_a_tty|supportsColor|FORCE_COLOR|--no-color")
DECORATION = re.compile(
    "[\u2500-\u257f\u2580-\u259f\u2190-\u21ff\u2600-\u27bf"
    "\U0001f300-\U0001faff\u2713\u2714\u2717\u2718]"
)


def files(root: pathlib.Path, limit: int = 4000) -> list[pathlib.Path]:
    out: list[pathlib.Path] = []
    for path in root.rglob("*"):
        if len(out) >= limit:
            break
        if not path.is_file() or set(path.parts) & SKIP_DIRS:
            continue
        if path.suffix.lower() not in CODE_SUFFIXES | CONFIG_SUFFIXES:
            continue
        try:
            if path.stat().st_size > 800_000:
                continue
        except OSError:
            continue
        out.append(path)
    return out


def finding(result: str, detail: str, action: str = "", evidence: list[str] | None = None) -> dict:
    return {"result": result, "detail": detail, "action": action, "evidence": evidence or []}


def check_s01(root: pathlib.Path) -> dict:
    locks = [name for name in LOCKFILES if (root / name).is_file()]
    manifests = [name for name in MANIFESTS if (root / name).is_file()]
    readme = root / "README.md"
    commands: list[str] = []
    if readme.is_file():
        text = readme.read_text(errors="replace")
        for block in re.findall(r"```[a-z]*\n(.*?)```", text, re.S):
            for line in block.splitlines():
                stripped = line.strip()
                if stripped and any(word in stripped.lower() for word in COMMAND_WORDS):
                    commands.append(stripped)
    if not manifests and not locks:
        return finding(
            "unknown",
            "no dependency manifest or lockfile found",
            "a repository with no dependencies meets S01 through its documented commands alone",
        )
    if locks and commands:
        return finding(
            "met", f"lockfile ({', '.join(locks)}) and documented commands", evidence=commands[:3]
        )
    if not locks and manifests and commands:
        return finding(
            "judgement",
            f"manifest ({', '.join(manifests)}) without a lockfile, and documented commands",
            "a library declaring ranges meets the pinning half; an application usually should not",
            evidence=commands[:3],
        )
    if locks and not commands:
        return finding(
            "gap",
            f"lockfile ({', '.join(locks)}) but no setup command found in the README",
            "document the commands that take a clean checkout to a working build",
        )
    return finding(
        "gap",
        "neither pinned dependencies nor documented setup commands were found",
        "add both: the versions, and the commands that use them",
    )


def check_s06(root: pathlib.Path, paths: list[pathlib.Path]) -> dict:
    reads: list[str] = []
    exposed: list[str] = []
    for path in paths:
        try:
            text = path.read_text(errors="replace")
        except OSError:
            continue
        relative = str(path.relative_to(root))
        for number, line in enumerate(text.splitlines(), start=1):
            where = f"{relative}:{number}"
            if ENV_READ.search(line) and len(reads) < 5:
                reads.append(where)
            if path.suffix.lower() in CONFIG_SUFFIXES or "config" in relative.lower():
                home = HOME_PATH.search(line)
                if home:
                    exposed.append(f"{where}  home directory path: {home.group(0)}")
                    continue
                mail = EMAIL.search(line)
                if mail and not any(hint in mail.group(0) for hint in PLACEHOLDER_EMAILS):
                    exposed.append(f"{where}  email address: {mail.group(0)}")
    if exposed:
        return finding(
            "gap",
            f"{len(exposed)} committed default(s) expose a home path or a personal address",
            "move them to environment variables and ship an example file instead",
            evidence=exposed[:6],
        )
    if not reads:
        return finding(
            "unknown",
            "nothing was seen reading configuration",
            "S06 is Not applicable where nothing reads configuration; say what you looked for",
        )
    return finding(
        "met",
        "configuration is read from the environment and no exposed default was found",
        evidence=reads,
    )


def check_s07(root: pathlib.Path, paths: list[pathlib.Path]) -> dict:
    leaks: list[str] = []
    bare: list[str] = []
    logs = 0
    for path in paths:
        if path.suffix.lower() not in CODE_SUFFIXES:
            continue
        try:
            text = path.read_text(errors="replace")
        except OSError:
            continue
        relative = str(path.relative_to(root))
        for number, line in enumerate(text.splitlines(), start=1):
            if not LOG_CALLS.search(line):
                continue
            logs += 1
            where = f"{relative}:{number}"
            if SENSITIVE.search(line):
                leaks.append(f"{where}  {line.strip()[:90]}")
            elif BARE_MESSAGE.search(line):
                bare.append(f"{where}  {line.strip()[:90]}")
    if not logs:
        return finding(
            "unknown",
            "no logging or error output was found",
            "S07 is Not applicable where the code emits none; say what you looked for",
        )
    if leaks:
        return finding(
            "gap",
            f"{len(leaks)} log line(s) mention a credential or personal field",
            "check each: logging the name of a token is fine, logging its value is not",
            evidence=leaks[:6],
        )
    if bare:
        return finding(
            "judgement",
            f"{len(bare)} message(s) may not name the failed operation or its cause",
            "the minimum S07 asks is the operation that failed and why, not a bare 'error'",
            evidence=bare[:6],
        )
    return finding("met", f"{logs} log or error sites, none naming a credential or bare message")


def check_s10(root: pathlib.Path) -> dict:
    hits: list[str] = []
    if (root / "docs" / "decisions").is_dir():
        hits.append("docs/decisions/")
    for path in list((root / "docs").rglob("*.md")) if (root / "docs").is_dir() else []:
        if any(word in path.name.lower() for word in ARCHITECTURE_WORDS):
            hits.append(str(path.relative_to(root)))
    readme = root / "README.md"
    if readme.is_file():
        for line in readme.read_text(errors="replace").splitlines():
            if line.startswith("#") and any(word in line.lower() for word in ARCHITECTURE_WORDS):
                hits.append(f"README.md: {line.strip('# ').strip()}")
    agents = root / "AGENTS.md"
    if agents.is_file():
        hits.append("AGENTS.md")
    if hits:
        return finding(
            "judgement",
            "a document that may carry the architecture exists",
            "S10 wants the main components named, and any constraint a new contributor could "
            "break without knowing it. Read these and decide",
            evidence=hits[:6],
        )
    return finding(
        "gap",
        "no architecture document, ADR, or README section found",
        "name the main components and the constraints that are not obvious from the code",
    )


def check_x04(root: pathlib.Path, paths: list[pathlib.Path]) -> dict:
    colour: list[str] = []
    decoration: list[str] = []
    escape_hatch: list[str] = []
    for path in paths:
        if path.suffix.lower() not in CODE_SUFFIXES:
            continue
        try:
            text = path.read_text(errors="replace")
        except OSError:
            continue
        relative = str(path.relative_to(root))
        for number, line in enumerate(text.splitlines(), start=1):
            where = f"{relative}:{number}"
            if NO_COLOUR.search(line):
                escape_hatch.append(where)
            elif ANSI.search(line):
                colour.append(where)
            elif DECORATION.search(line) and ('"' in line or "'" in line):
                decoration.append(f"{where}  {line.strip()[:70]}")
    if not colour and not decoration:
        return finding(
            "unknown",
            "no colour or decorated output was found",
            "X04 is Not applicable where the product has no terminal output; say what you "
            "looked for",
        )
    if colour and not escape_hatch:
        return finding(
            "gap",
            f"{len(colour)} site(s) emit colour and nothing was seen turning it off",
            "honour NO_COLOR, or check isatty, so piped and redirected output stays readable",
            evidence=colour[:5],
        )
    if decoration:
        return finding(
            "judgement",
            f"{len(decoration)} line(s) put box-drawing or symbols in output"
            + (f"; colour has an off switch at {escape_hatch[0]}" if escape_hatch else ""),
            "check the meaning survives without them: a tick that is the only signal of success "
            "is the failure X04 names",
            evidence=decoration[:5],
        )
    return finding(
        "met",
        f"{len(colour)} colour site(s), with an off switch at {escape_hatch[0]}",
    )


def audit(root: pathlib.Path) -> dict:
    paths = files(root)
    return {
        "path": str(root),
        "criteria": {
            "S01": check_s01(root),
            "S06": check_s06(root, paths),
            "S07": check_s07(root, paths),
            "S10": check_s10(root),
            "X04": check_x04(root, paths),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", type=pathlib.Path, default=pathlib.Path("."))
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()

    root = arguments.path.resolve()
    if not root.is_dir():
        print(f"software: {root} is not a directory", file=sys.stderr)
        return 1

    report = audit(root)
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
