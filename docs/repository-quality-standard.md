# Repository Quality Standard

- Version: 1.3.3
- Last reviewed: 2026-08-25
- Review cadence: every six months, even when nothing changes

This document is the public source of truth for repository quality across
projects maintained by `trsdn`. It defines outcomes and evidence, not a mandatory
technology stack.

A machine-readable catalog of every criterion in this document is published as
[`standard.yml`](../standard.yml). The two are kept in sync by a required check;
neither is allowed to drift from the other.

## Purpose

A maintainable repository lets a new contributor answer five questions without
private context:

1. What is this repository for, and who is it for?
2. How do I install, configure, run, validate, and release it?
3. What protects changes from regressions and leaked secrets?
4. How are contributions, support requests, and security reports handled?
5. What is the current release and maintenance status?

Every assessment must point to durable evidence: a repository file, GitHub
setting, release artifact, or successful workflow run.

## Versioning And Compatibility

This standard is versioned so that an assessment result stays reproducible. A
result is always recorded against the exact version it was produced with.

| Change | Version impact |
|---|---|
| A criterion is removed, renumbered, or its meaning narrows so that a recorded `Pass` could become a `Fail` | Major |
| A criterion, profile, or section is added | Minor |
| Wording, examples, formatting, or typos change without altering meaning | Patch |

Adding criteria is a minor change because a recorded result stays valid for the
version it names. A repository does not silently regress when this document
grows; it is simply due for reassessment.

### Criterion Identifiers Are Permanent

Criterion identifiers are append-only.

- An identifier is never reused, renumbered, or reassigned to different content.
- A criterion that no longer applies is marked retired in place, keeping its
  identifier and gaining a note that states when and why it was retired.
- New criteria take the next free number in their section.

This rule exists because identifiers are cited from other repositories, from
remediation issues, and from conformance records. An identifier that changes
meaning silently invalidates every citation pointing at it.

### Prefix Register

Section prefixes are assigned here and nowhere else. Adding a section requires
claiming its prefix in this table in the same change.

| Prefix | Section |
|---|---|
| A | Archived |
| B | Baseline |
| D | Deployable |
| G | Agent Readiness |
| I | Product Identity |
| L | Language And Localization |
| P | Public |
| R | Package And Release |
| S | Software |
| T | Documentation |
| X | Accessibility |
| Y | Data Protection And Privacy |

Retired prefixes are never reused. Any letter not listed above is free.

### Citing This Standard

Cite the pinned form. Never cite the default branch: it changes underneath the
citation and destroys the evidence trail.

```text
https://github.com/trsdn/.github/blob/v1.2.0/docs/repository-quality-standard.md#s05
```

Every criterion carries an anchor matching its identifier in lower case, so a
single criterion can be linked directly. Assessments, conformance records, and
remediation issues must use this form.

## Profiles

Apply the baseline to every active repository, then add every matching profile.

| Profile | Applies when |
|---|---|
| Public | The repository is publicly visible |
| Software | It builds or executes application, library, CLI, script, or service code |
| Deployable | It is deployed to a workstation, server, container, or cloud environment |
| Package | It publishes a package, binary, image, or release artifact |
| Documentation | Its primary product is documentation, research, content, or templates |
| Archived | Development has intentionally ended and GitHub marks it archived |

## Baseline

