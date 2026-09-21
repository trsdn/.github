# 0017 - How to meet a criterion is published next to the criterion

- Status: Accepted
- Date: 2026-09-21

## Context

The standard defines outcomes and evidence and deliberately does not prescribe a
technology stack. That kept it short and stable, and it left every repository to
work out the same things again. A survey of the account's repositories found the
same secret scan copied into nine repositories, a release job whose certificate
import had drifted in six, CodeQL configured three different ways, and eleven
repositories with no secret scan at all. The best implementation of several
criteria lived in one repository, OpenWritr, and nowhere anyone would look for it.
Assessments also kept finding gaps a worked example would have closed.

Enabling CodeQL across the account showed the cost of leaving this unwritten: the
default setup and a repository's own CodeQL workflow cannot both be on, and no
document said so.

## Decision

Publish the how next to the what, and keep them apart. The standard states what
must be true; guides under `docs/guides/` show how, indexed by criterion; starter
kits under `templates/` hold the files to copy; and reusable workflows under
`.github/workflows/` are called from other repositories where a file has no
per-repository content, so there is no copy to drift.

A guide or template never replaces a criterion and is never evidence that one is
met. Guides link to criteria and do not restate them, on the same reasoning as
`B13`.

Take the material from repositories that already work, not from invention, and
have it reviewed before publishing, because a defect in a template is copied.

## Consequences

- A new repository, or an agent bringing one to the standard, starts from a kit
  and a guide instead of from the criterion text alone.
- A change to a reusable workflow reaches every caller. Inputs stay compatible,
  and a breaking change is published under a tag.
- The material has to be kept true as the platform and the repositories change,
  which is a cost the standard alone did not carry. The review cadence covers it.
- The standard itself stays technology-neutral: nothing here is a criterion.
