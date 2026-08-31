"""Tests for scripts/conformance.py.

The record is the assessment; the badge is only a rendering of it. These tests
pin that relationship down: a badge may never be editable on its own, a record
may never claim more than its evidence supports, and a record that has aged past
the review cadence must stop reading as current.
"""

from __future__ import annotations

import datetime as dt
import subprocess
import sys
import unittest

from support import ROOT, SCRIPTS, ScriptTestCase

STALE_AFTER_DAYS = 183


def record(
    *,
    version: str = "2.0.0",
    assessed_on: str | None = None,
    state: str = "Healthy",
    evidence: str = "docs/self-assessment.md",
    criteria: dict[str, str] | None = None,
    omit: str = "",
) -> str:
    assessed_on = assessed_on or dt.date.today().isoformat()
    criteria = criteria or {"B01": "pass", "B02": "pass", "S01": "pass"}
    fields = {
        "standard_version": version,
        "assessed_on": assessed_on,
        "state": state,
        "evidence": evidence,
    }
    lines = [f'{key}: "{value}"' for key, value in fields.items() if key != omit]
    lines.append("")
    lines.append("criteria:")
    lines += [f"  {identifier}: {result}" for identifier, result in criteria.items()]
    return "\n".join(lines) + "\n"


class ConformanceTests(ScriptTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.write_standard()
        self.write_changelog()
        self.generate_catalog()

    def check(self):
        return self.run_script("conformance.py", "--check")

    def badge(self):
        return self.repository / ".github" / "badges" / "conformance.svg"

    def generate_badge(self) -> None:
        self.assertAccepts(self.run_script("conformance.py"))

    # Acceptance ----------------------------------------------------------

    def test_accepts_a_record_whose_badge_is_in_sync(self) -> None:
        self.write_record(record())
        self.generate_badge()
        result = self.check()
        self.assertAccepts(result)
        self.assertIn("badge in sync", result.stdout)

    def test_badge_carries_the_state_and_its_colour(self) -> None:
        self.write_record(record(state="At risk"))
        self.generate_badge()
        svg = self.badge().read_text()
        self.assertIn("At risk", svg)
        self.assertIn("#d1242f", svg)

    def test_badge_generation_is_idempotent(self) -> None:
        self.write_record(record())
        self.generate_badge()
        first = self.badge().read_text()
        self.generate_badge()
        self.assertEqual(first, self.badge().read_text())

    # The badge may not be edited on its own --------------------------------

    def test_rejects_a_missing_badge(self) -> None:
        self.write_record(record())
        self.assertRejects(self.check(), "badge is missing")

    def test_rejects_a_hand_edited_badge(self) -> None:
        self.write_record(record(state="Needs work"))
        self.generate_badge()
        self.badge().write_text(self.badge().read_text().replace("Needs work", "Healthy"))
        self.assertRejects(self.check(), "badge does not match the record")

    def test_rejects_a_badge_without_a_record(self) -> None:
        """A badge with nothing behind it is worse than no badge."""
        self.badge().write_text("<svg>Healthy</svg>")
        self.assertRejects(
            self.check(), "no conformance record exists, so no badge may be published"
        )

    def test_badge_follows_the_record_when_the_record_changes(self) -> None:
        self.write_record(record(state="Healthy"))
        self.generate_badge()
        self.write_record(record(state="At risk"))
        self.assertRejects(self.check(), "badge does not match the record")
        self.generate_badge()
        self.assertAccepts(self.check())

    # Record integrity ------------------------------------------------------

    def test_rejects_a_missing_required_field(self) -> None:
        self.write_record(record(omit="evidence"))
        self.assertRejects(self.check(), "required field `evidence` is missing")

    def test_rejects_an_undefined_state(self) -> None:
        self.write_record(record(state="Great"))
        self.assertRejects(self.check(), "state `Great` is not a defined state")

    def test_rejects_an_undefined_result(self) -> None:
        self.write_record(record(criteria={"B01": "maybe", "B02": "pass", "S01": "pass"}))
        self.assertRejects(self.check(), "`maybe` is not a defined result")

    def test_rejects_a_criterion_missing_from_the_record(self) -> None:
        self.write_record(record(criteria={"B01": "pass", "B02": "pass"}))
        self.assertRejects(self.check(), "S01 is missing from the record")

    def test_rejects_a_criterion_that_is_not_in_the_catalog(self) -> None:
        self.write_record(
            record(criteria={"B01": "pass", "B02": "pass", "S01": "pass", "B09": "pass"})
        )
        self.assertRejects(self.check(), "B09 is not a criterion in the catalog")

    def test_rejects_healthy_with_a_failing_criterion(self) -> None:
        """The record may not claim more than its own criteria support."""
        self.write_record(
            record(state="Healthy", criteria={"B01": "fail", "B02": "pass", "S01": "pass"})
        )
        self.assertRejects(
            self.check(), "state `Healthy` is not consistent with failing criteria: B01"
        )

    def test_allows_needs_work_with_a_failing_criterion(self) -> None:
        self.write_record(
            record(state="Needs work", criteria={"B01": "fail", "B02": "pass", "S01": "pass"})
        )
        self.generate_badge()
        self.assertAccepts(self.check())

    # Version pinning -------------------------------------------------------

    def test_rejects_a_record_pinned_to_another_standard_version(self) -> None:
        self.write_record(record(version="1.0.0"))
        self.assertRejects(self.check(), "reassess or pin the record")

    # Published tags --------------------------------------------------------

    def test_accepts_a_recorded_version_that_has_a_published_tag(self) -> None:
        self.write_record(record())
        self.generate_badge()
        self.assertAccepts(
            self.run_script("conformance.py", "--check", "--published-tags", "v1.9.0, v2.0.0")
        )

    def test_rejects_a_recorded_version_that_has_no_published_tag(self) -> None:
        """The state this repository was in: merged, recorded, never tagged."""
        self.write_record(record())
        self.generate_badge()
        self.assertRejects(
            self.run_script("conformance.py", "--check", "--published-tags", "v1.9.0"),
            "`v2.0.0` is not a published tag",
        )

    def test_rejects_a_recorded_version_when_no_tag_exists_at_all(self) -> None:
        self.write_record(record())
        self.generate_badge()
        self.assertRejects(
            self.run_script("conformance.py", "--check", "--published-tags", ""),
            "`v2.0.0` is not a published tag",
        )

    def test_skips_the_tag_check_when_no_tags_are_supplied(self) -> None:
        """A version bump is merged before it is tagged, so pull requests opt out."""
        self.write_record(record())
        self.generate_badge()
        self.assertAccepts(self.check())

    # Ageing ----------------------------------------------------------------

    def test_rejects_a_record_older_than_the_review_cadence(self) -> None:
        old = dt.date.today() - dt.timedelta(days=STALE_AFTER_DAYS + 1)
        self.write_record(record(assessed_on=old.isoformat()))
        self.generate_badge()
        self.assertRejects(self.check(), "older than the review cadence")

    def test_accepts_a_record_just_inside_the_review_cadence(self) -> None:
        recent = dt.date.today() - dt.timedelta(days=STALE_AFTER_DAYS - 1)
        self.write_record(record(assessed_on=recent.isoformat()))
        self.generate_badge()
        self.assertAccepts(self.check())

    def test_a_stale_record_renders_a_distinct_badge(self) -> None:
        """The public badge stays honest even while the assessment is overdue."""
        old = dt.date.today() - dt.timedelta(days=STALE_AFTER_DAYS + 1)
        self.write_record(record(assessed_on=old.isoformat()))
        self.assertAccepts(self.run_script("conformance.py"))
        self.assertIn("#8250df", self.badge().read_text())

    def test_regenerating_a_stale_badge_does_not_clear_the_failure(self) -> None:
        """Ageing may not be silenced by regenerating the badge."""
        old = dt.date.today() - dt.timedelta(days=STALE_AFTER_DAYS + 1)
        self.write_record(record(assessed_on=old.isoformat()))
        self.assertAccepts(self.run_script("conformance.py"))
        self.assertRejects(self.check(), "older than the review cadence")

    def test_rejects_a_record_assessed_in_the_future(self) -> None:
        ahead = dt.date.today() + dt.timedelta(days=1)
        self.write_record(record(assessed_on=ahead.isoformat()))
        self.assertRejects(self.check(), "assessed_on is in the future")

    def test_rejects_a_malformed_date(self) -> None:
        self.write_record(record(assessed_on="22-08-2026"))
        self.assertRejects(self.check(), "is not an ISO date")

    # Real repository -------------------------------------------------------

    def test_this_repository_record_is_valid(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "conformance.py"),
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
