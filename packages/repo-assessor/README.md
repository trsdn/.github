# Repository assessor

An agent that assesses a repository against the
[Repository Quality Standard](../../docs/repository-quality-standard.md) and files
one GitHub issue per gap, run on your own machine. It ships as a versioned
[Agent Package Manager](https://github.com/microsoft/apm) package, the same way as
[`apple-hig-review`](../apple-hig-review/README.md), so a repository declares
which version it uses and updates by changing the version.

**This package needs write access, unlike `apple-hig-review`.** Filing an issue
calls `gh issue create`, which needs a `gh` session with issue-write (`repo`)
scope on the target repository. Run it under your own already-authenticated `gh`
session, interactively, on your own machine. It needs no CI, no minutes, and no
dedicated token or repository secret — the credential is the session you already
have, used the way you'd use it by hand. It never opens a pull request, edits a
source file, or changes a repository setting: the only write it makes is `gh
issue create` (or a comment on an existing issue), nothing else.

## What is in it

| File | Installed as |
|---|---|
| [`.apm/agents/repo-assessor.agent.md`](.apm/agents/repo-assessor.agent.md) | The assessor agent |
| [`.apm/instructions/repo-assessor.instructions.md`](.apm/instructions/repo-assessor.instructions.md) | The Remediation Issue Contract shape and the deciding rules, condensed from the standard |
| [`.apm/prompts/repo-assessor.prompt.md`](.apm/prompts/repo-assessor.prompt.md) | The request to assess the repository and file issues |

Nothing in the package is specific to one repository. It reads that repository's
own `AGENTS.md` first, and the standard from wherever you point it at.

## What it does not do

It does not fix anything, and it does not write
[`.github/conformance.yml`](../../docs/conformance-record.md). Assessing and
recording are different acts on purpose: `B11` and `scripts/conformance.py
--check` exist so a generated record cannot pass for one without an assessor
having reasoned about each criterion, and a tool that both finds a gap and marks
it closed is a conflict of interest built into one step. It writes a *draft*
record under `draft/<owner>-<repo>/` instead, for a human or a
[fleet-rollout worker](../../docs/fleet-rollout.md) to review and commit.

## Use it in a repository

1. Install APM once: `brew install apm`.
2. Declare the dependency in the repository's `apm.yml`, pinned to a tag of this
   repository:

   ```yaml
   name: my-repo
   version: 1.0.0
   targets:
     - claude
     - copilot
   dependencies:
     apm:
       - trsdn/.github/packages/repo-assessor#v1.22.0
   ```

3. Run `apm install`. It writes the agent, instructions and prompt for each
   declared target (see `apple-hig-review`'s README for exactly which files),
   and records them in `apm.lock.yaml`. Commit the installed files and the lock
   file.

## Run it

From the repository being assessed, with a `trsdn/.github` checkout on your
machine and `gh auth status` showing a session with issue-write access, ask your
agent runtime to run the installed prompt (in Claude Code, `/repo-assessor
/path/to/trsdn/.github`; in Copilot, the equivalent reusable prompt), or tell it
directly to follow `repo-assessor.prompt.md` and act as the `repo-assessor`
agent. `apm run` runs a script declared in `apm.yml`, not an installed
prompt or agent, so it is not the way to invoke this. It reads
`scripts/assess.py`'s output, decides every remaining criterion itself, and
files one issue per `Fail` or `Partial`, each in the
[Remediation Issue Contract](../../docs/repository-quality-standard.md#remediation-issue-contract)
shape: the criterion, the observed gap, required content, expected evidence,
`Done when`, and exclusions. It searches open and closed issues for the
criterion ID first, so a gap already tracked is not filed twice.

Read its report before acting on it: it names every criterion it could not
decide (an unreadable setting, for example) rather than guessing, and those need
a person, not a filed issue.

## Versions

Pinned by tag, the same convention as `apple-hig-review`: a repository updates by
moving the tag and rerunning `apm install`, and reads the diff of what changed
before trusting the new rules.

## Verified, and not

Installed with `apm` 0.31.0 into an empty repository for the `claude` and
`copilot` targets: it writes the agent, instructions, prompt and rule files for
both (`.claude/agents/repo-assessor.md`, `.claude/commands/repo-assessor.md`,
`.claude/rules/repo-assessor.md`, `.github/agents/repo-assessor.agent.md`,
`.github/instructions/repo-assessor.instructions.md`,
`.github/prompts/repo-assessor.prompt.md`), records them in the lock file, and
`apm audit` reports no drift. Not verified: an actual assessment run and issue
filing against a real repository, and how each agent runtime behaves when it
runs the assessor.
