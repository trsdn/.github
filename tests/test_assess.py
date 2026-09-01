"""Tests for scripts/assess.py.

The script exists to remove transcription from an assessment, not judgement. So
these tests pin down both halves of that: the results it derives from a fact are
correct, including the graduated `S12` table, and the results it cannot derive
stay `unknown` in a draft that still cannot pass for an assessment.

Every case runs the command line against a facts file, so no test touches the
network and the contract asserted is the one a maintainer uses.
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

from support import ROOT, SCRIPTS


def facts(**overrides) -> dict:
    """A minimal, passing set of facts that each test bends into one shape."""
    base = {
        "repository": "trsdn/example",
        "collected_on": "2026-01-01",
        "owner": "trsdn",
        "private": False,
        "archived": False,
        "description": "An example repository.",
        "homepage": "",
        "topics": ["trsdn-standard"],
        "default_branch": "main",
        "licence": "MIT",
        "truncated_tree": False,
        "paths": ["README.md", "AGENTS.md", ".github/conformance.yml"],
        "contents": {},
        "community_files": {},
        "secret_scanning": "",
        "protection": {
            "visible": False,
            "required_checks": [],
            "force_pushes": False,
            "deletions": False,
        },
    }
    base.update(overrides)
    return base


def workflow(body: str, name: str = "ci.yml") -> dict:
    return {f".github/workflows/{name}": body}


class AssessTests(unittest.TestCase):
    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.directory = pathlib.Path(directory.name)

    def assess(self, data: dict) -> tuple[dict[str, str], str]:
        """Run the script and return the drafted results and the notes."""
        source = self.directory / "facts.json"
        source.write_text(json.dumps(data), encoding="utf-8")
        out = self.directory / "out"
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "assess.py"),
                "--facts",
                str(source),
                "--out",
                str(out),
                "--repository",
                str(ROOT),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(
            result.returncode,
            0,
            msg=f"expected a zero exit. Output:\n{result.stdout}{result.stderr}",
        )
        record = (out / "conformance.yml").read_text(encoding="utf-8")
        drafted = {}
        for line in record.splitlines():
            if line.startswith("  ") and ":" in line:
                key, _, value = line.strip().partition(":")
                drafted[key] = value.strip()
        return drafted, (out / "assessment.md").read_text(encoding="utf-8")

    # -- the draft must not be able to pass for an assessment ---------------

    def test_the_draft_keeps_the_placeholder_date(self) -> None:
        """A generated file must not read as a record a person produced."""
        source = self.directory / "facts.json"
        source.write_text(json.dumps(facts()), encoding="utf-8")
        out = self.directory / "out"
        subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "assess.py"),
                "--facts",
                str(source),
                "--out",
                str(out),
                "--repository",
                str(ROOT),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertIn('assessed_on: "YYYY-MM-DD"', (out / "conformance.yml").read_text())

    def test_criteria_it_cannot_decide_stay_unknown(self) -> None:
        drafted, notes = self.assess(facts())
        self.assertEqual(drafted["B02"], "unknown", "a README's content is not machine-decidable")
        self.assertEqual(drafted["S02"], "unknown", "test coverage is not machine-decidable")
        self.assertIn("`B02`", notes.split("## Left to a person")[1])

    # -- S12, whose table is the point ------------------------------------

    def test_an_outside_action_referenced_by_tag_fails(self) -> None:
        drafted, notes = self.assess(facts(contents=workflow("jobs:\n  uses: someone/act@v3\n")))
        self.assertEqual(drafted["S12"], "fail")
        self.assertIn("someone/act@v3", notes)

    def test_an_outside_action_pinned_by_sha_passes(self) -> None:
        reference = "someone/act@" + "a" * 40
        drafted, _ = self.assess(facts(contents=workflow(f"jobs:\n  uses: {reference}\n")))
        self.assertEqual(drafted["S12"], "pass")

    def test_a_github_action_may_use_a_major_version_tag(self) -> None:
        drafted, _ = self.assess(facts(contents=workflow("jobs:\n  uses: actions/checkout@v7\n")))
        self.assertEqual(drafted["S12"], "pass")

    def test_a_workflow_in_the_same_account_may_use_a_branch(self) -> None:
        """The third row of the table is a permission, so the script must honour it."""
        drafted, _ = self.assess(
            facts(contents=workflow("jobs:\n  uses: trsdn/.github/.github/workflows/x.yml@main\n"))
        )
        self.assertEqual(drafted["S12"], "pass")

    def test_a_branch_reference_outside_the_account_still_fails(self) -> None:
        drafted, _ = self.assess(
            facts(contents=workflow("jobs:\n  uses: other/.github/.github/workflows/x.yml@main\n"))
        )
        self.assertEqual(drafted["S12"], "fail")

    # -- S11 ---------------------------------------------------------------

    def test_a_workflow_without_permissions_is_partial_when_another_has_them(self) -> None:
        contents = workflow("permissions:\n  contents: read\n", "a.yml")
        contents.update(workflow("jobs:\n  build:\n", "b.yml"))
        drafted, notes = self.assess(facts(contents=contents))
        self.assertEqual(drafted["S11"], "partial")
        self.assertIn("b.yml", notes)

    def test_no_workflows_makes_the_workflow_criteria_not_applicable(self) -> None:
        drafted, _ = self.assess(facts(contents={}))
        self.assertEqual(drafted["S11"], "na")
        self.assertEqual(drafted["S12"], "na")

    # -- S13 ---------------------------------------------------------------

    def test_an_untrusted_trigger_reading_a_secret_fails(self) -> None:
        body = (
            "on:\n  pull_request_target:\njobs:\n  a:\n    env:\n      T: ${{ secrets.DEPLOY }}\n"
        )
        drafted, notes = self.assess(facts(contents=workflow(body)))
        self.assertEqual(drafted["S13"], "fail")
        self.assertIn("DEPLOY", notes)

    def test_an_untrusted_trigger_reading_no_secret_passes(self) -> None:
        body = "on:\n  pull_request_target:\njobs:\n  a:\n    env:\n      T: ${{ secrets.GITHUB_TOKEN }}\n"
        drafted, _ = self.assess(facts(contents=workflow(body)))
        self.assertEqual(drafted["S13"], "pass")

    # -- metadata ----------------------------------------------------------

    def test_a_missing_topic_fails_b12(self) -> None:
        drafted, _ = self.assess(facts(topics=[]))
        self.assertEqual(drafted["B12"], "fail")

    def test_a_missing_record_fails_b11(self) -> None:
        drafted, _ = self.assess(facts(paths=["README.md"]))
        self.assertEqual(drafted["B11"], "fail")

    def test_a_private_repository_makes_the_public_profile_not_applicable(self) -> None:
        drafted, _ = self.assess(facts(private=True))
        self.assertEqual(drafted["P01"], "na")
        self.assertEqual(drafted["P06"], "na")

    def test_a_public_repository_without_a_licence_fails(self) -> None:
        drafted, _ = self.assess(facts(licence=""))
        self.assertEqual(drafted["P01"], "fail")
        self.assertEqual(drafted["B03"], "fail")

    def test_a_private_repository_without_a_licence_is_left_to_a_person(self) -> None:
        """`B03` accepts an internal-use statement, which the script cannot read."""
        drafted, _ = self.assess(facts(private=True, licence=""))
        self.assertEqual(drafted["B03"], "unknown")

    def test_a_security_policy_in_the_tree_is_not_reported_missing(self) -> None:
        """The community profile has no `security` key, so absence proves nothing."""
        drafted, _ = self.assess(
            facts(paths=["SECURITY.md"], community_files={"readme": True, "license": True})
        )
        self.assertEqual(drafted["P03"], "unknown")

    def test_no_security_policy_anywhere_fails(self) -> None:
        drafted, _ = self.assess(
            facts(paths=["README.md"], community_files={"readme": True, "license": True})
        )
        self.assertEqual(drafted["P03"], "fail")

    # -- B16 is decided by two settings, and only when they are visible -----

    def test_a_branch_that_blocks_both_settings_passes_b16(self) -> None:
        drafted, _ = self.assess(
            facts(
                protection={
                    "visible": True,
                    "required_checks": ["Tests"],
                    "force_pushes": False,
                    "deletions": False,
                }
            )
        )
        self.assertEqual(drafted["B16"], "pass")

    def test_a_branch_that_permits_one_setting_is_partial(self) -> None:
        drafted, _ = self.assess(
            facts(
                protection={
                    "visible": True,
                    "required_checks": ["Tests"],
                    "force_pushes": True,
                    "deletions": False,
                }
            )
        )
        self.assertEqual(drafted["B16"], "partial")

    def test_a_branch_that_permits_both_settings_fails_b16(self) -> None:
        drafted, _ = self.assess(
            facts(
                protection={
                    "visible": True,
                    "required_checks": ["Tests"],
                    "force_pushes": True,
                    "deletions": True,
                }
            )
        )
        self.assertEqual(drafted["B16"], "fail")

    def test_invisible_protection_leaves_b16_to_a_person(self) -> None:
        """A 404 cannot tell a ruleset, an unprotected branch, and no plan apart."""
        drafted, _ = self.assess(facts())
        self.assertEqual(drafted["B16"], "unknown")


if __name__ == "__main__":
    unittest.main()
