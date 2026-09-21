# 0016 - Public repositories run the free security scanners

- Status: Accepted
- Date: 2026-09-21

## Context

A survey of the account's 87 public repositories found the free GitHub security
settings applied unevenly. Secret scanning and push protection were on in 82,
private vulnerability reporting in 47, Dependabot alerts in 49, Dependabot
security updates in 46, and CodeQL in 5. `P03` and `S05` already ask for the
first two, but nothing asked for dependency alerts or for a code scanner, so the
gap sat outside the standard and nobody was told about it.

All of them cost a public repository nothing. The costs are alerts to triage and
pull requests to review, and those are the work `S08` already asks somebody to own.

## Decision

Add two criteria to the Public profile. `P12` asks that Dependabot alerts and
security updates are enabled, and has no `Not applicable`, because the settings do
not depend on the repository having dependencies. `P13` asks that a code scanner
runs where CodeQL supports a language of the repository, and is `Not applicable`
where none is supported or no runner exists.

Two settings that stay optional: secret scanning of non-provider patterns, which
produces many false alarms, and validity checks, which buy little for repositories
that hold few credentials. Neither is asked for.

Enable the settings on every active, non-fork public repository in the account in
the same change, so the criteria describe what is true and not what is intended.
Forks are excluded because their settings belong to the upstream relationship.

## Consequences

- Alerts and pull requests will now arrive for repositories that had none, and
  `B06` will count an open critical alert against a repository that carried it
  unseen. That is the point, and it is more visible work in the short term.
- The settings are reversible one repository at a time, so a repository that
  finds one unbearable can switch it off and record the result the standard then
  gives.
- Adding criteria is a minor change, so records made against earlier versions
  stay valid and are due for reassessment.
