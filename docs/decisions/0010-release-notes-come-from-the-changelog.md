# 0010 - Release notes are generated from the changelog, and R06 stays as it is

- Status: Accepted
- Date: 2026-08-31

## Context

`R06` asks that release notes describe meaningful changes and upgrade concerns,
and accepts "GitHub release **or** changelog" as evidence. That disjunction is
the hole.

A repository in the estate demonstrated it. It keeps a Keep-a-Changelog file
with an `## Unreleased` section and one dated section per release, and its
release workflow publishes every GitHub release with a hardcoded notes string
describing the artifacts rather than the change. The changelog is never read by
anything. Nothing fails when a tag has no changelog section, and nothing fails
when entries are still sitting under `## Unreleased` at tag time — those entries
ship and then appear in no release notes at all.

Assessed against `R06` as written, that repository passes: a maintained
changelog exists, and it does describe meaningful changes. The criterion was
satisfied by a document nobody consumes while the surface consumers actually
land on said nothing.

## Decision

Add `R07`, requiring that the notes published for a tag are generated from the
changelog entry for exactly that version, enforced by a release gate that fails
when the entry is missing, empty, or still held in an unreleased section.

Leave `R06` unchanged.

## Consequences

Sharpening `R06` was the obvious alternative and was rejected for two reasons.

It buys nothing. Once `R07` holds, boilerplate notes over an unread changelog
cannot pass, because the notes are no longer written separately from the entry.
The combination "exemplary changelog, meaningless release page" is closed by
provenance, not by restating the content requirement more forcefully.

It is expensive. Narrowing a criterion so that a recorded `Pass` could become a
`Fail` is a major change under
[Versioning And Compatibility](../repository-quality-standard.md#versioning-and-compatibility).
Every recorded result in the estate would be invalidated and every repository
would be due for reassessment — to reach an outcome `R07` already reaches as a
minor change, where a recorded result stays valid for the version it names.

So the two criteria divide the work and stay orthogonal. `R06` is about content:
a changelog entry reading "bug fixes" still fails it, and `R07` cannot catch
that, because such an entry is faithfully published. `R07` is about provenance:
whatever the entry says, it is what the consumer receives. Neither subsumes the
other, and keeping them separate means an assessment says which of the two
things is wrong.

The cost is that `R06` still reads permissively in isolation, and a reader who
finds it without `R07` may draw the old conclusion. The prose under the Package
And Release table names the division for that reader, which is the remedy
available without a major bump.

`R07` is deliberately conditional on the second half. A repository that keeps no
unreleased section has nowhere to strand an entry and satisfies that condition by
construction; requiring a guard against a failure mode the repository cannot have
would be evidence theatre, which
[decision 0005](0005-proportionate-accessibility-and-privacy.md) rules out.

This repository already satisfies `R07`: its release workflow extracts the
section for the tag from `CHANGELOG.md`, fails when the extraction is empty, and
publishes that text as the notes body. The unreleased guard was added alongside
this decision so the gate is complete rather than complete-by-absence.

A criterion that mandates automation has to say where the automation comes from,
or every repository invents it again and the estate ends up with as many gates as
it has release workflows. A reference workflow is therefore published as
[`templates/release-notes/`](../../templates/release-notes/) and linked from the
criterion's prose, the same way `templates/AGENTS.md` backs `G01`-`G08` and
`templates/repo-stats/` backs `P09`. It is a starting point, not a mandate:
`R07` asks for the outcome, and a repository that reaches it with a shell script,
a release tool, or a different CI system passes just as well.
