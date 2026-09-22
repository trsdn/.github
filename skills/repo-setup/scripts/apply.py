"""Apply repository metadata that `audit.py` found missing.

This script decides nothing. Every value it sets is one the caller supplies, so
the wording stays a judgement the agent or the maintainer made and this only
performs it reliably. It touches repository metadata and nothing else: no files,
no settings that change access, no visibility, no archiving.

Usage:
    python3 apply.py --repo OWNER/NAME --description "..." --topics a,b,c
    python3 apply.py --repo OWNER/NAME --homepage https://example.com --dry-run

Nothing happens without at least one value. `--dry-run` prints the commands.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys

MAX_DESCRIPTION = 350
MAX_TOPICS = 20


def run(command: list[str], dry_run: bool) -> bool:
    if dry_run:
        print("would run: " + " ".join(command))
        return True
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        message = (result.stderr or result.stdout).strip()
        print(f"repo-setup: failed: {' '.join(command)}\n  {message}", file=sys.stderr)
        return False
    return True


def valid_topic(topic: str) -> bool:
    """GitHub topics are lowercase, may hold hyphens, and start alphanumeric."""
    if not topic or len(topic) > 50:
        return False
    if topic != topic.lower():
        return False
    if not topic[0].isalnum():
        return False
    return all(character.isalnum() or character == "-" for character in topic)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="OWNER/NAME")
    parser.add_argument("--description", help="one sentence stating the purpose")
    parser.add_argument("--topics", help="comma-separated, lowercase")
    parser.add_argument("--homepage", help="URL, or an empty string to clear it")
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()

    if not shutil.which("gh"):
        print("repo-setup: gh is not on PATH", file=sys.stderr)
        return 1

    if arguments.description is None and arguments.topics is None and arguments.homepage is None:
        print("repo-setup: nothing to apply; pass --description, --topics, or --homepage")
        return 1

    if arguments.description is not None and len(arguments.description) > MAX_DESCRIPTION:
        print(
            f"repo-setup: description is {len(arguments.description)} characters, "
            f"longer than GitHub's {MAX_DESCRIPTION}",
            file=sys.stderr,
        )
        return 1

    topics: list[str] = []
    if arguments.topics is not None:
        topics = [t.strip() for t in arguments.topics.split(",") if t.strip()]
        invalid = [t for t in topics if not valid_topic(t)]
        if invalid:
            print(
                "repo-setup: these are not valid GitHub topics (lowercase, alphanumeric "
                f"and hyphens, starting alphanumeric): {', '.join(invalid)}",
                file=sys.stderr,
            )
            return 1
        if len(topics) > MAX_TOPICS:
            print(
                f"repo-setup: {len(topics)} topics, more than GitHub's {MAX_TOPICS}",
                file=sys.stderr,
            )
            return 1

    ok = True

    edit: list[str] = []
    if arguments.description is not None:
        edit += ["--description", arguments.description]
    if arguments.homepage is not None:
        edit += ["--homepage", arguments.homepage]
    if edit:
        ok &= run(["gh", "repo", "edit", arguments.repo, *edit], arguments.dry_run)

    if arguments.topics is not None:
        # `gh repo edit --add-topic` only adds, so the full set is written through
        # the API to make the result the list the caller gave rather than a union
        # with whatever was there before.
        fields: list[str] = []
        for topic in topics:
            fields += ["-f", f"names[]={topic}"]
        if not fields:
            fields = ["-f", "names[]"]
        ok &= run(
            [
                "gh",
                "api",
                "--method",
                "PUT",
                f"repos/{arguments.repo}/topics",
                "-H",
                "Accept: application/vnd.github+json",
                *fields,
            ],
            arguments.dry_run,
        )

    if not ok:
        return 1
    print("repo-setup: applied" if not arguments.dry_run else "repo-setup: dry run only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
