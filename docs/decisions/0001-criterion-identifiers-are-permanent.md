# 0001 - Criterion identifiers are permanent

- Status: Accepted
- Date: 2026-08-22

## Context

Version 1.2.0 added four sections at once. Each needed a prefix, and prefixes
were being chosen ad hoc across separate issues, with `L`, `G`, `X`, and `Y` all
claimed independently. `A` was already taken by Archived, which was only noticed
by accident.

At the same time, criterion identifiers had started appearing outside this
repository: in remediation issues, in assessments, and now in conformance
records. `S05` had become something other repositories point at.

Nothing prevented a future edit from renumbering criteria, and nothing recorded
which prefixes were in use.

## Decision

Identifiers are append-only. They are never reused, renumbered, or reassigned to
different content. A criterion that stops applying is marked retired in place and
keeps its identifier.

Prefixes are claimed in a register inside the standard. Adding a section claims
its letter in the same change. `scripts/standard.py --check` fails when a
criterion uses an unclaimed prefix, when an identifier is duplicated, or when
numbering within a prefix is not contiguous from 01.

## Consequences

Retired criteria accumulate as visible dead entries rather than disappearing.
That is the intended cost: a reader can see that `S04` once meant something and
no longer does, instead of finding a hole.

Numbering gaps cannot be tidied up, because tidying is exactly the operation that
breaks external citations.

## Alternatives considered

**Renumber freely and fix citations when they break.** Rejected. Citations live
in repositories and issues that are not in this checkout, so breakage is silent
and unbounded.

**Use content hashes or UUIDs as identifiers.** Rejected. They are stable but
unreadable, and a criterion identifier is meant to be quoted by a human in a pull
request.
