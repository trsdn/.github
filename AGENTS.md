# Agent instructions

Read this before changing anything in this repository.

## What this repository is

`trsdn/.github` publishes two things:

1. the **Repository Quality Standard** in `docs/repository-quality-standard.md`,
   which is the canonical set of criteria that other `trsdn` repositories are
   assessed against; and
2. the **default community health files** that GitHub applies to public `trsdn`
   repositories which do not ship their own.

Both are consumed from outside this repository. A change here can alter the
assessment result of repositories that are not in this checkout, and can change
the contributing, security, and conduct guidance shown to people in repositories
that have never been touched. Treat every change as a public interface change.

## What this repository is not

It is not a product, it does not deploy anywhere, and it ships no runtime code.
The scripts under `scripts/` exist to validate this repository's own content.

## Layout

| Path | Purpose |
|---|---|
| `docs/repository-quality-standard.md` | The standard. Hand-written, authoritative. |
| `standard.yml` | Generated catalog of every criterion. Never hand-edit. |
| `docs/conformance-record.md` | Format of the per-repository assessment record. |
| `docs/self-assessment.md` | This repository's own assessment, with per-criterion notes. |
| `docs/decisions/` | Architectural decision records. |
| `templates/AGENTS.md` | Starting point published for other repositories. |
| `scripts/` | Validation and generation tooling, Python standard library only. |
| `tests/` | Tests for the tooling in `scripts/`, run via `unittest`. |
| `.github/conformance.yml` | This repository's conformance record. |
| `.github/badges/` | Generated badge output. Never hand-edit. |
| `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `SUPPORT.md` | Inherited by other repositories. Write them for *any* repository, never about this one. |

## Validate before proposing a change

Run all four. They are the complete validation for this repository:

```sh
python3 scripts/standard.py --check
python3 scripts/conformance.py --check
python3 -m unittest discover -s tests
npx --yes markdownlint-cli2@0.18.1 "**/*.md"
```

`scripts/standard.py --check` fails when `standard.yml` has drifted from the
Markdown, when a criterion identifier is duplicated or non-contiguous, when a
prefix is not claimed in the register, or when the document version disagrees
with the changelog.

`scripts/conformance.py --check` fails when the badge disagrees with the
conformance record, when a criterion is missing from the record, or when the
record has aged past the review cadence. A red check from ageing is intentional
and means reassessment is due. Regenerating the badge makes it render as stale
but does not clear the check, because only a fresh assessment can.

`tests/` covers both scripts through their command line, asserting the exit code
and the specific diagnostic for each rejection path. When you add or change a
check, add the test that proves it rejects — then disable the check and confirm
the suite goes red. A test that passes either way is not coverage.

## Rules specific to the standard

- **Criterion identifiers are append-only.** Never renumber, reuse, or repurpose
  an identifier. A retired criterion keeps its identifier and gains a retirement
  note. Identifiers are cited from other repositories and from issues; changing
  one silently invalidates those citations.
- **Claim the prefix.** A new section claims its letter in the prefix register in
  the same change.
- **Regenerate, do not edit.** After changing the standard, run
  `python3 scripts/standard.py` and commit the regenerated `standard.yml`.
- **Version and changelog move together.** Adding criteria is a minor bump;
  removing, renumbering, or narrowing a criterion is a major bump. The check
  enforces that the document version matches the newest changelog entry.
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
- Do not create or move Git tags, publish releases, or change repository
  settings, branch protection, or security settings. Those are maintainer
  actions.
- Do not hand-edit `standard.yml` or anything under `.github/badges/`.
- Do not change a conformance record to make a badge look better. The record
  follows the evidence; the badge follows the record.
- Do not renumber existing criteria, including to "tidy up" a gap.
- Do not add dependencies. The scripts use the Python standard library, and
  Markdown linting runs through `npx` with a pinned version.

## Attribution

Agent-authored commits carry a `Co-authored-by` trailer identifying the agent, so
authorship stays visible in history. Every change goes through a pull request;
none is pushed straight to the default branch.
