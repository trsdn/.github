---
applyTo: "**/*.md"
---

<!-- markdownlint-disable MD041 -->

# Documentation staleness review

Apply the Repository Quality Standard's own definitions, not a general sense of
"this reads old."

## Staleness (T05)

All three must hold for a passage to be a finding:

1. **Unchanged for six months.** `git log -1 --format=%ad -- <path>` on the
   file, or on the passage's git blame range if the file is large and mostly
   current.
2. **No currency marker.** No date, "as of," or status line saying the passage
   is still accurate.
3. **Contradicted by something current.** The manifest, the source tree, a
   newer document, or the repository's actual behavior no longer matches what
   the passage describes.

A passage already marked superseded, deprecated, or archived, with a link to
its replacement, or sitting in an archive directory, is not a finding — that is
what "marked" means, and the standard treats it as compliant, not stale.

## Restatement (B13)

Only three kinds of fact count: a command, a version or supported runtime, and
a policy (reporting, contribution, or licence terms). Only four surfaces count:
the README, `AGENTS.md`, the contributing guide, and `docs/`. A fact stated on
one of those and linked to from elsewhere is not a restatement; only a second
hand-written copy is. Where two copies of the same fact exist, compare them
literally — a version number, a command's exact flags, a stated response time —
and report both outcomes: copies that disagree are a `B13` `Fail`, and copies
that agree are a `B13` `Partial`. Generated or templated restatement (a
badge, a generated table) does not count.

## What is not a finding

- A passage that is old but still accurate. Age alone is not staleness.
- A passage marked as historical, superseded, or archived — that is the
  standard's own escape hatch, not a gap.
- A fact whose currency you cannot verify against something concrete in the
  repository. Report only what you checked, and say what you could not check
  rather than guessing.
