# Performance review

A read-only agent that reviews code for performance defects the way a senior
engineer reviews architecture — by reading what the code does and judging
whether that is the right amount of work in the right place — not by comparing
a number against a stored baseline. It ships as a versioned
[Agent Package Manager](https://github.com/microsoft/apm) package, the same way
as [`apple-hig-review`](../apple-hig-review/README.md), so a repository declares
which version it uses and updates by changing the version.

It runs locally and needs no CI, no token, no minutes, and no repository
setting, the same posture as `apple-hig-review`. It edits nothing. Where a
finding would benefit from a number, it may run a measurement command the
repository already documents — never one it invents itself, and never launching
the product outside what that command already does.

## What it is not

Not a benchmark gate that fails a build when a number moves past a threshold.
That is a narrower, noisier tool for repositories with a real hot path worth
tracking continuously, and this account does not have one built yet (see
`docs/decisions/0022-a-performance-agent-reviews-not-only-benchmarks.md` for
why this shape was chosen first). This package is a review: it reads a diff,
judges it, and reports findings the way a code reviewer does — a defect it
found, not a chart it drew.

## What is in it

| File | Installed as |
|---|---|
| [`.apm/agents/performance-reviewer.agent.md`](.apm/agents/performance-reviewer.agent.md) | The reviewer agent |
| [`.apm/instructions/performance-review.instructions.md`](.apm/instructions/performance-review.instructions.md) | What counts as a defect: complexity, placement, threading, allocation, I/O, concurrency |
| [`.apm/prompts/performance-review.prompt.md`](.apm/prompts/performance-review.prompt.md) | The request to review the current branch |

Nothing in the package is specific to one repository or one language; the
categories it reviews apply to any code. What is specific to a repository is
whether it documents a measurement command in `AGENTS.md` — the agent uses one
if it exists and reviews from the code alone if it does not, and both are a
complete review.

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
       - trsdn/.github/packages/performance-review#v1.22.0
   ```

3. Run `apm install`. It writes the agent, instructions, prompt and rule files
   for each declared target (see `apple-hig-review`'s README for exactly which
   paths) and records them in `apm.lock.yaml`. Commit the installed files and
   the lock file.

## Run it

Ask your agent runtime to follow the installed prompt directly (in Claude Code,
the installed slash command; in Copilot, the equivalent reusable prompt), or
tell it to act as the `performance-reviewer` agent against the current branch's
diff. `apm run` runs a script declared in `apm.yml`, not an installed prompt or
agent, so it is not the way to invoke this.

Run it before merging a change to a hot path, or when a change is expected to
affect performance and nobody has looked closely. Put the outcome in the pull
request description. It is not required by any criterion in the standard — it
is an editorial pass, like a second reviewer, not a gate.

## Versions

Pinned by tag, the same convention as `apple-hig-review`: a repository updates
by moving the tag and rerunning `apm install`, and reads the diff of what
changed before trusting the new rules.

## Verified, and not

Installed with `apm` 0.31.0 into an empty repository for the `claude` and
`copilot` targets: it writes the agent, instructions, prompt and rule files for
both, records them in the lock file, and `apm audit` reports no drift. Not
verified: an actual review run against a real diff, or how each agent runtime
behaves when it runs the reviewer, or when it decides to run a documented
measurement command versus reviewing from source alone.
