# 0003 - Agent readiness

- Status: Accepted
- Date: 2026-08-22

## Context

AI coding agents are primary contributors across these repositories, but the
standard had no criteria for them. A repository could be rated `Healthy` while an
agent entering it had to rediscover the build command, the validation command,
and the destructive operations on every run.

Seventeen repositories in the estate already had an `AGENTS.md`, with no shared
structure. This repository, which publishes the standard, had none.

## Decision

Agent instructions live in `AGENTS.md` in the repository root: one tool-neutral
file, readable by any agent, not tied to a vendor.

Tool-specific configuration references `AGENTS.md` rather than restating it.
`.github/copilot-instructions.md` in this repository is four sentences and a
pointer.

`AGENTS.md` must name forbidden and high-risk operations explicitly, not merely
describe the happy path. An agent that has not been told that force pushing is
forbidden has not been told anything about it.

The Baseline requires `G01` only, so no repository is forced into the full
section merely by existing. Software, Deployable, and Package repositories
require all of it. Documentation repositories require `G01` and `G03`.

## Consequences

Two files describe agent behaviour, and only one may contain content. Reviewers
must reject additions to tool-specific files that belong in `AGENTS.md`.

## Alternatives considered

**Put the content in `.github/copilot-instructions.md`.** Rejected. It ties the
repository to one vendor's convention, and the estate already uses several tools.

**Maintain both files with the same content.** Rejected. Duplicated instructions
drift, and an agent then follows whichever copy it read. This is the failure mode
`G04` exists to prevent.
