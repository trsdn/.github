# Documentation staleness review

A read-only agent that finds documentation stale past the standard's six-month
cadence and unmarked (`T05`), or restated in a way that now disagrees with its
home (`B13`), run on your own machine. It ships as a versioned
[Agent Package Manager](https://github.com/microsoft/apm) package, the same way
as [`apple-hig-review`](../apple-hig-review/README.md) and
[`performance-review`](../performance-review/README.md).

It runs locally and needs no CI, no token, no minutes, and no repository
setting. It edits nothing: it reports what is stale or disagreeing, and leaves
the correction to a person or a writer agent that knows the current facts.

## What it checks, and what it does not

`T05` and `B13` are both precisely defined in the standard, and this package
applies exactly those definitions rather than a general sense of "this reads
old":

- **Stale** means unchanged for six months, carrying no currency marker, and
  contradicted by something in the current repository — not merely old.
- **Restated** means the same command, version, or policy fact hand-written
  in more than one of the README, `AGENTS.md`, the contributing guide, and
  `docs/` — and it is a finding only where the copies now disagree.

It never rewrites anything. Deciding what the corrected text should say needs
knowledge of the current facts this agent does not have; that is a separate
step.

## What is in it

| File | Installed as |
|---|---|
| [`.apm/agents/doc-staleness-reviewer.agent.md`](.apm/agents/doc-staleness-reviewer.agent.md) | The reviewer agent |
| [`.apm/instructions/doc-staleness-review.instructions.md`](.apm/instructions/doc-staleness-review.instructions.md) | The `T05` and `B13` tests, condensed from the standard |
| [`.apm/prompts/doc-staleness-review.prompt.md`](.apm/prompts/doc-staleness-review.prompt.md) | The request to review this repository's documentation |

Nothing in the package is specific to one repository or one language.

## Use it in a repository

1. Install APM once: `brew install apm`.
2. Declare the dependency in the repository's `apm.yml`, pinned to a tag of
   this repository:

   ```yaml
   name: my-repo
   version: 1.0.0
   targets:
     - claude
     - copilot
   dependencies:
     apm:
       - trsdn/.github/packages/doc-staleness-reviewer#v1.25.0
   ```

3. Run `apm install`. It writes the agent, instructions, prompt and rule files
   for each declared target and records them in `apm.lock.yaml`. Commit the
   installed files and the lock file.

## Run it

Ask your agent runtime to follow the installed prompt (in Claude Code, the
installed slash command; in Copilot, the equivalent reusable prompt), or tell
it to act as the `doc-staleness-reviewer` agent against this repository's
documentation. `apm run` runs a script declared in `apm.yml`, not an installed
prompt or agent, so it is not the way to invoke this.

Worth running before a release, or on a schedule you set yourself (this
package has no scheduler of its own — it is a local, on-request review, not a
cron job).

## Versions

Pinned by tag, the same convention as the account's other packages.

## Verified, and not

Installed with `apm` 0.31.0 into an empty repository for the `claude` and
`copilot` targets: it writes the agent, instructions, prompt and rule files for
both, records them in the lock file, and `apm audit` reports no drift. Not
verified: an actual review run against a real repository's documentation.
