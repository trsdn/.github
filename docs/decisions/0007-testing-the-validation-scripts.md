# 0007 - Testing the validation scripts

- Status: Accepted
- Date: 2026-08-24

## Context

`scripts/standard.py` and `scripts/conformance.py` decide whether the published
catalog is consistent and whether a conformance record may be trusted. Every
other guarantee in this repository rests on them, and they had no tests. They
were known to work because their failure paths had been walked by hand once.

An unverified checker is worse than no checker. A checker that has silently
stopped rejecting still reports success, and the green check is read as evidence.

## Decision

Both scripts are tested through their command line, not by importing their
internals. The exit code and the diagnostic are the contract CI and maintainers
depend on, so that is what is asserted. Every test that expects a rejection
asserts a non-zero exit *and* the specific message, because a check that fails
for the wrong reason is not working.

Each test builds a small synthetic repository in a temporary directory. This
required both scripts to accept `--repository`, which is the only change made to
production code for testability.

Every check is verified to be load-bearing: disabling it in the script must turn
the suite red. A test that passes whether or not the code works is not coverage.

The tests use `unittest` from the standard library. The repository adds no
dependencies.

## Consequences

Changing a diagnostic message breaks tests. This is intended. The messages are
the interface a maintainer reads at 200 criteria in, and changing them is a
change worth noticing.

The suite runs both scripts against this repository as well as against synthetic
ones, so the published standard must satisfy its own generator.

## The defect this found

Ageing only failed `--check` when the badge *also* disagreed with the record.
Regenerating the badge produced a correct stale rendering and a green check, so
the reminder to reassess could be silenced without reassessing anything. That is
precisely the outcome ADR 0006 was written to prevent.

Ageing is now an independent failure. Regenerating the badge keeps the public
signal honest while it is overdue, but only a fresh assessment clears the check.

## Alternatives considered

**Importing the scripts and testing functions directly.** Rejected. It would test
`validate()` while leaving the argument handling, the exit codes, and the badge
writing — the parts CI actually invokes — unexercised.

**Asserting only the exit code.** Rejected. A script that rejects valid input for
an unrelated reason would pass such a test while being broken.

**Adding `pytest`.** Rejected. `unittest` is sufficient here, and the no-
dependency rule is worth more than the ergonomics.
