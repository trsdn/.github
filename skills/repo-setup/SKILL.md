---
name: "repo-setup"
description: "Audits a repository against the Baseline and Public criteria of the trsdn Repository Quality Standard and applies the mechanical fixes: description, README, licence, .gitignore, merge policy, dependency declaration, change history, topics, homepage, owner, and the community files GitHub recognises. Use when starting a repository, adopting the standard in an existing one, or closing a reported gap in B01-B04, B06-B10, P01, P02, P04, P05, P06 or P07."
---

<!-- markdownlint-disable MD041 -->

## What this is for

The Baseline applies to every repository and the Public criteria to every public
one, so their gaps are the ones you hit in every repository you own. This skill
closes them: the script does the parts that are the same every time, and you do
the parts that need reading.

It both **assesses** and **does**. The audit is the same judgement the standard
asks for, and the apply step performs only what you decided. It is not a
replacement for [`repo-assessor`](../../packages/repo-assessor/README.md), which
decides every criterion and files issues; this covers fifteen of them and fixes
what it can.

## How to use it

Audit first. It is read-only and changes nothing:

```sh
python3 scripts/audit.py --repo OWNER/NAME --path /path/to/checkout
```

The Public criteria are checked automatically when `gh` reports the repository
public; `--public` forces them. `--json` gives machine-readable output.

Every criterion comes back as one of four results:

- **`gap`** — something is missing and the fix is unambiguous. Close it.
- **`judgement`** — the script found the shape of an answer but cannot say whether
  it is a good one. Read it yourself and decide.
- **`met`** — nothing to do.
- **`unknown`** — the evidence was not readable, usually because `gh` has no
  session or the checkout was not given. Say so rather than guessing.

## What you do with each result

**`B01` description, `B09` and `P07` topics and homepage.** Read the README
first, then write the description yourself — one sentence saying what this
repository is for, in the words its README uses. Topics are how the fleet is
found, so use terms already used elsewhere in the account rather than inventing
new ones. Apply them with the script, which validates them against GitHub's
rules before it calls the API:

```sh
python3 scripts/apply.py --repo OWNER/NAME \
  --description "..." --topics swift,macos,menu-bar --dry-run
```

Drop `--dry-run` once the values look right. The script never invents a value,
so nothing reaches GitHub that you did not write.

**`B02` README, and `P05` for a public repository.** The audit only matches
words, so treat its answer as a prompt to read, never as a result. `B02` wants
purpose, audience, status, setup or usage, and key links. `P05` wants install,
configuration, examples, compatibility, security, and support status — one
sentence or one link each is enough. Write the missing parts in the repository's
own voice, and never add a heading with nothing under it: an empty section is
worse than a missing one, because it looks answered.

**`B03` licensing, and `P01` for a public repository.** A public repository needs
an OSI-approved licence GitHub can detect, which means the licence text
unmodified — an edited one stops being detected and the criterion fails on a file
that looks right. A private or internal repository satisfies `B03` with a
sentence in the README instead. Never pick a licence for the maintainer: ask.

**`B04` ignored state.** If the audit reports a committed secret, stop. Tell the
maintainer which file it is and what it unlocks, and do not delete it, rewrite
history, or rotate anything yourself. Otherwise add only the ignore patterns this
repository's ecosystem actually produces.

**`B06` merge policy.** One sentence saying how a change reaches the default
branch — through a pull request, or directly by the maintainer. State what is
true, not what sounds rigorous. Alerts are the other half, and where the API is
unreadable, say so rather than recording a pass.

**`B07` dependencies.** A manifest satisfies this. A repository with no
dependencies is `Not applicable`, and the evidence should say what was looked
for. Do not add a manifest to a repository that does not need one.

**`B08` change history.** A changelog, releases, decision records, or linked
issues all satisfy this. Check which one this repository already uses before
adding a file; an unused `CHANGELOG.md` that stops being updated is a liability,
not evidence.

**`B10` ownership.** One line naming who maintains it and whether it is active.
"Unmaintained" is a valid answer and a useful one.

**`P02` and `P04` contribution, conduct and intake.** These are usually already
met by inheritance: a public repository with no files of its own inherits them
from the account's `.github` repository, and the audit says which it found and
where. Do not copy an inherited file into a repository to make it look local —
that is a hand-maintained restatement, and `B13` grades it.

**`P06` recognition.** GitHub's community profile decides this, so a file it does
not recognise is usually misnamed or in the wrong directory rather than missing.
One known quirk: the API reports no issue template even when the repository
inherits forms from the account. The audit says so where it applies, and that
note is not a gap.

## Rules

- **Read before writing.** Every judgement here depends on what the repository
  already says. A description that contradicts the README is worse than none.
- **Never change a setting that affects access.** Visibility, collaborators,
  branch protection and archiving are the maintainer's, not yours. Report them.
- **Never commit.** Leave changed files in the working tree and say what you
  changed, so the maintainer reviews before anything lands.
- **Say what you could not do.** A criterion you skipped, and why, is worth more
  than a confident answer built on evidence you could not read.
- **One repository at a time.** The audit takes a single `--repo`, deliberately:
  a sweep that writes descriptions across a fleet in one pass is how every
  repository ends up sounding the same.

## What it deliberately does not do

- It does not decide a conformance result or write a conformance record.
- It does not fix criteria outside the Baseline and the Public section.
- It does not scan for secrets. `S05` owns that, and a lookalike filename is the
  only thing the audit notices.
