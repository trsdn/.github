"""Find where tool-specific agent instructions have drifted from `AGENTS.md`.

`G04` says a tool-specific file should point at `AGENTS.md` rather than
paraphrase it, because duplicated instructions drift apart and an agent then
follows whichever copy it happens to read.

Half of that is mechanical and this decides it: does the file reference
`AGENTS.md` at all. The other half — whether it *contradicts* `AGENTS.md` — is a
reading, so this does the work that makes the reading possible: it extracts the
rule-shaped lines from each file and shows which ones have no counterpart in
`AGENTS.md`. Those are where a contradiction can hide.

Usage:
    python3 audit.py --path /path/to/checkout [--json]
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

# The files `G04` enumerates.
TOOL_FILES = (
    ".github/copilot-instructions.md",
    "CLAUDE.md",
    "GEMINI.md",
    ".cursorrules",
    ".windsurfrules",
    ".clinerules",
)
TOOL_DIRS = (".cursor/rules",)

REFERENCE = re.compile(r"AGENTS\.md", re.I)

# A line that states a rule rather than describing something.
RULE_LINE = re.compile(
    r"(?i)\b(must|must not|never|always|do not|don't|shall|required to|only ever|"
    r"before you|make sure|ensure that)\b"
)

STOPWORDS = set(
    """a an the and or of to in for on with is are be it its this that these those you your
    we our as at by from if then than so not no yes can may should will would file files
    repository repo code change changes make made use used using run runs running""".split()
)


def find_files(root: pathlib.Path) -> list[pathlib.Path]:
    found: list[pathlib.Path] = []
    for name in TOOL_FILES:
        candidate = root / name
        if candidate.is_file():
            found.append(candidate)
    for name in TOOL_DIRS:
        directory = root / name
        if directory.is_dir():
            found.extend(sorted(p for p in directory.rglob("*") if p.is_file()))
    return found


def rule_lines(text: str) -> list[str]:
    lines: list[str] = []
    for raw in text.splitlines():
        line = raw.strip().lstrip("-*").strip()
        if len(line) < 15 or line.startswith(("#", "|", "```", "<!--")):
            continue
        if RULE_LINE.search(line):
            lines.append(line)
    return lines


def fingerprint(line: str) -> frozenset[str]:
    words = re.findall(r"[a-z0-9]+", line.lower())
    return frozenset(word for word in words if word not in STOPWORDS and len(word) > 2)


def covered(line: str, reference: list[frozenset[str]]) -> bool:
    """Is this rule already stated in AGENTS.md, in substance?"""
    mine = fingerprint(line)
    if not mine:
        return True
    for other in reference:
        if not other:
            continue
        overlap = len(mine & other) / len(mine)
        if overlap >= 0.6:
            return True
    return False


def finding(result: str, detail: str, action: str = "", evidence: list[str] | None = None) -> dict:
    return {"result": result, "detail": detail, "action": action, "evidence": evidence or []}


def audit(root: pathlib.Path) -> dict:
    agents = root / "AGENTS.md"
    files = find_files(root)

    if not agents.is_file():
        if not files:
            return {
                "path": str(root),
                "files": [],
                "criteria": {
                    "G04": finding(
                        "unknown",
                        "no AGENTS.md and no tool-specific instruction files",
                        "G04 is Not applicable where neither exists; say what you looked for",
                    )
                },
            }
        return {
            "path": str(root),
            "files": [str(p.relative_to(root)) for p in files],
            "criteria": {
                "G04": finding(
                    "gap",
                    f"{len(files)} tool-specific instruction file(s) and no AGENTS.md to agree with",
                    "the tool-neutral file is the one every agent reads; write it and point the "
                    "others at it",
                    evidence=[str(p.relative_to(root)) for p in files],
                )
            },
        }

    agents_text = agents.read_text(errors="replace")
    reference = [fingerprint(line) for line in rule_lines(agents_text)]

    unlinked: list[str] = []
    drift: list[str] = []
    linked: list[str] = []

    for path in files:
        try:
            text = path.read_text(errors="replace")
        except OSError:
            continue
        relative = str(path.relative_to(root))
        if not REFERENCE.search(text):
            unlinked.append(f"{relative} ({len(text.splitlines())} lines, no mention of AGENTS.md)")
        else:
            linked.append(relative)
        for line in rule_lines(text):
            if not covered(line, reference):
                drift.append(f"{relative}: {line[:110]}")

    if unlinked:
        return {
            "path": str(root),
            "files": [str(p.relative_to(root)) for p in files],
            "criteria": {
                "G04": finding(
                    "gap",
                    f"{len(unlinked)} tool-specific file(s) never mention AGENTS.md",
                    "a tool-specific file should point at AGENTS.md, not paraphrase it",
                    evidence=unlinked + drift[:4],
                )
            },
        }

    if drift:
        return {
            "path": str(root),
            "files": [str(p.relative_to(root)) for p in files],
            "criteria": {
                "G04": finding(
                    "judgement",
                    f"{len(drift)} rule(s) stated in a tool file with no counterpart in AGENTS.md",
                    "read each: a rule that only one agent is told is the drift G04 is about. "
                    "Move it into AGENTS.md, or delete it if AGENTS.md already says otherwise",
                    evidence=drift[:8],
                )
            },
        }

    return {
        "path": str(root),
        "files": [str(p.relative_to(root)) for p in files],
        "criteria": {
            "G04": finding(
                "met",
                f"{len(linked)} tool file(s) point at AGENTS.md and state no rule it does not",
                evidence=linked,
            )
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", type=pathlib.Path, default=pathlib.Path("."))
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()

    root = arguments.path.resolve()
    if not root.is_dir():
        print(f"instructions: {root} is not a directory", file=sys.stderr)
        return 1

    report = audit(root)
    if arguments.json:
        print(json.dumps(report, indent=2))
        return 0

    if report["files"]:
        print("tool-specific files: " + ", ".join(report["files"]) + "\n")
    entry = report["criteria"]["G04"]
    print(f"G04  {entry['result'].upper():10s} {entry['detail']}")
    for line in entry["evidence"]:
        print(f"      {line}")
    if entry["action"]:
        print(f"     → {entry['action']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
