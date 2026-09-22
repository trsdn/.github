---
name: "baseline-setup"
description: "Brings a repository up to the Baseline of the trsdn Repository Quality Standard: description, README, licence, .gitignore, merge policy, dependency declaration, change history, topics and homepage, and a stated owner. Use when starting a new repository, when adopting the standard in an existing one, or when an assessment reports a Baseline gap (B01, B02, B03, B04, B06, B07, B08, B09, B10)."
---

<!-- markdownlint-disable MD041 -->

## What this is for

The Baseline applies to every repository, so its gaps are the ones you hit in
every repository you own. This skill closes them: the script does the parts that
are the same every time, and you do the parts that need reading.

It covers the nine Baseline criteria that had no tooling behind them. It does not
assess a repository — [`repo-assessor`](../../packages/repo-assessor/README.md)
does that — and it does not touch anything outside the Baseline.

## How to use it

Run the audit first. It is read-only and changes nothing:

```sh
python3 scripts/audit.py --repo OWNER/NAME --path /path/to/checkout
```

Add `--json` when you want to work through the results programmatically.

Every criterion comes back as one of four results:

- **`gap`** — something is missing and the fix is unambiguous. Close it.
- **`judgement`** — the script found the shape of an answer but cannot say whether
  it is a good one. Read it yourself and decide.
- **`met`** — nothing to do.
- **`unknown`** — the evidence was not readable, usually because `gh` has no
  session or the checkout was not given. Say so rather than guessing.

## What you do with each result

**`B01` description, `B09` topics and homepage.** Read the README first, then
write the description yourself — one sentence saying what this repository is for,
in the words its README uses. Topics are how the fleet is found, so use terms
that are already used elsewhere in the account rather than inventing new ones.
Apply them with the script, which validates them against GitHub's rules before
it calls the API:

```sh
python3 scripts/apply.py --repo OWNER/NAME \
  --description "..." --topics swift,macos,menu-bar --dry-run
```

Drop `--dry-run` once the values look right. The script never invents a value,
so nothing reaches GitHub that you did not write.

**`B02` README.** The audit only matches words, so treat its answer as a prompt
to read, never as a result. The five parts are purpose, audience, status, setup
or usage, and key links. Write the missing parts in the repository's own voice.
Do not add a heading with nothing under it: an empty section is worse than a
missing one, because it looks answered.

**`B03` licensing.** If the repository is meant to be used by others, add a
licence file. If it is internal or personal, say that in the README in one
sentence. Both satisfy the criterion; silence does not. Never pick a licence for
the maintainer — ask which one.

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
- It does not fix criteria outside the Baseline.
- It does not scan for secrets. `S05` owns that, and a lookalike filename is the
  only thing the audit notices.
