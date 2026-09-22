---
name: "release-hygiene"
description: "Checks that package metadata agrees with the repository's own, that a versioning and compatibility policy is documented, and that the latest release notes describe what changed and what a consumer must do about it. Covers R01, R02 and R06 of the trsdn Repository Quality Standard. Use before cutting a release, or when an assessment reports a release gap."
---

<!-- markdownlint-disable MD041 -->

## What this is for

A release is the moment a repository stops being private to its maintainer.
These three criteria are about what a consumer sees at that moment: what the
package claims to be, what the version number promises, and what the notes say
changed.

They drift quietly, because nothing breaks when they do. A description edited on
GitHub and not in the manifest leaves two answers to "what is this?", and the
one users see is whichever surface they found first.

## How to use it

```sh
python3 scripts/audit.py --repo OWNER/NAME --path /path/to/checkout
```

Read-only. `--json` gives machine-readable output. `R01` and `R06` are assessed
on the latest *published* release, as the standard requires, so the release is
read through `gh` rather than guessed from the tree.

## What each result asks of you

**`R01` metadata agrees.** The audit compares the manifest's description,
licence and repository URL against what GitHub holds, and shows the character
where they first differ rather than two strings that look identical for their
first fifty characters. Decide which is right and change the other. Where a
disagreement is deliberate — a package name that differs from the repository
name, say — that is a thing to state, not to leave for a reader to trip over.

`R01` is about *where the metadata lives*, not whether it exists. SwiftPM has no
field for a licence, a description, or a repository URL, so for a Swift package
the audit reads the artifact's own `Info.plist` instead, and the criterion is met
by that. Keys ending in `UsageDescription` are consent strings shown to a user
and are deliberately ignored: they are not a description of the product.

**`R02` versioning policy.** Naming SemVer is enough on its own, because SemVer
defines what breaking means. Any other scheme needs one sentence saying what a
consumer can rely on across versions. The audit finds the mention; whether the
sentence carries a promise is yours to read.

**`R06` release notes.** Two failures the audit separates: notes that are empty,
and notes that carry only an auto-generated changelog link. A link to a list of
commits is not a description of what changed — it is the work of describing it,
handed to the reader.

Where the notes do describe changes, the audit reports whether they mention an
upgrade concern. That is not automatically a gap: if nothing needed action from a
consumer, saying nothing is correct. If something did — a removed option, a
changed default, a new minimum version — it belongs in the notes and not only in
the diff.

## Rules

- **Write notes for the person upgrading**, not for the person who wrote the
  code. "Fixed a bug in the parser" tells a consumer nothing about whether it
  affected them.
- **Check the release, not the changelog.** These criteria are assessed on what
  was published. A perfect `CHANGELOG.md` behind an empty release body still
  fails `R06`, because the release is what a consumer sees.
- **Never edit a published release to fix history.** Correct it going forward,
  and say so in the next release.
- **Never commit.** Leave manifest changes in the working tree for review.
