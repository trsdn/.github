# 0015 - The assessor decides, including which gaps are intended

- Status: Accepted
- Date: 2026-09-20

## Context

[0014](0014-release-and-pinning-criteria-scale-with-what-they-protect.md) made
assessment something an AI agent normally performs. That moved the problem
rather than solving it. Two things still needed a person:

- `R05` asked that somebody install the published artifact, launch it and use
  its core function. For an interface that needs an operator that step cannot be
  automated, so the criterion could not be met without the maintainer.
- A gap the maintainer had a good reason for could be recorded only as a
  `Partial` with a rationale, and the standard did not say which reasons were
  good. An agent had to ask, or guess, and the maintainer was left to rule on
  every exception.

The aim is a standard where an agent can reach every result alone and the
maintainer sees an exception only when they choose to dispute one.

## Decision

Add [Deciding Without The Maintainer](../repository-quality-standard.md#deciding-without-the-maintainer)
to Assessment. It fixes the order of questions an assessor asks, the small set of
reasons that make a deviation intended, and what each reason yields. An intended
deviation that the criterion's own text does not allow is a `Partial`, kept
visible and not counted against the state. The critical and high-priority gaps
already listed under the state table are never excused by intent, so the
mechanism cannot be used to wave through committed secrets or an unreproducible
release.

Rework `R05` around a smoke kit, a documented command an agent can run against
the published artifact, with a table of results that says when the criterion is
`Pass` and when it is not. Operating the core function is dropped as a
requirement. `D03` asks for a runnable health command instead of a rehearsed
rollback.

Then go through every criterion, not only the ones that had been noticed. An
audit of all 104 found that none needs a human and that two need a documented
procedure in the repository, but that two thirds left the boundary between
`Partial`, `Fail` and `Not applicable` unstated, and that eight contradicted the
text around them. The fix is default results for the general cases, a computed
overall state, and a per-criterion correction wherever the default is wrong or
insufficient.

The corrections may only clarify or widen, so that no recorded `Pass` weakens. A
review of the merged result caught a dozen places where a clarification had
narrowed a criterion, and each was reworded.

## Consequences

- An agent can finish an assessment without asking, and the result is reproducible
  because the reasons and their checks are written down.
- The list of intended reasons is closed. A reason not in the table is not one,
  so the standard stays enforceable and the exceptions do not multiply.
- A maintainer who disagrees disputes the result in an issue, as before. The cost
  moves from approving every exception to reading the ones they disagree with.
- Repositories whose smoke check was a manual record now need a kit, or the stated
  limit for an artifact that cannot be checked unattended.
