# Agent instructions

Read this before changing anything in this repository.

## What this repository is

`trsdn/.github` publishes three things:

1. the **Repository Quality Standard** in `docs/repository-quality-standard.md`,
   which is the canonical set of criteria that other `trsdn` repositories are
   assessed against; and
2. the **default community health files** that GitHub applies to public `trsdn`
   repositories which do not ship their own; and
3. the **self-hosted statistics generator** and reusable workflow used for the
   `P09` repository activity card.

All three are consumed from outside this repository. A change here can alter the
assessment result of repositories that are not in this checkout, and can change
the contributing, security, and conduct guidance shown to people in repositories
that have never been touched. Treat every change as a public interface change.

## What this repository is not

It is not a product and it does not deploy anywhere. The validation scripts
under `scripts/` exist to validate this repository's own content;
`scripts/profile_stats/` is reusable runtime tooling for generated SVG
statistics cards.

## Layout

| Path | Purpose |
|---|---|
| `docs/repository-quality-standard.md` | The standard. Hand-written, authoritative. |
| `standard.yml` | Generated catalog of every criterion. Never hand-edit. |
| `docs/conformance-record.md` | Format of the per-repository assessment record. |
| `docs/self-assessment.md` | This repository's own assessment, with per-criterion notes. |
| `docs/decisions/` | Architectural decision records. |
| `templates/AGENTS.md` | Starting point published for other repositories. |
| `scripts/standard.py`, `scripts/conformance.py`, `scripts/links.py` | Validation and generation tooling for the standard, Python standard library only. |
| `scripts/profile_stats/` | Self-hosted GitHub statistics generator; runtime dependency is `requests`. |
| `tests/` | Tests for the tooling in `scripts/`, run via `unittest`. |
| `.github/conformance.yml` | This repository's conformance record. |
| `.github/badges/` | Generated badge output. Never hand-edit. |
| `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `SUPPORT.md` | Inherited by other repositories. Write them for *any* repository, never about this one. |

## Validate before proposing a change

Run the commands in [Validation](README.md#validation). That list is the complete
validation for this repository and lives in one place, so that it cannot drift
from what CI runs.

What each one rejects, and why it exists:

`scripts/standard.py --check` fails when `standard.yml` has drifted from the
Markdown, when a criterion identifier is duplicated or non-contiguous, when a
prefix is not claimed in the register, or when the document version disagrees
with the changelog.

`scripts/conformance.py --check` fails when the badge disagrees with the
conformance record, when a criterion is missing from the record, or when the
record has aged past the review cadence. A red check from ageing is intentional
and means reassessment is due. Regenerating the badge makes it render as stale
but does not clear the check, because only a fresh assessment can.

Adding `--published-tags` makes it also fail when the recorded
`standard_version` has no tag. CI supplies it on the default branch only, since
a version bump is merged before it is tagged; between the merge and the tag that
job is red, and tagging clears it. It is deliberately absent from the local
validation list for the same reason: on a branch that bumps the version, the tag
cannot exist yet.

`scripts/links.py` fails when a relative link points at a file that does not
exist, or at a heading or `<a id>` anchor that does not. Anchors are the reason
it exists: criteria are cited from other repositories as `#s05`, and renaming a
heading breaks those citations silently. External links are deliberately not
checked, because a check that fails for reasons outside this repository is a
check people learn to ignore.

`tests/` covers both scripts through their command line, asserting the exit code
and the specific diagnostic for each rejection path. When you add or change a
check, add the test that proves it rejects — then disable the check and confirm
the suite goes red. A test that passes either way is not coverage.

## Rules specific to the standard

- **A criterion is decided by its rule text alone.** Before merging a criterion
  or a rule that feeds one, take it and a plausible repository and try to reach
  `Pass`, `Partial`, `Fail`, or `Not applicable` using only the document at that
  version. If that needs an intention the text does not state, the text is not
  finished. Every case a rule names has a stated result, and so does everything
  its enumeration excludes; attach the outcome to a property of the thing
  assessed rather than to a residual set like "everywhere else"; say that a
  permission is a permission, because `may` beside a list reads as `must`; and
  never let the changelog carry the rule. See
  [decision 0011](docs/decisions/0011-criteria-are-decided-by-the-rule-text.md),
  which exists because `P08` failed this twice in consecutive versions.
- **Criterion identifiers are append-only.** Never renumber, reuse, or repurpose
  an identifier. A retired criterion keeps its identifier and gains a retirement
  note. Identifiers are cited from other repositories and from issues; changing
  one silently invalidates those citations.
- **Claim the prefix.** A new section claims its letter in the prefix register in
  the same change.
- **Regenerate, do not edit.** After changing the standard, run
  `python3 scripts/standard.py` and commit the regenerated `standard.yml`.
- **Version and changelog move together.** The bump follows
  [Versioning And Compatibility](docs/repository-quality-standard.md#versioning-and-compatibility),
  which is the only place the rules are stated. The check enforces that the
  document version matches the newest changelog entry.
- **Publish the release when the version changes.** Tag the commit that carries
  the new version as `v<version>` and push the tag. The release workflow verifies
  that the tag, `standard.yml`, and the changelog agree, then publishes with the
  changelog entry as the notes. A version that is never tagged cannot be cited by
  pinned reference, which is the whole point of versioning this document. Until
  the tag exists no repository can be assessed against that version, and this
  repository's own record must not name it: `standard_version` must be a
  published tag, and the local check cannot see when it is not. See
  [decision 0011](docs/decisions/0011-criteria-are-decided-by-the-rule-text.md).
- **Every criterion needs evidence a single maintainer can produce.** Do not add
  a criterion requiring a paid tool, an audit, a certification, or a specialist.
- **Do not require tooling that does not exist** in the repositories being
  assessed.

## Rules specific to the inherited community files

`CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, and `SUPPORT.md` are
displayed in *other* repositories. Never write "this repository" meaning this
one, never reference the standard's internals, and never assume a language,
ecosystem, or build tool.

## Do not do these

- Do not rewrite history, force push, or delete branches.
- Do not commit secrets, tokens, or personal data. Push protection is enabled and
  a blocked push means stop and rotate, not retry.
- Do not restate a fact that already has a home elsewhere. Link to it. The
  standard requires this of assessed repositories in `B13`, and this repository
  is not exempt from its own criteria. Generated restatement is fine, because it
  cannot drift; hand-maintained restatement is not.
- Do not change repository settings, branch protection, or security settings.
  Those are maintainer actions.
- Do not hand-edit `standard.yml` or anything under `.github/badges/`.
- Do not change a conformance record to make a badge look better. The record
  follows the evidence; the badge follows the record.
- Do not renumber existing criteria, including to "tidy up" a gap.
- Do not add dependencies to the standard and conformance validation scripts.
  The statistics generator may use its documented runtime dependency; Markdown
  linting runs through `npx` and Ruff through `pip`, both with a pinned version
  and neither declared as a dependency of anything.

## Attribution

Agent-authored commits carry a `Co-authored-by` trailer identifying the agent, so
authorship stays visible in history. Every change goes through a pull request;
none is pushed straight to the default branch.
