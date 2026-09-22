# 0025 - A kit customizer verifies its markers by running them

- Status: Accepted
- Date: 2026-09-22

## Context

The starter kits under `templates/` are deliberately generic, marked with
`TODO(name)` or `# EDIT: ...` wherever a value depends on the specific
repository adopting them. Three pilots bringing real repositories to the
standard found exactly what an unfinished marker costs: a SwiftLint rule the
installed tool version had renamed, a starter rule set that failed the moment
it ran against real code, a smoke-test workflow whose permissions did not
match the order it actually ran in. None of these were defects in the kit —
they were the customization step nobody had done yet, and each cost a pilot
real time rediscovering it by hand.

The maintainer's request was for an agent that performs exactly that step:
looks at the real repository and tunes the copied kit to it, the way a
capable engineer adopting the kit by hand would.

## Decision

Publish `packages/kit-customizer`, a local writer package in the same shape
as `frontend-designer`: it edits the copied kit files in the working tree and
never commits or opens a pull request itself. Its distinguishing rule is that
it verifies a marker's resolution by running the thing it configures —
building, testing, or linting with the trimmed configuration — rather than
resolving markers by reading code and reasoning about the answer, wherever a
command exists to check it. Where no such command exists or the value cannot
be determined safely, it leaves the marker in place with a note, rather than
filling it with something merely plausible.

This mirrors the kit's own ratchet principle for lint rules (every rule in
the set is true today, so a later violation is a regression) by applying it
during adoption instead of leaving it for the first CI failure to discover.

## Consequences

- Adopting a kit becomes a run of the customizer plus a review, instead of a
  manual pass through every `TODO(...)` and `# EDIT: ...` marker.
- The account's kits stay generic on purpose; nothing here pushes them toward
  encoding every repository's specifics, because the customizer's job is
  exactly to bridge that gap per adoption.
- A verified marker is stronger evidence than a reviewed one, but the package
  still leaves what it cannot verify for the operator — it does not trade
  honesty about uncertainty for a complete-looking result.
