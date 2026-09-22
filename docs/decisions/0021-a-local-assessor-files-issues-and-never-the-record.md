# 0021 - A local assessor files issues, and never the record

- Status: Accepted
- Date: 2026-09-22

## Context

Bringing the account's repositories to the standard so far has used an ad hoc
fleet-worker prompt: a coordinator hands a Claude Code subagent
`docs/fleet-rollout.md` and it opens pull requests to fix gaps. That works, but
every repository re-derives the same procedure from prose, and there is no
narrower way to just find what is wrong without also committing to fix it
through a pull request.

`apple-hig-review` established that a review agent can be packaged, versioned
with the Agent Package Manager, and run locally with no CI and no credential
beyond the operator's own. Filing a remediation issue is a different kind of
act: it writes to GitHub, so it cannot be credential-free the way a pure review
is. It needs to be said plainly, not hidden behind "it just works."

## Decision

Publish `packages/repo-assessor`: a local, versioned agent that assesses a
repository against the standard, exactly as `docs/fleet-rollout.md` already
directs a worker to, and files one issue per `Fail` or `Partial` using the
standard's own Remediation Issue Contract. It runs under the operator's own
`gh` session, never in CI, never with a dedicated token — the same posture the
fleet procedure already assumes, packaged instead of ad hoc.

It never writes `.github/conformance.yml` or opens a pull request. Assessing and
recording stay separate acts: a tool that both finds a gap and marks the record
as passing it would be the exact conflict `B11` and `scripts/conformance.py
--check` exist to prevent, and `AGENTS.md` already forbids changing a record to
make a badge look better. The package writes a draft record under
`draft/<owner>-<repo>/` for a human or a fleet worker to commit.

## Consequences

- A repository's maintainer, or an agent with only read access to the standard
  and write access to that one repository's issues, can get a full gap list
  without anyone opening a PR on their behalf.
- The package's README states its write requirement as prominently as
  `apple-hig-review`'s states the absence of one, so nobody assumes both
  packages have the same trust boundary.
- The fleet-rollout procedure is not replaced. A worker still opens the fixing
  pull requests and the record; `repo-assessor` is the triage step that can run
  without committing to that.
