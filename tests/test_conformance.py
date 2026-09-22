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

from support import MINIMAL_STANDARD, ROOT, SCRIPTS, ScriptTestCase

STALE_AFTER_DAYS = 183

# `B02` is the criterion the test standard names critical, and `S01` is an
# ordinary one. A record's state follows its results, so a test that wants a
# state has to record the results that produce it.
CRITICAL_FAILURE = {"B01": "pass", "B02": "fail", "S01": "pass"}
ORDINARY_FAILURE = {"B01": "pass", "B02": "pass", "S01": "fail"}

# A standard with an Archived section, for the states whose prerequisites name
# criteria the minimal standard does not have.
ARCHIVE_STANDARD = MINIMAL_STANDARD.replace(
    "| B | Baseline |",
    "| A | Archived |\n| B | Baseline |",
).replace(
    "## Conformance Records",
    """## Archived

| ID | Requirement | Expected evidence |
|---|---|---|
| <a id="a01"></a>A01 | First archive requirement | Some evidence |
| <a id="a02"></a>A02 | Second archive requirement | Some evidence |
| <a id="a03"></a>A03 | Third archive requirement | Some evidence |
| <a id="a04"></a>A04 | Fourth archive requirement | Some evidence |

## Conformance Records""",
)


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

    def record_path(self):
        return self.repository / ".github" / "conformance.yml"

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
        self.write_record(record(state="At risk", criteria=CRITICAL_FAILURE))
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
        self.write_record(record(state="Needs work", criteria=ORDINARY_FAILURE))
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
        self.write_record(record(state="At risk", criteria=CRITICAL_FAILURE))
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

    # The state follows the results -----------------------------------------

    def test_rejects_a_draft_record(self) -> None:
        """An untouched scaffold is not an assessment, whatever state it names."""
        self.write_record(
            record(state="Needs work", criteria={"B01": "unknown", "B02": "pass", "S01": "pass"})
        )
        self.assertRejects(self.check(), "1 criteria are still `unknown`")

    def test_rejects_a_critical_failure_recorded_as_needs_work(self) -> None:
        """`B02` is critical in the test standard, so its failure is `At risk`."""
        self.write_record(record(state="Needs work", criteria=CRITICAL_FAILURE))
        self.assertRejects(self.check(), "they support `At risk` because B02 is critical")

    def test_rejects_healthy_results_recorded_as_needs_work(self) -> None:
        """The disagreement is rejected in both directions, not only the flattering one."""
        self.write_record(record(state="Needs work"))
        self.assertRejects(self.check(), "they support `Healthy`")

    def test_accepts_a_critical_failure_recorded_as_at_risk(self) -> None:
        self.write_record(record(state="At risk", criteria=CRITICAL_FAILURE))
        self.generate_badge()
        self.assertAccepts(self.check())

    def test_writes_the_state_the_results_support(self) -> None:
        """Generating the badge settles the state, so nobody has to type it."""
        self.write_record(record(state="Healthy", criteria=CRITICAL_FAILURE))
        self.generate_badge()
        self.assertIn('state: "At risk"', self.record_path().read_text())
        self.assertAccepts(self.check())

    def test_does_not_write_a_state_over_a_draft(self) -> None:
        """A record nobody has assessed gets no state written into it."""
        draft = record(
            state="Needs work", criteria={"B01": "unknown", "B02": "pass", "S01": "pass"}
        )
        self.write_record(draft)
        self.run_script("conformance.py")
        self.assertIn('state: "Needs work"', self.record_path().read_text())

    def test_rejects_archived_when_an_archive_criterion_fails(self) -> None:
        self.write_standard(ARCHIVE_STANDARD)
        self.generate_catalog()
        self.write_record(
            record(
                state="Archived",
                criteria={"A01": "fail", "A02": "pass", "A03": "pass", "A04": "pass"},
            )
        )
        self.assertRejects(self.check(), "state `Archived` requires `A01`-`A04` to be met")

    def test_rejects_archive_candidate_without_its_stated_failures(self) -> None:
        self.write_record(record(state="Archive candidate"))
        self.assertRejects(
            self.check(), "state `Archive candidate` requires `B02` and `B10` to both fail"
        )

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

    # Starting a record -----------------------------------------------------

    def init(self, *arguments: str):
        return self.run_script("conformance.py", "--init", *arguments)

    def test_init_names_every_criterion_in_the_catalog(self) -> None:
        self.assertAccepts(self.init())
        written = (self.repository / ".github" / "conformance.yml").read_text()
        for identifier in ("B01", "B02", "S01"):
            self.assertIn(f"  {identifier}: unknown", written)

    def test_init_records_no_result_of_its_own(self) -> None:
        """A generated file must not be able to pass for an assessment."""
        self.assertAccepts(self.init())
        self.assertRejects(self.check(), "assessed_on `YYYY-MM-DD` is not an ISO date")

    def test_init_produces_a_record_that_validates_once_it_is_filled_in(self) -> None:
        self.assertAccepts(self.init())
        path = self.repository / ".github" / "conformance.yml"
        filled = path.read_text().replace("YYYY-MM-DD", dt.date.today().isoformat())
        filled = filled.replace('state: "Needs work"', 'state: "Healthy"')
        path.write_text(filled.replace(": unknown", ": pass"))
        self.generate_badge()
        self.assertAccepts(self.check())

    def test_init_refuses_to_overwrite_an_existing_record(self) -> None:
        """A record holds an assessment that regenerating it cannot reproduce."""
        self.write_record(record())
        self.assertRejects(self.init(), "will not overwrite it")

    def test_init_carries_the_catalog_version(self) -> None:
        self.assertAccepts(self.init())
        written = (self.repository / ".github" / "conformance.yml").read_text()
        self.assertIn('standard_version: "2.0.0"', written)

    def test_the_published_template_is_not_hand_maintained(self) -> None:
        """The template lists every criterion, so it must be generated, not typed."""
        expected = self.run_script(
            "conformance.py", "--init", "--output", str(self.repository / "generated.yml")
        )
        self.assertAccepts(expected)
        published = (ROOT / "templates" / "conformance.yml").read_text()
        current = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "conformance.py"),
                "--init",
                "--repository",
                str(ROOT),
                "--output",
                str(self.repository / "from-real-catalog.yml"),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertAccepts(current)
        self.assertEqual(
            published,
            (self.repository / "from-real-catalog.yml").read_text(),
            msg=(
                "templates/conformance.yml has drifted from the catalog. Delete it and run "
                "python3 scripts/conformance.py --init --output templates/conformance.yml"
            ),
        )


if __name__ == "__main__":
    unittest.main()
