"""Tests for scripts/standard.py.

The script is the only thing standing between a hand-edited standard and a
catalog that other repositories consume. Every rejection path below corresponds
to a mistake that would otherwise be published.
"""

from __future__ import annotations

import subprocess
import sys
import unittest

from support import MINIMAL_CHANGELOG, MINIMAL_STANDARD, ROOT, SCRIPTS, ScriptTestCase


class StandardTests(ScriptTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.write_standard()
        self.write_changelog()

    def check(self):
        return self.run_script("standard.py", "--check")

    # Acceptance ----------------------------------------------------------

    def test_accepts_a_consistent_standard(self) -> None:
        self.generate_catalog()
        result = self.check()
        self.assertAccepts(result)
        self.assertIn("3 criteria", result.stdout)

    def test_generation_is_idempotent(self) -> None:
        self.generate_catalog()
        first = (self.repository / "standard.yml").read_text()
        self.generate_catalog()
        self.assertEqual(first, (self.repository / "standard.yml").read_text())

    def test_catalog_records_section_and_evidence(self) -> None:
        self.generate_catalog()
        catalog = (self.repository / "standard.yml").read_text()
        self.assertIn('id: "B01"', catalog)
        self.assertIn('section: "Baseline"', catalog)
        self.assertIn('evidence: "Some evidence"', catalog)
        self.assertIn('version: "2.0.0"', catalog)

    # Catalog drift -------------------------------------------------------

    def test_rejects_a_missing_catalog(self) -> None:
        self.assertRejects(self.check(), "standard.yml is missing")

    def test_rejects_a_stale_catalog(self) -> None:
        self.generate_catalog()
        self.write_standard(
            MINIMAL_STANDARD.replace(
                "First baseline requirement", "Reworded baseline requirement"
            )
        )
        self.assertRejects(self.check(), "standard.yml is out of date")

    def test_rejects_a_hand_edited_catalog(self) -> None:
        self.generate_catalog()
        path = self.repository / "standard.yml"
        path.write_text(path.read_text().replace("Some evidence", "Tampered"))
        self.assertRejects(self.check(), "standard.yml is out of date")

    # Identifier integrity ------------------------------------------------

    def test_rejects_a_duplicate_identifier(self) -> None:
        self.write_standard(
            MINIMAL_STANDARD.replace(
                '| <a id="b02"></a>B02 | Second baseline requirement | Other evidence |',
                '| <a id="b01"></a>B01 | Second baseline requirement | Other evidence |',
            )
        )
        self.assertRejects(self.check(), "identifier `B01` already defined")

    def test_rejects_a_gap_in_numbering(self) -> None:
        self.write_standard(
            MINIMAL_STANDARD.replace(
                '<a id="b02"></a>B02', '<a id="b03"></a>B03'
            )
        )
        self.assertRejects(self.check(), "prefix `B` is not contiguous from 01")

    def test_rejects_an_unclaimed_prefix(self) -> None:
        self.write_standard(
            MINIMAL_STANDARD.replace(
                '<a id="s01"></a>S01', '<a id="q01"></a>Q01'
            )
        )
        self.assertRejects(self.check(), "prefix `Q` is not claimed")

    def test_rejects_an_anchor_that_does_not_match_its_identifier(self) -> None:
        self.write_standard(
            MINIMAL_STANDARD.replace(
                '<a id="b02"></a>B02 |', '<a id="b99"></a>B02 |'
            )
        )
        self.assertRejects(self.check(), "does not match identifier")

    def test_rejects_a_missing_prefix_register(self) -> None:
        self.write_standard(MINIMAL_STANDARD.replace("### Prefix Register", "### Other"))
        self.assertRejects(self.check(), "prefix register section is missing")

    # Version integrity ---------------------------------------------------

    def test_rejects_a_version_the_changelog_does_not_mention(self) -> None:
        self.write_standard(MINIMAL_STANDARD.replace("- Version: 2.0.0", "- Version: 2.1.0"))
        self.assertRejects(self.check(), "does not match latest changelog entry")

    def test_rejects_a_missing_version_line(self) -> None:
        self.write_standard(MINIMAL_STANDARD.replace("- Version: 2.0.0\n", ""))
        self.assertRejects(self.check(), "no `- Version: X.Y.Z` line found")

    def test_rejects_a_missing_review_date(self) -> None:
        self.write_standard(MINIMAL_STANDARD.replace("- Last reviewed: 2026-01-01\n", ""))
        self.assertRejects(self.check(), "no `- Last reviewed: YYYY-MM-DD` line found")

    def test_rejects_a_changelog_without_a_versioned_heading(self) -> None:
        self.write_changelog(MINIMAL_CHANGELOG.replace("## 2.0.0 - 2026-01-01", "## Unreleased"))
        self.assertRejects(self.check(), "changelog has no versioned heading")

    # Real repository -----------------------------------------------------

    def test_this_repository_is_consistent(self) -> None:
        """The published standard must satisfy its own generator."""
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "standard.py"),
                "--check",
                "--repository",
                str(ROOT),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertAccepts(result)


if __name__ == "__main__":
    unittest.main()
