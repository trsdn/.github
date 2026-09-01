# 0012 - A repository without a runner is assessed, not excused

- Status: Accepted
- Date: 2026-09-01

## Context

Nine criteria in the standard reach their evidence through a workflow run. Six of
them — `S02`, `S03`, `S04`, `R03`, `R05`, `R07` — plus the continuous integration
badge in `P08` cannot be cleared at all without one.

GitHub-hosted runner minutes are free for public repositories and metered for
private ones. Actions can also be disabled outright, and no self-hosted runner
has to exist. Whether a repository can run a workflow is therefore an account and
configuration question, and it is uncorrelated with how well the repository is
maintained. A private repository with a complete test suite, configured linters,
a documented validation command, and a hand-cut but reproducible release could
reach `Fail` on six criteria and lose a required badge, and nothing in that
result would be about its quality.

The standard already commits to two things that this situation strains. Every
criterion needs evidence a single maintainer can produce, and no criterion may
require tooling the assessed repository does not have. It also commits, in
[decision 0011](0011-criteria-are-decided-by-the-rule-text.md), to criteria that
are decided by their rule text alone. None of the six said what to record when no
runner exists, so each assessor would settle it privately — one recording `Fail`,
another `Not applicable`, a third a `Partial` nobody can clear — and none of
those results would be reproducible from the document at the version cited.

## Decision

The standard states the outcome, in one place, for the case it had left
undecided.

**Runner availability is a property of the repository.** It is established from
the repository's Actions settings and the Actions allowance of the account that
owns it, and recorded in the assessment beside the visibility that `B09` already
makes intentional. It is deliberately not defined as "private", because private
repositories with a minutes allowance or a self-hosted runner are common, and it
is deliberately not inferred from the absence of workflow files, because that
would convert every repository that has simply not set CI up into one that is
excused from it. Where availability is not recorded, the repository has a runner.
That default is the safe one: it leaves the criteria as written.

**The substance is separated from the vehicle.** `S02`, `S03`, and `R05` keep a
reachable `Pass`, because what they are actually about is a test suite, a set of
configured checks, and an artifact exercised in an environment that inherits
nothing. A maintainer can produce all three from a documented `B05` command and
record the run. `R03` and `R07` are capped at `Partial`, because what *they* are
about is the automation itself: a hand-built artifact and hand-copied release
notes are precisely the failures those criteria were written to catch, and
awarding `Pass` for them would empty the criteria out. `S04` is `Not applicable`,
because a matrix across runtimes is not something one maintainer on one machine
can approximate at all.

**The badge is omitted rather than faked.** Where no workflow runs, position
three of the required block is dropped and the remaining badges keep their order.
A committed image standing in for it stays a `Fail`, since an image of a workflow
that never runs is stale from the moment it lands — which is what the existing
prohibition on committed status images was already for.

## Consequences

This is a minor version change. `S04` moves from a reachable `Fail` to
`Not applicable`, which the compatibility table names as minor, and every other
outcome added here is one the previous text left unstated rather than one it
decided differently.

No recorded `Pass` can become a `Fail`, and this time that is a property of the
rule text rather than an assurance in the changelog — the distinction decision
0011 was written about. Reaching `Pass` on any affected criterion previously
required a workflow run. A repository that produced one has a runner, and this
section does not apply to it.

The capped criteria are the deliberate cost. A repository with no runner cannot
reach `Pass` on `R03` or `R07`, and its conformance record will show that
permanently until a runner is made available. That is the honest reading: the
release automation genuinely is absent, the standard says so, and the work that
would clear it is named. A criterion nobody can clear is a defect; a criterion
this repository has chosen not to clear, for a recorded reason, is a result.

The scope is stated by exclusion as well as inclusion. `S09`, `L04`, and `B05`
are named in the rule text as unaffected, with the reason each is unaffected,
because the previous two drafting failures in `P08` both came from leaving a
reader to work out which members of a set a rule reached.
