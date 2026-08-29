# Self-Assessment: trsdn/.github

- Standard version: 1.4.0
- Assessed on: 2026-08-29
- State: **Needs work**
- Record: [`.github/conformance.yml`](../.github/conformance.yml)

This repository publishes the standard, so it assesses itself against it.

Earlier today this repository reached `Healthy` against 1.3.3, with every
applicable criterion passing. Version 1.4.0 then added the Published Site profile
and `B13`, and the profile applies here: the standard is a public document whose
readers are, by design, people who maintain *other* repositories.

There is no site, so all eight `W` criteria fail and the state returns to
`Needs work`.

That is the correct behaviour, not a regression. Raising the bar creates gaps in
repositories that were compliant with the previous bar — including this one, and
it would be dishonest for the repository that writes the standard to exempt
itself from the version it just published. `B11` exists precisely so that a
result names the version it was produced against: the `Healthy` result was real,
and it was real *against 1.3.3*.

## Profiles

| Profile | Applies | Rationale |
|---|---|---|
| Public | Yes | Public visibility |
| Software | Yes | `scripts/` executes script code, and the standard's Software profile covers scripts |
| Deployable | No | Nothing is deployed anywhere |
| Package | Yes | The standard is published as tagged releases |
| Documentation | Yes | The primary product is documentation |
| Published Site | Yes | The standard is written for readers who maintain other repositories and who have no reason to contribute to this one |
| Archived | No | Actively maintained |

## Gaps

### W01-W08 — No published site — `fail`

The standard is currently readable only as Markdown in a repository, or as
`standard.yml`. Someone deciding whether to adopt it has to open a repository and
read a long document in GitHub's file viewer.

All eight criteria fail together because they describe one artefact that does not
exist. Tracked as a single remediation issue rather than eight, per the
[Remediation Issue Contract](repository-quality-standard.md#remediation-issue-contract).

Two decisions belong to the maintainer before this can be closed, and neither is
an implementation detail:

1. **Where the site lives.** Publishing Pages from `.github` yields a URL
   containing a leading dot, and this repository is already special-cased by
   GitHub as the source of default community health files. Rendering the
   standard from a separate repository may be the better answer.
2. **Whether the design language becomes public.** `W05` requires Instrument
   Workshop, which is consumed by vendoring two stylesheets. The design system
   repository is private and no public repository ships those files yet, so the
   first site to satisfy `W05` also publishes the design language. That is a
   disclosure decision, not a technical one.

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
self-contained, so it observes no reader — which is the whole reason `P09`
requires a self-hosted card rather than a third-party image service.

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

Due by 2027-02-28, six months after the assessment date. The conformance check
fails once the record ages past that point and stays red until the repository is
reassessed. Regenerating the badge makes it render as stale, which keeps the
public signal honest, but does not clear the check.
