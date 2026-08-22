# 0006 - Conformance record, topic, and badge

- Status: Accepted
- Date: 2026-08-22

## Context

Three related needs appeared together: seeing which repositories are governed by
the standard, seeing a repository's result on its front page, and being able to
reproduce that result later.

The obvious implementation of the second — a hardcoded badge URL pasted into a
README — is the one that fails. Nobody edits a green badge back to `Needs work`
when a workflow is deleted. Within months it asserts something false on a public
front page.

## Decision

The **record** is the source of truth: `.github/conformance.yml`, naming the
standard version, the assessment date, the state, and a result for every
criterion in the catalog.

The **topic** `trsdn-standard` marks a repository as assessed, and nothing more.
It carries no outcome, because a topic asserting quality is a claim nobody
maintains.

The **badge** is generated from the record and committed. No badge value is
editable on its own, so it cannot disagree with the record.

Supporting rules:

- Every criterion appears in the record, including `na`, so that "does not apply"
  stays distinguishable from "was never looked at".
- `Pass` remains a per-criterion result and is never a repository-level state.
  One word with two meanings makes both useless.
- A record older than the review cadence renders as stale. Because the badge is
  committed, the check turns red as the record ages, and a red check means
  reassessment is due.
- No record means no badge. A permanent "unknown" badge would simply be left in
  place.
- No numeric score is derived. The standard assigns state by impact, and a
  percentage would quietly replace that judgement with arithmetic.

## Consequences

CI in every adopting repository will eventually go red purely because time
passed. This is the mechanism, not a defect: it is the only thing that makes an
abandoned assessment visible.

Records are verbose, listing every criterion. Completeness is what makes them
evidence.

## Alternatives considered

**A `Pass` or `Fail` badge maintained by hand.** Rejected. It is the failure mode
this decision exists to prevent.

**A version-bearing topic such as `trsdn-standard-v1`.** Rejected. It goes stale
on every major bump and must be re-applied across the estate by hand.

**Storing the result only in the topic or only in the badge.** Rejected. Neither
can hold per-criterion evidence, and both would become a second source of truth
competing with the record.
