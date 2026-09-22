# 0022 - A performance agent reviews, it does not only benchmark

- Status: Accepted
- Date: 2026-09-22

## Context

The research behind `repo-assessor` (see its worked example and the wider
survey it drew from) also considered a performance package, shaped as a
`perf-baseline-reviewer`: run the repository's own benchmark, compare it
against a committed, versioned baseline file, and flag only a regression past a
stated tolerance that persists across repeated samples. That shape is real
prior art and avoids the flakiness a zero-tolerance gate produces, but it needs
a maintained baseline convention this account does not have, and it only
catches what a benchmark already measures.

The maintainer's actual request was narrower and more useful at this account's
current scale: a review, the way a senior engineer reads a diff for
architecture problems, not a number compared against a stored one. Most
performance defects — an accidentally quadratic loop, an N+1 query, work done
on the wrong thread, a copy where a reference would do — are visible from the
code, the same way most architecture defects are, before any benchmark would
even run.

## Decision

Publish `packages/performance-review` as a review agent, in the same
credential-free, local, versioned shape as `apple-hig-review`: it reads a diff
and its surrounding code, judges whether the work is the right amount in the
right place, and reports findings with severity, location, rationale, and
correction — `apple-hig-review`'s own finding format, because it already works
and gives the two packages one voice.

It may run a measurement the repository already documents (a benchmark, a
timed script, a profiling trace) to support a specific finding, but never to
replace reading the code, and never a measurement it invents itself. This is
deliberately not the `perf-baseline-reviewer` shape: no stored baseline file, no
threshold, no regression gate. That shape stays a candidate for later, once a
specific repository has a hot path worth tracking continuously and a maintainer
decides the baseline convention for it.

## Consequences

- The package is useful immediately, without any repository first adopting a
  baseline file or a benchmark suite; it reviews from source alone where
  neither exists.
- It will miss a regression that is only visible at runtime and not evident
  from the code — the class of defect a baseline-and-threshold tool exists for.
  That gap is accepted for now rather than building a heavier tool nothing yet
  needs.
- If a repository later wants continuous regression tracking, that is a
  separate package built against a stated baseline convention, not a mode this
  one grows into.
