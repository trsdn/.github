---
description: Assess this repository against the Repository Quality Standard and file one remediation issue per gap
---

<!-- markdownlint-disable MD041 -->

Assess this repository with the `repo-assessor` agent, against the standard in
the `trsdn/.github` checkout at $1 (a local path; ask if not given).

1. Confirm you are running locally under the operator's own `gh` session
   (`gh auth status`), not in CI. If there is no authenticated session with
   issue-write access to this repository, stop and say so.
2. Run `python3 <standard checkout>/scripts/assess.py --repo OWNER/NAME --out
   draft/<owner>-<repo>` from this repository's root, and read what it decided
   and what it left undecided.
3. Decide every remaining criterion the standard defines for this repository's
   profiles. Do not skip a criterion and do not ask the operator to decide one.
4. For each `Fail` or `Partial`, de-duplicate against open and closed issues,
   then file or update an issue exactly as the instructions describe.
5. Write a draft `.github/conformance.yml` and `docs/self-assessment.md` under
   `draft/<owner>-<repo>/`, in the record format `docs/conformance-record.md`
   describes, but do not touch the repository's real files.
6. Report: criteria decided, issues filed (with numbers), gaps already tracked,
   and anything you could not decide and why.

Do not open a pull request, edit a source file, or change a repository setting.
