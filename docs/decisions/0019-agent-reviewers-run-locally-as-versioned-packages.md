# 0019 - Agent reviewers run locally, as versioned packages

- Status: Accepted
- Date: 2026-09-21

## Context

The Apple Human Interface Guidelines review was built in OpenWritr as an agentic
workflow: a pull request renders the app's screens on a macOS runner, and an agent
reviews them and posts a comment. Copying it to other apps meant a compile step for
a generated lock file, an agent token per repository, a macOS runner, and a
reviewer that reads its own rules from the pull request under review. That is a lot
of machinery, and none of it works in a private repository without minutes.

The review is also cheap to run locally, by the same agent that made the change.

## Decision

Run agent reviewers locally, on request, and not as workflows. Publish the agent,
its rules and its request as a versioned package for the Agent Package Manager
(`packages/`), so a repository declares a version pinned to a tag, installs it
with one command, and updates it by changing the version. Keep everything specific
to an app out of the package: the app's own `AGENTS.md` says what kind of app it is,
what data it handles and how to render its screens.

Remove the agentic workflow from the macOS kit.

## Consequences

- The review costs no minutes, no token and no repository setting, and works in a
  private repository.
- Nothing forces it to run. It is run by whoever makes a UI change, because the
  procedure says so, and its outcome is written in the pull request description.
- The package depends on a tool the account does not use yet. Its first
  installation is its test, and until then the package is documented as
  unverified.
- A later agent reviewer follows the same pattern: a package, pinned to a tag,
  run locally.