| ID | Requirement | Expected evidence |
|---|---|---|
| <a id="b01"></a>B01 | Name and description state the purpose | GitHub metadata |
| <a id="b02"></a>B02 | README explains purpose, audience, status, setup or usage, and key links | `README.md` |
| <a id="b03"></a>B03 | Licensing intent is explicit | `LICENSE` or a clear internal-use statement |
| <a id="b04"></a>B04 | Secrets, local state, and generated output are ignored while maintained source is tracked | `.gitignore` and repository contents |
| <a id="b05"></a>B05 | A reproducible validation command is documented | README or contributing guide plus a successful run |
| <a id="b06"></a>B06 | The default branch has an intentional merge policy and no unresolved critical alerts | GitHub settings and Security tab |
| <a id="b07"></a>B07 | Dependencies and supported runtime versions are declared where applicable | Manifest, lockfile, or README |
| <a id="b08"></a>B08 | User-facing or operational changes have durable history | Changelog, releases, ADRs, or linked issues |
| <a id="b09"></a>B09 | Visibility, topics, homepage, and archive state are intentional | GitHub metadata |
| <a id="b10"></a>B10 | Ownership and maintenance status are clear | `CODEOWNERS`, contributing guide, or README |
| <a id="b11"></a>B11 | The repository records which version of this standard it was assessed against, and when | Conformance record described in [Conformance Records](#conformance-records) |
| <a id="b12"></a>B12 | Assessed repositories are discoverable as a set | The `trsdn-standard` GitHub topic |

`B12` marks a repository as *governed by this standard*. It makes no claim about
the outcome; the outcome lives only in the conformance record required by `B11`.
Archived and explicitly out-of-scope repositories drop the topic.

The inventory of assessed repositories is produced with:

```sh
gh search repos --owner trsdn --topic trsdn-standard --limit 100 \
  --json fullName,isArchived
```

The difference between that list and the full account list is the outstanding
assessment backlog.

## Public Repositories

| ID | Requirement | Expected evidence |
|---|---|---|
| <a id="p01"></a>P01 | An OSI-approved license is present | Root `LICENSE` or `LICENSE.md` recognized by GitHub |
| <a id="p02"></a>P02 | Contribution and conduct expectations are documented | `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` |
| <a id="p03"></a>P03 | Security reporting is private and documented | `SECURITY.md` and private vulnerability reporting |
| <a id="p04"></a>P04 | Issue and pull-request intake is structured | Issue forms and pull-request template |
| <a id="p05"></a>P05 | README covers install, configuration, examples, compatibility, security, and support status | `README.md` |
| <a id="p06"></a>P06 | Community health files are recognized by GitHub | Community Standards page |
| <a id="p07"></a>P07 | Metadata supports discovery | Description, topics, and a maintained homepage where useful |
| <a id="p08"></a>P08 | README status badges follow the badge convention | [Status Badges](#status-badges) |
| <a id="p09"></a>P09 | Repository activity is shown from a self-hosted, generated source rather than a third-party image service | [Repository Statistics](#repository-statistics) |

## Software Repositories

| ID | Requirement | Expected evidence |
|---|---|---|
| <a id="s01"></a>S01 | Setup is reproducible from a clean checkout | Lockfile or pinned dependencies plus documented commands |
| <a id="s02"></a>S02 | Automated tests cover important behavior and failure paths | Test suite and CI run |
| <a id="s03"></a>S03 | Formatting, linting, type, and static checks run automatically where supported | Tool configuration and CI workflow |
| <a id="s04"></a>S04 | CI covers every materially supported runtime or platform | Focused CI matrix |
| <a id="s05"></a>S05 | Secret scanning runs on commits and pull requests | GitHub secret scanning, Gitleaks, or equivalent |
| <a id="s06"></a>S06 | Configuration is environment-driven and defaults do not expose private data | Example configuration and source review |
| <a id="s07"></a>S07 | Errors and logs are actionable without leaking credentials or personal data | Tests or documented logging behavior |
| <a id="s08"></a>S08 | Dependency updates and vulnerability triage have an owner and process | Dependabot or documented equivalent |
| <a id="s09"></a>S09 | Existing required checks protect the default branch | Branch ruleset or protection settings |
| <a id="s10"></a>S10 | Architecture and non-obvious constraints are documented | README, `docs/`, or ADRs |

## Deployable Repositories

| ID | Requirement | Expected evidence |
|---|---|---|
| <a id="d01"></a>D01 | Target, prerequisites, configuration, and deployment command are documented | Deployment guide or runbook |
| <a id="d02"></a>D02 | Secrets are referenced, never committed, and their safe location is documented | Secret names and secret-store reference |
| <a id="d03"></a>D03 | Health verification and rollback or recovery are documented | Runbook and smoke or health command |
| <a id="d04"></a>D04 | Runtime and infrastructure dependencies are constrained | Container, IaC, deployment, or runtime files |
| <a id="d05"></a>D05 | Operational changes update durable history and inventory where applicable | Changelog and inventory entry |
| <a id="d06"></a>D06 | Backup, migration, and destructive-operation risks are addressed when stateful | Runbook or explicit not-applicable result |

## Package And Release Repositories

| ID | Requirement | Expected evidence |
|---|---|---|
| <a id="r01"></a>R01 | Package metadata is complete and agrees with repository metadata | Package manifest |
| <a id="r02"></a>R02 | Versioning and compatibility policy are documented | README or release guide |
| <a id="r03"></a>R03 | A tag produces installable artifacts through automation | Release workflow and uploaded release assets |
| <a id="r04"></a>R04 | Tag, package version, and release title are consistent | Release workflow validation |
| <a id="r05"></a>R05 | Built artifacts are smoke-tested in a clean environment | CI or release workflow |
| <a id="r06"></a>R06 | Release notes describe meaningful changes and upgrade concerns | GitHub release or changelog |

## Product Identity

Apply these requirements to anything a user installs, runs, or downloads:
applications, installers, binaries, container images, published packages, and
hosted sites. They make a shipped artifact traceable back to its source without
guesswork.

| ID | Requirement | Expected evidence |
|---|---|---|
| <a id="i01"></a>I01 | The built artifact embeds its product name and exact version | Bundle manifest, package manifest, image label, or binary metadata |
| <a id="i02"></a>I02 | The built artifact embeds its repository URL and issue tracker URL | Manifest, label, or metadata field resolved from the release build |
| <a id="i03"></a>I03 | The built artifact embeds its license identifier and copyright holder | Manifest, label, or metadata field, plus the bundled license text where required |
| <a id="i04"></a>I04 | The running product shows its version and links to the repository and issue tracker | About window, `--version` and `--help` output, site footer, or equivalent |
| <a id="i05"></a>I05 | A product icon is embedded in the artifact and reused across installer, store, and site surfaces | Icon asset in the built artifact and on published surfaces |
| <a id="i06"></a>I06 | Embedded identity metadata is produced by the build, not maintained by hand | Release workflow or build script deriving values from the tag and repository |

Example for a macOS application bundle: `CFBundleName`,
`CFBundleShortVersionString`, `NSHumanReadableCopyright`, and `CFBundleIconFile`
are set in `Info.plist`; repository and issue URLs are added as custom keys or
shown in the About window; the release workflow injects the version from the
tag. Equivalent fields exist for other ecosystems, such as `pyproject.toml`
project URLs, npm `repository` and `bugs`, and OCI image labels
`org.opencontainers.image.source` and `org.opencontainers.image.licenses`.

## Documentation Repositories

| ID | Requirement | Expected evidence |
|---|---|---|
| <a id="t01"></a>T01 | Scope, audience, navigation, status, and freshness are visible | README or index and document metadata |
| <a id="t02"></a>T02 | Internal links and generated output are validated where practical | Link checker or documented review command |
| <a id="t03"></a>T03 | Sources and evidence are distinguishable from conclusions | Citations, references, or source notes |
| <a id="t04"></a>T04 | Generated artifacts identify their source and regeneration process | Build or export documentation |
| <a id="t05"></a>T05 | Stale or superseded material is archived or clearly marked | Status markers and archive structure |

## Agent Readiness

AI coding agents are primary contributors to these repositories. A repository
that cannot be worked in safely by an agent is not maintainable in practice,
even when a human can still navigate it.

The Baseline requires `G01` only. The Software, Deployable, and Package profiles
require the full section. Documentation repositories require `G01` and `G03`.

| ID | Requirement | Expected evidence |
|---|---|---|
| <a id="g01"></a>G01 | Agent-facing instructions exist at a discoverable, tool-neutral location | `AGENTS.md` in the repository root |
| <a id="g02"></a>G02 | Instructions state purpose, layout, and the authoritative build, run, and validation commands | `AGENTS.md` content plus a successful run of each command |
| <a id="g03"></a>G03 | Forbidden and high-risk operations are named explicitly | `AGENTS.md` section covering history rewriting, force pushes, secret handling, deployments, releases, and data-destructive commands |
| <a id="g04"></a>G04 | Tool-specific configuration does not diverge from the tool-neutral instructions | `.github/copilot-instructions.md` and equivalents reference `AGENTS.md` instead of restating it |
| <a id="g05"></a>G05 | An agent can validate its own change before proposing it | A single documented command that succeeds from a clean checkout |
| <a id="g06"></a>G06 | Generated, vendored, and machine-owned paths are marked so they are not hand-edited | `.gitignore`, `.gitattributes`, or an explicit statement in `AGENTS.md` |
| <a id="g07"></a>G07 | Agent-authored changes are attributable and reviewable | Commit trailers, pull-request labels, or a documented review expectation |
| <a id="g08"></a>G08 | Repository-scoped agent configuration is intentional where the platform supports it | `.github/github-app.yml` or a recorded not-applicable result |

`G04` is the criterion that decays first. Duplicated instructions drift apart,
and an agent then follows whichever copy it happens to read. A tool-specific file
should point at `AGENTS.md`, not paraphrase it.

A reusable starting point is published as [`templates/AGENTS.md`](../templates/AGENTS.md).

## Language And Localization

Repositories are published to an international audience. Language is therefore a
property of the repository, not a matter of personal habit.

Applies to the Software, Deployable, Package, and Documentation profiles.

| ID | Requirement | Expected evidence |
|---|---|---|
| <a id="l01"></a>L01 | The primary user-facing language is declared and is English unless a documented exception applies | README statement |
| <a id="l02"></a>L02 | User-facing strings are not hardcoded in a language other than the declared primary language | Source review or a lint rule |
| <a id="l03"></a>L03 | Localization support is declared as either English-only or an explicit list of supported locales | README or locale manifest |
| <a id="l04"></a>L04 | Localized builds keep string catalogs complete, with missing and orphaned keys detected | Catalog files plus a validation command or CI check |
| <a id="l05"></a>L05 | Dates, numbers, currency, and sorting use platform locale APIs rather than manual formatting | Source review or tests |
| <a id="l06"></a>L06 | Translated strings are traceable to their source string and to their translation origin | Catalog metadata or translation notes |
| <a id="l07"></a>L07 | Repository and contributor surfaces are English | README, `docs/`, code comments, identifiers, commit messages, issues, pull requests, and release notes |

User-facing surfaces include interface labels, menus, notifications, onboarding,
error messages, `--help` and `--version` output, human-readable log messages,
store listings, install prompts, and website copy.

`L07` applies even to repositories that ship a non-English product. The product
language and the contributor language are separate decisions.

### German-Content Exception

A repository whose subject matter is inherently German — genealogy, archival,
regional, or personal-record projects — declares German as its primary
user-facing language in its README, with one sentence of rationale. The
exception covers the product surface only. `L07` still applies.

Silence is not an exception. An undeclared language is a `Fail` on `L01`.

## Accessibility

Applies to the Deployable and Package profiles, and to any repository shipping a
user interface, including command-line tools and websites. Not applicable to
libraries with no user-facing surface; record the rationale.

These are single-maintainer projects. The target is the absence of obvious,
cheap-to-avoid barriers, not formal conformance certified by an audit. No
criterion here requires a paid tool or a specialist.

| ID | Requirement | Expected evidence |
|---|---|---|
| <a id="x01"></a>X01 | The product is fully operable by keyboard, including focus order and a visible focus indicator | Documented manual check or an automated test |
| <a id="x02"></a>X02 | Interactive elements expose an accessible name and role to assistive technology | Platform accessibility labels in source, or an inspector result |
| <a id="x03"></a>X03 | Text contrast and text sizing respect platform settings, and meaning is never conveyed by colour alone | Design tokens, source review, or a documented check |
| <a id="x04"></a>X04 | Command-line and terminal output stays usable without colour and without Unicode decoration | A documented plain-output or no-colour mode |
| <a id="x05"></a>X05 | Known accessibility limitations are stated rather than left implicit | README or a dedicated accessibility note |

`X05` is deliberate. Stating a known gap honestly is a `Pass`; leaving a reader
to discover it is not.

## Data Protection And Privacy

Existing criteria cover secrets in the repository. These cover the data the
product handles once it runs.

Applies to the Deployable and Package profiles, and to any repository that
processes user data or contacts a network service.

Most of these projects are local-first tools with no backend, so the honest
answer is usually that nothing is collected and nothing is sent. The purpose of
this section is to make that answer stated and checkable instead of assumed.

| ID | Requirement | Expected evidence |
|---|---|---|
| <a id="y01"></a>Y01 | The data the product collects, stores, or transmits is stated, including the explicit "none" case | README or privacy note |
| <a id="y02"></a>Y02 | Every outbound network destination and its purpose is documented | README, privacy note, or configuration |
| <a id="y03"></a>Y03 | Telemetry, analytics, and crash reporting are off by default or opt-in, and are disclosed | Source review plus a documented setting |
| <a id="y04"></a>Y04 | Local storage locations for user data are documented, and the user can find, export, or delete them | README or runbook |
| <a id="y05"></a>Y05 | Third-party services and AI providers that receive user content are named | README or privacy note |
| <a id="y06"></a>Y06 | Retention and deletion behaviour is stated where data outlives a session | README, runbook, or an explicit not-applicable result |

`Y01` is load-bearing. A single sentence such as "this application stores all
data locally and contacts no network service" is a `Pass`.

These criteria describe disclosure, not legal process. They do not require a
record of processing, a data protection agreement, or legal review. They also do
not restate the secret-handling requirements in `S05`, `S06`, `S07`, and `D02`.

## Status Badges

Badges are the first thing a reader sees. They are held to the same rule as
built artifacts in `I06`: their values are produced from an authoritative source,
not maintained by hand.

Applies wherever `P08` applies.

Required badge block, in this order:

1. license;
2. platform or runtime requirement;
3. CI status of the default branch;
4. latest release, where the repository publishes releases;
5. conformance, where a conformance record exists.

Rules:

- Every badge links to what it reports: the license file, the manifest or
  documented requirement, the workflow, the release, the conformance record.
- Every badge value is derived from an authoritative source, or is covered by a
  check that fails when it drifts. A hardcoded value duplicating a manifest is a
  `Partial` at best.
- Badges outside the required and optional sets need a stated reason. A wall of
  badges carries less information than four accurate ones.
- Badge images are served from the repository or a first-party source where
  practical, because a third-party image host observes every reader. See `Y02`.

A hardcoded `Swift 5.9` badge beside a manifest that has moved to 6.0 is the
failure this section exists to prevent.

## Repository Statistics

Badges report state. A statistics card reports activity: commit volume, when the
repository was last touched, the current release, contributor count, language
mix. A reader uses it to judge whether a project is alive before reading any
code.

`P09` applies the same rule the badge section applies to values: the card is
generated from an authoritative source and committed to the repository. It is
not fetched from a third-party rendering service at read time.

The reason is `Y02`. A README image served from an external host observes every
visitor, including their address and referrer, and does so on a page the
maintainer controls. A self-hosted card removes that observation, and it also
removes an availability dependency: a card committed as an SVG cannot break
because someone else's free tier expired.

Rules:

- The card is generated, never hand-edited. A committed SVG that no workflow
  reproduces is a `Fail`.
- Generation runs on a schedule, so the card cannot silently age past the
  repository it describes.
- Light and dark variants are published as separate files and selected with a
  `<picture>` element. A `prefers-color-scheme` query inside the SVG has no
  effect through GitHub's image proxy.
- The card embeds no external references: no remote fonts, no `<image href>` to
  another host. It is self-contained or it reintroduces the problem it solves.

The shared implementation is the reusable workflow described in
[Repository Stats](repo-stats.md). A repository may generate the card another
way; the criterion is about the property, not the tool.

## Conformance Records

`B11` requires a conformance record: the machine-readable result of assessing a
repository against a named version of this standard.

The record is the source of truth. The conformance badge renders it and can
never disagree with it, because no badge value is editable on its own.

| Field | Meaning |
|---|---|
| `standard_version` | The version assessed against, matching a published tag |
| `assessed_on` | The date the assessment was completed |
| `state` | One of the states defined in [Assessment](#assessment) |
| `criteria` | Every criterion in the catalog, each with a result |
| `evidence` | Link to the assessment output holding the per-criterion notes |

Every criterion in the catalog appears in the record. A criterion that does not
apply is recorded as `na` with its rationale in the linked assessment, so the
difference between "does not apply" and "was never looked at" stays visible.

Rules:

- The badge shows the states defined in this document. `Pass` stays a
  per-criterion result and is never used as a repository-level state, because one
  word with two meanings makes both useless.
- A record carries an assessment date, and a record older than the review cadence
  renders as stale rather than as its last known result. An assessment from two
  years ago is not evidence.
- Where no record exists, no badge is shown. A permanent "unknown" badge is
  worse than an absent one.
- No numeric score or percentage is derived from a record. State is assigned by
  impact, and a score would quietly replace that judgement.

The format and a worked example are documented in
[Conformance Record Format](conformance-record.md).

## Archived Repositories

Archived repositories do not need to satisfy the active baseline.

| ID | Requirement | Expected evidence |
|---|---|---|
| <a id="a01"></a>A01 | GitHub archive state is enabled | GitHub settings |
| <a id="a02"></a>A02 | README states why and when maintenance ended | `README.md` |
| <a id="a03"></a>A03 | A successor or migration destination is linked when one exists | `README.md` |
| <a id="a04"></a>A04 | No active deployment or undocumented dependency remains | Deployment records or inventories |

## Assessment

Use one result for every applicable criterion.

| Result | Meaning |
|---|---|
| Pass | Requirement is met and evidence is linked |
| Partial | Evidence exists, but a material part is missing |
| Fail | Requirement applies and is not met |
| N/A | Requirement does not apply and the rationale is recorded |
| Unknown | Evidence has not been inspected |

Assign the overall state by impact, not by percentage.

| State | Rule |
|---|---|
| Healthy | No critical or high-priority gaps; remaining gaps are minor |
| Needs work | One or more high-priority gaps exist, but normal use remains supportable |
| At risk | A critical gap exists in security, recoverability, deployment, or basic reproducibility |
| Archive candidate | No clear owner or active purpose exists and no dependency requires it |
| Archived | Archive requirements are met |

Critical gaps include committed secrets, an exposed write-capable service,
missing recovery for irreplaceable state, or an active deployment with no known
source or configuration. High-priority gaps include no README, ambiguous public
licensing, no software validation, unsupported dependencies, or unreproducible
releases.

## Remediation Issue Contract

Every remediation issue must be executable without private context. For every
scope item, include:

- the criterion ID and observed gap;
- required content or configuration, not only a file or setting name;
- expected evidence, such as a recognized community file, green workflow,
  release asset, or repository-setting result;
- concrete acceptance criteria under `Done when`; and
- explicit exclusions for working behavior that must be preserved.

For example, `add SECURITY.md` is insufficient. Require supported versions, a
private reporting path, response expectations, and guidance against public
disclosure. Likewise, `protect main` must name existing checks, require the
branch to be current before merge, and block force pushes and deletion. Never
require a check that does not exist.

## Recommended Shape

Use only files that serve the repository's profiles. Empty governance files are
not evidence of quality.

```text
AGENTS.md
README.md
LICENSE
SECURITY.md
CONTRIBUTING.md
CODE_OF_CONDUCT.md
CHANGELOG.md
.gitignore
.github/
  CODEOWNERS
  conformance.yml
  copilot-instructions.md
  dependabot.yml
  github-app.yml
  ISSUE_TEMPLATE/
  pull_request_template.md
  workflows/
    ci.yml
    release.yml
docs/
  decisions/
tests/
```

Equivalent evidence is valid when it is durable, discoverable, and testable.
