# 0011 - A criterion is decided by its rule text alone

- Status: Accepted
- Date: 2026-08-31

## Context

`P08` failed twice in a row, in two consecutive versions, for the same reason.
Both failures surfaced only when someone actually assessed a repository against
the criterion, and neither was visible while writing it.

In 1.5.1 the badge rule asked for images served from a first-party source
"where practical". The first repository assessed against it recorded `Partial`
and wrote that there was no work available that would clear the criterion. That
was correct: "where practical" names no condition a repository can satisfy, so
the criterion had no reachable `Pass`. A qualifier had been used to cover a case
the author had not decided.

1.6.0 replaced that qualifier with a rule that turns on how a value changes, and
introduced a second hole of a different shape. One bullet named license,
platform, and conformance as qualifying for a committed image; the next granted
a `Pass` to a live third-party image "everywhere else". The three named values
were not "everywhere else", so the text left them with no stated result — not
`Pass`, not `Partial`, not `Fail` — which allowed "may be committed" to be read
as "must be committed". The assessor found both readings, could not settle them
against the document, and settled them against a sentence in the changelog:
"No recorded result can turn into a `Fail` from any of this."

That sentence produced the right answer. It is still the failure. A conformance
record cites a version of the standard, and the reusable check validates against
the document at that tag. A changelog entry is not part of what a later reader
retrieves when they ask what a criterion required, so a result that depends on
one cannot be reproduced from the evidence the record names. The 1.6.1 wording
fix closed the specific hole; it did not stop the next one.

The two holes look different and share a cause. "Where practical" defers a
decision to the assessor. A residual set — "everywhere else" — defers it to
whoever compares two lists and notices which members fall outside both. In each
case the rule described a preference and left the outcome to be inferred.

## Decision

A criterion is decided by the text of the standard at the version being assessed,
and by nothing else.

Concretely, before a criterion or a rule that feeds one is merged:

- Every case the rule names has a stated result. If a rule enumerates values,
  cases, or exceptions, each one resolves to `Pass`, `Partial`, `Fail`, or
  `Not applicable`, and so does everything the enumeration excludes.
- Outcomes attach to a property of the thing assessed, not to a residual set.
  "A value with no first-party image" survives someone extending a list later;
  "everywhere else" does not.
- A permission says it is a permission. Where a rule allows something without
  requiring it, the text says so, because `may` next to an enumeration reads as
  `must` to the next person.
- Where a criterion has a reachable `Pass`, the work that reaches it is
  identifiable from the text. A criterion no repository can clear is a defect,
  not a high bar.
- The changelog explains why a rule changed. It never carries the rule. If the
  changelog entry is needed to decide a result, the rule is not finished.

The rules that follow from this live in `AGENTS.md`, where they are read before
a change rather than after one.

## Consequences

This is a drafting rule, not a criterion. It adds nothing to assess and does not
change any recorded result. It is enforced by review, because no script can tell
a rule that decides a case from one that merely discusses it.

The check that makes it usable is cheap: take the criterion and a plausible
repository, and try to reach a result using only the document at that version. If
that requires an intention the text does not state, the text is not finished.
Both `P08` failures would have been caught by doing this with a licence badge in
hand, which is why the rule is stated as an act of assessment rather than as
advice to write clearly.

It also sets an expectation for how this kind of defect is reported. Both `P08`
holes were found by an assessor who checked the rule instead of adopting a
conclusion, and both were fixed in the standard rather than absorbed into a
repository's record as a `Partial` nobody could clear. An assessment that cannot
reach a result from the text is evidence about the standard, and the standard is
where it goes.
