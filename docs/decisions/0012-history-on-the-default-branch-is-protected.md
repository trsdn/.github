# 0012 - History on the default branch is protected by its own criterion

- Status: Accepted
- Date: 2026-09-01

## Context

1.9.0 added [Automation Availability](../repository-quality-standard.md#automation-availability),
which records `S09` as `Not applicable` where no runner is available. That
reading is textually correct. `S09` is "Existing required checks protect the
default branch", a required check is something a runner performs, and where no
runner exists there is nothing to require.

But `S09`'s expected evidence is "Branch ruleset or protection settings", and a
ruleset does more than gate on checks. The same settings page also blocks force
pushes and deletion, and neither needs a runner. `S09` was the only criterion
pointing at that page, so once it went `Not applicable` nothing in the standard
asked for the default branch to survive.

`B06` does not close it. It asks that the default branch have "an intentional
merge policy and no unresolved critical alerts", and "anyone may force push and
history may be rewritten" is an intentional policy. The criterion asks for
deliberateness, not for a floor.

The result was that a private repository with no runner could record `Healthy`
with a default branch that could be rewritten over or deleted outright. The
[Remediation Issue Contract](../repository-quality-standard.md#remediation-issue-contract)
already described the shape of the expectation — a `protect main` issue "must
name existing checks, require the branch to be current before merge, and block
force pushes and deletion" — but an example of a well-formed issue is not a
criterion, and nothing carried the second half of that sentence.

This was not a defect introduced by 1.9.0. The gap predates it; 1.9.0 made it
reachable.

## Decision

Append a Baseline criterion, `B16`: the default branch cannot be force-pushed
over or deleted, evidenced by a branch ruleset or classic branch protection.

It sits at the Baseline rather than in the Software profile. A documentation
repository's history is no less worth keeping than a library's, and the setting
costs the same in both.

It is deliberately not named in the Automation Availability results table.
Blocking a force push and a deletion is a property of the repository's settings,
not something a runner does, so it belongs on neither row. That section's
closing paragraph already states that every criterion it does not name is
assessed normally, so `B16` needed no second statement to say so.

Every case it names has a stated result, per
[decision 0011](0011-criteria-are-decided-by-the-rule-text.md). Both settings
blocked is a `Pass`, one of the two is a `Partial`, and neither is a `Fail` —
as is a default branch that no ruleset or protection covers at all. A repository
whose plan offers no such mechanism records `Not applicable` and has to say so
in the evidence its conformance record links to, on the same terms as a missing
runner: an unstated possibility is not evidence, and the sentence has to be
removed when the mechanism becomes available.

Administrator bypass is explicitly out of scope. The person who can lift the
protection is the person who set it, so requiring enforcement against them would
test intent rather than configuration, and would leave the criterion asserting
something about a maintainer that no setting can hold. The setting still binds
every other contributor and every workflow token, which is the exposure the
criterion exists for.

## Alternatives considered

**Do nothing, and record that history protection is out of scope.** Defensible
for a single-maintainer estate, where the maintainer is the only account that
could force push. Rejected because the exposure is not only the maintainer: a
workflow token, a compromised token, an agent, and a future second contributor
all act with write access, and none of them is the person whose judgement the
"deliberately out of scope" argument relies on. The setting that closes it is
two checkboxes, so the cost of the criterion is lower than the cost of writing
down why there is no criterion.

**Narrow `B06` so that an intentional merge policy blocks force pushes and
deletion.** This states the requirement where a reader already looks, and adds
nothing to the catalog. Rejected on version impact. Under
[Versioning And Compatibility](../repository-quality-standard.md#versioning-and-compatibility),
narrowing a criterion's meaning so that a recorded `Pass` could become a `Fail`
is a major change, and a major bump invalidates every recorded result in the
estate: each repository would need reassessment against a version that changed
one criterion. Appending a criterion buys the same protection at a minor bump,
where every existing record stays valid for the version it names and
reassessment happens on the ordinary cadence.

## Consequences

Repositories assessed against 1.9.1 and earlier keep their recorded results;
they gain an unassessed criterion, not a regression. A repository whose default
branch is unprotected will record a `Fail` at its next assessment, which is the
intended outcome and is fixed by two settings.

`S09` is unchanged. It keeps its meaning and keeps its `Not applicable` where no
runner is available. The two criteria now divide the same settings page along
the line that matters: `S09` gates what enters the branch, `B16` keeps the
branch.
