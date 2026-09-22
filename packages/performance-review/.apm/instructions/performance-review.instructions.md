---
applyTo: "**"
---

<!-- markdownlint-disable MD041 -->

# Performance code review

Review code changes for concrete performance defects, the way a senior engineer
reviews architecture: by reading what the code does and judging whether that is
the right amount of work in the right place. Report only findings you can
justify from the code, or from a measurement you took to confirm one. Do not
report a stylistic preference or a difference too small to matter where it
runs.

- **Complexity.** A loop inside a loop over the same or related data, a lookup
  in a list or array where a set or map would be constant time, a sort inside a
  loop that only needed to happen once, repeated linear scans that could share
  one pass. State the complexity class the code has and the one it could have.
- **Placement.** Work done on every call that only needs to happen once (a
  regex compiled per call, a config re-parsed per request, a connection
  re-established per operation); work done eagerly that could be lazy or
  deferred until actually needed; a cache invalidated or recomputed more often
  than its input changes.
- **Threading and blocking.** Synchronous I/O, a lock held across an I/O call,
  or any unbounded wait on a thread that a user, a frame renderer, or another
  caller is blocked on. On a platform with a documented main or UI thread,
  anything on it that is not fast and bounded.
- **Allocation and copying.** A copy of a large structure where a reference or
  a view would do; repeated allocation in a hot path where reuse is available;
  a data structure sized far larger than what it holds, or resized repeatedly
  instead of once.
- **I/O and queries.** A query or a request issued once per item in a
  collection instead of once for all of them (the N+1 pattern, in any
  language); reading a file or calling a service repeatedly for data that does
  not change within the operation; no batching where the underlying interface
  offers one.
- **Concurrency shape.** Unbounded parallelism where a bound is needed, no
  parallelism where the work is embarrassingly parallel and the cost is real,
  a producer that can outpace a consumer with no backpressure.

## Measuring, when it helps

If `AGENTS.md` documents a command that measures something — a benchmark, a
timed startup script, a memory report, a profiling trace recipe — running it to
confirm a specific finding is welcome. Two rules bound it:

- Run only the documented command, unmodified in what it does. Do not construct
  a new measurement, launch the product outside what that command already does,
  or add instrumentation of your own.
- A measurement supports a finding you can already state from reading the code.
  It never stands alone: "the profiler shows 12% of time here" is not a finding
  without the mechanism that explains it and the correction that would change
  it.

Where no such command exists, review from the code alone and say so; that is a
complete review, not a partial one.

## What is not a finding

- A one-time cost (startup, initialization, a command run by a developer, not a
  user) unless it is large enough to be felt.
- A difference too small to matter next to what the code is doing anyway (an
  allocation inside a function that also makes a network call).
- Correct code that could theoretically be marginally faster with no
  user-facing or resource consequence. This is a review for defects, not a
  request for the fastest possible version of everything.
- A change that trades a small, stated performance cost for clarity, safety, or
  correctness, where the trade is reasonable for what the code does.
