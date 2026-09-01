# Self-Assessment: trsdn/.github

- Standard version: 1.8.0
- Assessed on: 2026-09-01
- State: **Healthy**
- Record: [`.github/conformance.yml`](../.github/conformance.yml)

This repository publishes the standard, so it assesses itself against it. Every
criterion that applies passes. That is a recent result, not a founding one: an
earlier assessment recorded one failure and four partials, and each was closed by
changing the repository rather than by softening the criterion.

The record is what the badge renders. If a future assessment finds a gap, the
badge goes back to `Needs work`, because a green badge over a known gap would
make every other badge in the estate worthless.

## Profiles

| Profile | Applies | Rationale |
|---|---|---|
| Public | Yes | Public visibility |
| Software | Yes | `scripts/` executes script code, and the standard's Software profile covers scripts |
| Deployable | No | Nothing is deployed anywhere |
| Package | Yes | The standard is published as tagged releases |
| Documentation | Yes | The primary product is documentation |
| Published Site | No | This repository defines the standard; it does not ship a product. See below |
| Archived | No | Actively maintained |

## Runner availability

This repository **has a runner**: it is public and Actions is enabled, so hosted
minutes cover it. [Automation Without A Runner](repository-quality-standard.md#automation-without-a-runner)
therefore does not apply to any criterion here, and `S02`, `S03`, `S04`, `R03`,
`R05`, `R07`, and the badge block are assessed exactly as written. The finding is
recorded because the section requires it to be, and because a reader comparing
this record against one from a private repository needs to see which of the two
readings produced it.

## Closed gaps

Each of these was a gap in the previous assessment. They are kept here rather
than deleted, because the record of what was wrong is the reason to trust that
what is now green was actually fixed.

### P09 — Repository activity is shown from a self-hosted source

Was `fail`. The generator, the reusable workflow, and the documentation all
existed, but this repository did not show its own card. The criterion asks for
the card to be shown, not for the tooling to exist.

The card is now rendered for this repository alongside the account cards and
published to the `stats` branch, which the README embeds with a `<picture>`
element. It is published to a branch rather than committed to `main` because
`main` requires status checks, and a workflow cannot push through that.

### S03 — Static checks run automatically

Was `partial`. Markdown was linted; the Python that generates and validates
everything this repository publishes was not.

Ruff now runs `check` and `format --check` in CI, pinned. The first run found an
ambiguous variable name and two f-strings without placeholders. The rule set
stays close to Ruff's defaults deliberately: a configuration nobody can satisfy
gets suppressed rather than fixed, and a suppressed check reads as coverage
without being any.

### S09 — Required checks protect the default branch

Was `partial`, and had been stale rather than wrong. The three checks named in
the previous assessment were added to the required set shortly after it was
written, and the record had not caught up. Verified against the API: `Markdown
lint`, `Standard consistency`, `Conformance record`, and `Script tests` are all
required, with strict mode on.

This is the one gap that closed without any change to the repository, which is
exactly why the review cadence exists.

### P04 — Issue and pull-request intake is structured

Was `partial`. Issue forms and a pull-request template existed, but no
`ISSUE_TEMPLATE/config.yml` did, so a single click on "Open a blank issue"
bypassed all of them.

Blank issues are now disabled and contact links route vulnerabilities to the
security policy and questions to the support guide.

### T02 — Internal links and generated output are validated

Was `partial`. Markdown lint ran, but nothing checked that links resolved.

`scripts/links.py` now validates relative targets and anchors across every
Markdown file. Anchors are the point: criteria are addressed as `#s05` and cited
from other repositories, so a renamed heading silently invalidates citations that
live outside this checkout. Verified by mutation — a missing file, a missing
anchor in another file, a missing anchor in the same file, and a renamed heading
are each caught.

External links are deliberately out of scope. Checking them needs the network and
fails for reasons unrelated to this repository, which is how a check earns the
right to be ignored.

## Not applicable

**Published Site `W01`-`W08`.** This repository defines the standard; it does not
ship a product. Everyone who reads the standard reads it while working inside a
repository — applying it, citing a criterion in an issue, or acting on it as an
agent — and a page in front of it would add a surface to maintain while answering
nothing they were asking. The criteria are consumed as Markdown at a pinned URL
and as `standard.yml`, both of which are already the right shape for that
audience.

This was recorded as eight failures against 1.4.0 for one day. The trigger was
written too broadly — "readers who will never open the repository" caught any
document, including a specification — and 1.5.0 narrowed it. The repositories the
standard is *applied to* are the ones that ship products, and many of them do
need a site.

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
`markdownlint-cli2` from the npm registry and Ruff from PyPI. The activity card
the README now shows is served from this repository's own `stats` branch and is
self-contained, so nothing about it depends on a third party staying available —
which is what `P09` asks for, and it observes no reader on any surface,
proxied or not.

**Localization `L04`-`L06`.** English only, no string catalogs, no localized
builds, no translations to trace.

**`S06`.** No runtime configuration exists to be environment-driven.

**`R01`, `R05`.** Releases carry a document, not a package. There is no package
manifest to complete and no installable artifact to smoke-test in a clean
environment.

**Archived `A01`-`A04`.** Actively maintained.

## Notable passes

- `B13` — passes, but only after a fix. The six validation commands were listed
  verbatim in both `README.md` and `AGENTS.md`, and adding two checks earlier
  today required editing both. That is exactly the failure `B13` describes: the
  next person to add a check updates one copy, and the other silently becomes
  wrong while still reading as authoritative. `README.md` now holds the list,
  which `B05` requires anyway, and `AGENTS.md` links to it and keeps only what is
  unique to it — what each check rejects and why it exists.
- `B06`, `S05`, `S09`, `P03` — secret scanning, push protection, private
  vulnerability reporting, and branch protection are all enabled and verified
  against the API rather than assumed.
- `R02`, `R04` — the versioning policy is documented and a check enforces that
  the document version, the changelog, and the release tag agree, so they cannot
  drift apart silently.
- `R07` — passes, and the criterion was written from a failure found elsewhere in
  the estate rather than from this repository. `.github/workflows/release.yml`
  extracts the changelog section for the tag, exits non-zero when the result is
  empty, and publishes that same text as the notes body, so no release can carry
  notes that were written separately from the entry. The unreleased guard was
  added in the same change: this repository keeps no unreleased section and could
  not strand an entry today, but a gate that holds only while a convention holds
  is not a gate.
- `G01`-`G08` — the agent readiness criteria are satisfied by `AGENTS.md`, a
  Copilot configuration that defers to it instead of duplicating it, generated
  paths marked explicitly, and a single documented validation command.
- `S02` — `tests/` covers both validation scripts through their command line,
  asserting the exit code *and* the specific diagnostic for every rejection path.
  Each check was verified to be load-bearing by disabling it in the script and
  confirming the suite goes red; a test that passes whether or not the code works
  is not coverage. Writing these tests found a real defect: ageing only failed
  `--check` when the badge also disagreed with the record, so regenerating the
  badge silenced the reminder without anyone reassessing. That is fixed and
  pinned by a test.

## Reassessment

Due by 2027-03-01, six months after the assessment date. The conformance check
fails once the record ages past that point and stays red until the repository is
reassessed. Regenerating the badge makes it render as stale, which keeps the
public signal honest, but does not clear the check.
