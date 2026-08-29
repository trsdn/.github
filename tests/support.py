"""Shared fixtures for the validation script tests.

Each test builds a small synthetic repository on disk and runs a script against
it as a subprocess. Exercising the command line is deliberate: the exit code and
the diagnostic are the contract CI depends on, so that is what is asserted. A
check that fails for the wrong reason is not a working check.
"""

from __future__ import annotations

import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"

MINIMAL_STANDARD = """\
# Repository Quality Standard

- Version: 2.0.0
- Last reviewed: 2026-01-01
- Review cadence: every six months

Intro text.

## Versioning And Compatibility

Policy text.

### Prefix Register

| Prefix | Section |
|---|---|
| B | Baseline |
| S | Software |

Trailing text.

## Baseline

| ID | Requirement | Expected evidence |
|---|---|---|
| <a id="b01"></a>B01 | First baseline requirement | Some evidence |
| <a id="b02"></a>B02 | Second baseline requirement | Other evidence |

## Software

| ID | Requirement | Expected evidence |
|---|---|---|
| <a id="s01"></a>S01 | First software requirement | More evidence |
"""

MINIMAL_CHANGELOG = """\
# Changelog

Intro.

## 2.0.0 - 2026-01-01

- Something changed.
"""


class ScriptTestCase(unittest.TestCase):
    """Builds throwaway repositories and runs a script against them."""

    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.repository = pathlib.Path(directory.name)
        (self.repository / "docs").mkdir()
        (self.repository / ".github").mkdir()
        (self.repository / ".github" / "badges").mkdir()

    def write_standard(self, text: str = MINIMAL_STANDARD) -> None:
        (self.repository / "docs" / "repository-quality-standard.md").write_text(text)

    def write_changelog(self, text: str = MINIMAL_CHANGELOG) -> None:
        (self.repository / "CHANGELOG.md").write_text(text)

    def write_record(self, text: str) -> None:
        (self.repository / ".github" / "conformance.yml").write_text(text)

    def write_catalog(self, text: str) -> None:
        (self.repository / "standard.yml").write_text(text)

    def generate_catalog(self) -> None:
        """Produce a catalog the way a maintainer would, by running the script."""
        result = self.run_script("standard.py")
        self.assertAccepts(result)

    def run_script(self, name: str, *arguments: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / name),
                "--repository",
                str(self.repository),
                *arguments,
            ],
            capture_output=True,
            text=True,
            check=False,
        )

    def assertRejects(self, result: subprocess.CompletedProcess, expected: str) -> None:
        """Assert a non-zero exit *and* the specific reason for it."""
        output = result.stdout + result.stderr
        self.assertNotEqual(
            result.returncode,
            0,
            msg=f"expected a non-zero exit, got 0. Output:\n{output}",
        )
        self.assertIn(
            expected,
            output,
            msg=f"expected diagnostic containing {expected!r}. Output:\n{output}",
        )

    def assertAccepts(self, result: subprocess.CompletedProcess) -> None:
        output = result.stdout + result.stderr
        self.assertEqual(result.returncode, 0, msg=f"expected a zero exit. Output:\n{output}")
