# 0023 - S14 asks for a performance practice, not performance quality

- Status: Accepted
- Date: 2026-09-22

## Context

[Decision 0022](0022-a-performance-agent-reviews-not-only-benchmarks.md) kept
performance review out of the standard: judging whether performance *is good*
has no line an assessor can draw consistently without a baseline this account
does not maintain, and the standard's own rule is that a criterion needs
evidence a single maintainer can produce.

The maintainer still wanted something in the standard, on the same shape `S08`
already uses for dependency triage: not "is the practice good," but "does a
practice exist and is it named." That question has a line: a repository either
names a performance-sensitive path and how it is reviewed, or it does not.

## Decision

Add `S14`: a repository with a performance-sensitive path states which path and
how it is reviewed or measured. The trigger for "performance-sensitive" is
stated as a fixed test (runs per-frame/request/keystroke, sits in a path a user
waits on at startup, scales with unbounded user input, or is already treated as
one by an existing issue or note), so an assessor applies a test rather than a
judgement. A repository with no such path is `Not applicable`.

The practice named can be anything, including
[the performance-review package](../../packages/performance-review/README.md)
run before a merge — that package is cited as one acceptable form, the way `S08`
cites Dependabot as one acceptable form, never as the only one.

## Consequences

- The criterion is decidable the way `S08` and `S10` already are: a fact about
  documentation, not a judgement about code quality.
- Most repositories in this account will record `Not applicable`, honestly,
  because they have no such path. That is expected and correct, not a sign the
  criterion is toothless — `S13` behaves the same way for repositories with no
  untrusted-trigger workflow.
- A repository is never scored on whether its performance is actually
  acceptable. That question stays with `performance-review`, run by choice, and
  outside the graded standard, consistent with 0022.
