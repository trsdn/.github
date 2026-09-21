# Tests and lint

Serves [`S02`](../repository-quality-standard.md#s02) (tests cover important
behavior and failure paths) and [`S03`](../repository-quality-standard.md#s03)
(format, lint, type, and static checks run automatically where supported).

## A minimum useful suite

A suite is useful when it fails for a reason a person cares about. Aim for:

1. One test of the main success path.
2. One test of each way the main path is expected to fail: bad input, a missing
   file, an error from a dependency. Assert the specific error, not just that
   something failed.
3. A regression test for each bug that was fixed.
4. The `B05` command, run in CI, so a green run is the evidence.

Coverage numbers are a floor to keep, not a goal. Set one you already meet and
raise it on purpose.

## Minimum lint by language

The check has to run automatically and fail the build.

| Language | Format | Lint | Type |
|---|---|---|---|
| Python | `ruff format --check .` | `ruff check .` | `mypy`, if the code is typed. Otherwise `S03` is partial and the assessment says why. |
| Node | Prettier check, if used | `eslint` | TypeScript: `tsc --noEmit` |
| .NET | `dotnet format --verify-no-changes` | Analyzers, run during `dotnet build` | The compiler |
| Markdown | `npx --yes markdownlint-cli2@0.18.1 "**/*.md"` | (the same) | Not applicable |

Compiling is a type check, not a format or lint check, so a .NET repository
that only builds has only part of `S03`. Pin the tool version, so a new rule does
not turn the build red on its own. Complete jobs are in the
[Python](../../templates/python/.github/workflows/ci.yml),
[Node](../../templates/node/.github/workflows/ci.yml),
[.NET](../../templates/dotnet/.github/workflows/ci.yml), and
[documentation](../../templates/docs/.github/workflows/markdown.yml) kits.

## A failure-path test where there is only a smoke test

A script with one test that runs it and checks it exits cleanly has no failure
path. Add the smallest case that shows it refuses bad input. Worked example for a
Python command line tool that takes a file:

```python
import subprocess
import sys


def test_missing_input_file_fails_with_a_message(tmp_path):
    result = subprocess.run(
        [sys.executable, "tool.py", str(tmp_path / "does-not-exist.txt")],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "does-not-exist.txt" in result.stderr
```

The test proves two things: the tool does not report success, and the message
names the file. Then break the check on purpose and confirm the test goes red. A
test that passes either way is not coverage.

## A failure-path check for a static site or content repository

A site with no logic still has ways to break: a link to a page that is gone, a
missing required front matter field, an image that is not there. Test those.
Worked example, a script that fails when a page has no title:

```sh
#!/bin/sh
# check-titles.sh: every page needs a title line.
status=0
for f in content/*.md; do
  if ! grep -q '^title:' "$f"; then
    echo "missing title: $f" >&2
    status=1
  fi
done
exit $status
```

Run it in CI as a step. Prove it catches a failure by adding a page without a
title once and watching the job go red. The link check and Markdown lint in the
[documentation kit](../../templates/docs/README.md) are checks of this kind.
For a built site, also run the build in CI: a build that fails on a broken
include is a failure-path test too.

## Worked example

A Python repository has one smoke test. Add the missing-file test above, add
`ruff check` and `ruff format --check` to CI, and note in the README the single
command the CI runs. `S02` moves from partial to pass, `S03` to pass for
format and lint, and the type check is named as the remaining gap.
