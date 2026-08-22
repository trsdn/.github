# Self-Assessment: trsdn/.github

- Standard version: 1.2.0
- Assessed on: 2026-08-22
- State: **Needs work**
- Record: [`.github/conformance.yml`](../.github/conformance.yml)

This repository publishes the standard, so it assesses itself against it. The
result is deliberately not `Healthy`: one criterion fails and four are partial.
Publishing a green badge over known gaps would make every other badge in the
estate worthless.

## Profiles

| Profile | Applies | Rationale |
|---|---|---|
| Public | Yes | Public visibility |
| Software | Yes | `scripts/` executes script code, and the standard's Software profile covers scripts |
| Deployable | No | Nothing is deployed anywhere |
| Package | Yes | The standard is published as tagged releases |
| Documentation | Yes | The primary product is documentation |
| Archived | No | Actively maintained |

## Gaps

### S02 — Automated tests cover important behavior and failure paths — `fail`

`scripts/standard.py` and `scripts/conformance.py` are the checks that everything
else relies on, and neither has a single test. Their failure paths — a duplicated
identifier, an unclaimed prefix, a missing criterion, a stale record — are
exactly the cases that must work, and today they are only known to work because
they were run by hand once.

An unverified checker gives a false sense of safety, which is worse than no
checker. This is the highest-priority gap in the repository.

Remediation: table-driven tests over crafted inputs for each failure path, run
in CI.

### S03 — Static checks run automatically — `partial`

Markdown is linted in CI. The Python scripts are not linted, formatted, or
type-checked by anything. Evidence exists for one language and not the other.

### S09 — Required checks protect the default branch — `partial`

Branch protection is in place and is stronger than the baseline requires: linear
history, no force pushes, no deletions, required conversation resolution, and
required status checks that must be current before merge.

It is `partial` only because the two new checks added in this version —
`Standard consistency` and `Conformance record` — are not yet in the required
set. Until they are, the checks that guard the standard's integrity can be
merged past.

### P04 — Issue and pull-request intake is structured — `partial`

Issue forms and a pull-request template exist. There is no
`ISSUE_TEMPLATE/config.yml`, so blank issues bypass the forms entirely and the
structure is advisory rather than enforced.

### T02 — Internal links and generated output are validated — `partial`

Markdown lint runs, but nothing checks that links resolve. This document set now
contains many cross-references between the standard, the record format, the
decisions, and the templates. A broken link between them is currently invisible
to CI.

## Not applicable

**Deployable `D01`-`D06`.** Nothing is deployed. There is no target, no
environment, no secret store, and no rollback path, because there is no running
system.

**Product Identity `I01`-`I06`.** No artifact is built, installed, or run. There
is no bundle, binary, image, or package to embed identity metadata into. Note
that `I06` — identity is produced by the build, not by hand — is nonetheless
applied by analogy in `P08` and in the badge tooling.

**Accessibility `X01`-`X03`, `X05`.** No user interface ships. `X04` does apply:
the scripts print plain text with no colour and no Unicode decoration, so their
output survives any terminal, pipe, or log.

**Privacy `Y03`-`Y06`.** No telemetry, no user data, no storage, no retention,
because nothing runs. `Y01` and `Y02` do apply and are answered: this repository
collects nothing, and the only outbound network access is CI resolving
`markdownlint-cli2` from the npm registry.

**Localization `L04`-`L06`.** English only, no string catalogs, no localized
builds, no translations to trace.

**`S06`.** No runtime configuration exists to be environment-driven.

**`R01`, `R05`.** Releases carry a document, not a package. There is no package
manifest to complete and no installable artifact to smoke-test in a clean
environment.

**Archived `A01`-`A04`.** Actively maintained.

## Notable passes

- `B06`, `S05`, `S09`, `P03` — secret scanning, push protection, private
  vulnerability reporting, and branch protection are all enabled and verified
  against the API rather than assumed.
- `R02`, `R04` — the versioning policy is documented and a check enforces that
  the document version, the changelog, and the release tag agree, so they cannot
  drift apart silently.
- `G01`-`G08` — the agent readiness criteria are satisfied by `AGENTS.md`, a
  Copilot configuration that defers to it instead of duplicating it, generated
  paths marked explicitly, and a single documented validation command.

## Reassessment

Due by 2027-02-22, six months after the assessment date. The conformance check
fails once the record ages past that point, and the badge must then be
regenerated to render as stale.
