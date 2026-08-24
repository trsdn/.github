# 0005 - Proportionate accessibility and privacy

- Status: Accepted
- Date: 2026-08-22

## Context

The standard covered secrets in the repository but said nothing about the data a
product handles once it runs, and nothing at all about accessibility. A product
could be rated `Healthy` while being unusable by keyboard, or while quietly
sending user content to a third party.

The obvious versions of both sections — WCAG conformance audits, records of
processing, data protection agreements — would be written once and satisfied
never. A criterion nobody can meet produces either a permanent `Fail` that gets
ignored or a dishonest `Pass`.

## Decision

Both sections stay at the level of disclosure and cheap verification.

Accessibility covers keyboard operability, accessible names and roles, contrast
and text sizing, and usable output without colour. `X05` makes stating a known
limitation a `Pass`, because an honest documented gap is more useful to a user
than silence.

Privacy covers what is collected, where it goes, whether telemetry is opt-in,
where data is stored, who else receives it, and how long it is kept. `Y01`
accepts the common case in a single sentence: stores everything locally, contacts
no network service.

Neither section requires a paid tool, an audit, a certification, or legal review.

## Consequences

These criteria will not catch a subtle accessibility defect or a
privacy-by-design flaw. They catch the barriers and the undisclosed data flows,
which is the realistic ceiling for single-maintainer projects and considerably
better than nothing.

## Alternatives considered

**Name WCAG 2.2 AA as a conformance target.** Rejected. Naming a formal target
implies an audit obligation that will not be met, which makes the claim false.

**Require a formal GDPR record of processing.** Rejected as disproportionate for
local-first tools that process no personal data at all.

**Require an automated accessibility scan for web surfaces.** Deferred. It is
cheap where a web surface exists, but the estate has few, and a criterion that is
`N/A` almost everywhere is not worth its maintenance.
