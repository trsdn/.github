# 0013 - Sites are designed for the project, not assembled from a shared kit

- Status: Accepted
- Date: 2026-09-17

## Context

[Decision 0009](0009-published-sites-and-content-boundaries.md) required every
published site to vendor **Instrument Workshop**, the shared, privately
maintained design language, on the reasoning that a design language earns its
value from consistent use and that contrast, focus, target size, and density
are better decided once than re-litigated per site.

Rebuilding `OpenPromptr`'s site surfaced what that consistency actually cost.
The page carried the same panel chrome, badge shapes, and callout treatment as
every other site built from the same two stylesheets, regardless of what
`OpenPromptr` is — a native macOS teleprompter mirror, not the kind of project
the shared components were shaped around. The result read as competent and
generic at once: correct against `W05`, and indistinguishable from a site for
a different product entirely. A visitor learned nothing about `OpenPromptr`
from the page that the page's own words didn't already say; the design carried
no information.

`W05`'s trade was consistency for distinctiveness, made once for every project
in the estate. That trade was reasonable when it was written and only one or
two sites existed to test it against. It stops being reasonable once "look
like they come from the same hand" is read literally: nine-plus unrelated
products — a teleprompter tool, a scrum aid, a Windows markdown viewer, an
about-me page — sharing one visual identity is not a property a reader values,
it is a signal that nobody spent a design decision on any of them individually.

## Decision

Retire `W05` and `W06` in place, keeping both identifiers per [decision
0001](0001-criterion-identifiers-are-permanent.md). Append `W09`: a site's
visual design must be made for the project it describes, evidenced by a look at
the page rather than a vendored file. The [Site
Design](../repository-quality-standard.md#site-design) subsection replaces the
former Design Language subsection and drops the Instrument Workshop mandate; a
site may still use it where it genuinely fits, but nothing requires it, and
nothing recommends it as the default.

`W07` — no third-party resources, no cookies, no analytics — is untouched. It
was never about the design language; it applies to whatever a site's design
turns out to need.

## Alternatives considered

**Narrow `W05`'s wording in place, rather than retiring it.** Reads where a
reader already looks, and needed no new identifier. Rejected on version impact:
under [Versioning And Compatibility](../repository-quality-standard.md#versioning-and-compatibility),
narrowing a criterion's meaning so that a recorded `Pass` could become a `Fail`
is a major change, and a site that vendored Instrument Workshop in good faith
under the old wording should not have its recorded result invalidated by this
one. Retiring the old criterion and appending a new one buys the same outcome
at a minor bump — the same pattern [decision 0012](0012-history-on-the-default-branch-is-protected.md)
used for the same reason.

**Leave `W05`/`W06` as optional rather than retired.** An optional criterion
with no stated condition for when it applies is not assessable — nothing in
[Baseline](../repository-quality-standard.md#baseline) or elsewhere in this
standard is graded "maintainer's choice", because a result that can't be
wrong isn't evidence of anything. Retiring the pair and stating the new
requirement as `W09` keeps every Published Site criterion falsifiable.

**Replace Instrument Workshop with a second shared design language instead of
removing the requirement.** Would repeat the same trade under a different
name. The actual problem was requiring any one visual identity across
unrelated products, not which identity was required.

## Consequences

Recorded `Pass` results for `W05` and `W06` in any repository's conformance
record stay valid for the standard version they name — [decision
0001](0001-criterion-identifiers-are-permanent.md) and the versioning policy
both hold. Neither criterion is assessed again after this version; a
repository's next conformance pass drops them and picks up `W09`
unassessed, which is due for reassessment rather than a regression.

A site that still vendors Instrument Workshop keeps rendering exactly as
before and is not asked to change; `W09` is not failed by using it, only by a
site with no design intent behind it at all — an unstyled scaffold, a
framework default left untouched, or another project's site carried over
without adapting it. `OpenPromptr`'s rebuilt site, and the reasoning that
produced it, is the worked example `W09` is checked against until a second one
exists.
