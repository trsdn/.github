# 0002 - Versioning and citation

- Status: Accepted
- Date: 2026-08-22

## Context

The standard carried a version number in its body and a changelog, but no tags
and no releases, so `1.1` could not be resolved to a commit. Any citation had to
point at the default branch, which changes underneath the citation. A recorded
assessment result could therefore never be reproduced.

## Decision

Semantic versioning with an explicit mapping:

- **major** when a criterion is removed, renumbered, or narrowed so a recorded
  `Pass` could become a `Fail`;
- **minor** when a criterion, profile, or section is added;
- **patch** for wording that does not change meaning.

Adding criteria is minor because a recorded result names the version it was
produced with. The repository does not regress when the standard grows; it
becomes due for reassessment.

Every version is tagged and released. The release workflow refuses to publish
when the tag, the declared version, and the changelog disagree.

Citations use the pinned form, and every criterion carries an anchor matching its
identifier in lower case:

```text
https://github.com/trsdn/.github/blob/v1.2.0/docs/repository-quality-standard.md#s05
```

## Consequences

Every substantive change to the standard now requires a changelog entry and a
version bump, enforced by a check. This is friction on purpose.

## Alternatives considered

**Date-based versioning.** Rejected. It communicates recency but not
compatibility, and compatibility is the question an assessment result depends on.

**Treating added criteria as major.** Rejected. It would make every routine
addition a breaking change and push the major number up without informing anyone,
diluting the signal that matters.

**Section anchors only, without per-criterion anchors.** Rejected once GitHub's
rendering of anchors inside table cells was verified to work. Linking to a
section and asking the reader to search for `S05` is worse when the citation is
the evidence.
