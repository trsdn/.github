# Repository Quality Standard

- Version: 1.2
- Last reviewed: 2026-08-21

This document is the public source of truth for repository quality across
projects maintained by `trsdn`. It defines outcomes and evidence, not a mandatory
technology stack.

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
| B01 | Name and description state the purpose | GitHub metadata |
| B02 | README explains purpose, audience, status, setup or usage, and key links | `README.md` |
| B03 | Licensing intent is explicit | `LICENSE` or a clear internal-use statement |
| B04 | Secrets, local state, and generated output are ignored while maintained source is tracked | `.gitignore` and repository contents |
| B05 | A reproducible validation command is documented | README or contributing guide plus a successful run |
| B06 | The default branch has an intentional merge policy and no unresolved critical alerts | GitHub settings and Security tab |
| B07 | Dependencies and supported runtime versions are declared where applicable | Manifest, lockfile, or README |
| B08 | User-facing or operational changes have durable history | Changelog, releases, ADRs, or linked issues |
| B09 | Visibility, topics, homepage, and archive state are intentional | GitHub metadata |
| B10 | Ownership and maintenance status are clear | `CODEOWNERS`, contributing guide, or README |

## Public Repositories

| ID | Requirement | Expected evidence |
|---|---|---|
| P01 | An OSI-approved license is present | Root `LICENSE` or `LICENSE.md` recognized by GitHub |
| P02 | Contribution and conduct expectations are documented | `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` |
| P03 | Security reporting is private and documented | `SECURITY.md` and private vulnerability reporting |
| P04 | Issue and pull-request intake is structured | Issue forms and pull-request template |
| P05 | README covers install, configuration, examples, compatibility, security, and support status | `README.md` |
| P06 | Community health files are recognized by GitHub | Community Standards page |
| P07 | Metadata supports discovery | Description, topics, and a maintained homepage where useful |

## Software Repositories

| ID | Requirement | Expected evidence |
|---|---|---|
| S01 | Setup is reproducible from a clean checkout | Lockfile or pinned dependencies plus documented commands |
| S02 | Automated tests cover important behavior and failure paths | Test suite and CI run |
| S03 | Formatting, linting, type, and static checks run automatically where supported | Tool configuration and CI workflow |
| S04 | CI covers every materially supported runtime or platform | Focused CI matrix |
| S05 | Secret scanning runs on commits and pull requests | GitHub secret scanning, Gitleaks, or equivalent |
| S06 | Configuration is environment-driven and defaults do not expose private data | Example configuration and source review |
| S07 | Errors and logs are actionable without leaking credentials or personal data | Tests or documented logging behavior |
| S08 | Dependency updates and vulnerability triage have an owner and process | Dependabot or documented equivalent |
| S09 | Existing required checks protect the default branch | Branch ruleset or protection settings |
| S10 | Architecture and non-obvious constraints are documented | README, `docs/`, or ADRs |

## Deployable Repositories

| ID | Requirement | Expected evidence |
|---|---|---|
| D01 | Target, prerequisites, configuration, and deployment command are documented | Deployment guide or runbook |
| D02 | Secrets are referenced, never committed, and their safe location is documented | Secret names and secret-store reference |
| D03 | Health verification and rollback or recovery are documented | Runbook and smoke or health command |
| D04 | Runtime and infrastructure dependencies are constrained | Container, IaC, deployment, or runtime files |
| D05 | Operational changes update durable history and inventory where applicable | Changelog and inventory entry |
| D06 | Backup, migration, and destructive-operation risks are addressed when stateful | Runbook or explicit not-applicable result |

## Package And Release Repositories

| ID | Requirement | Expected evidence |
|---|---|---|
| R01 | Package metadata is complete and agrees with repository metadata | Package manifest |
| R02 | Versioning and compatibility policy are documented | README or release guide |
| R03 | A tag produces installable artifacts through automation | Release workflow and uploaded release assets |
| R04 | Tag, package version, and release title are consistent | Release workflow validation |
| R05 | Built artifacts are smoke-tested in a clean environment | CI or release workflow |
| R06 | Release notes describe meaningful changes and upgrade concerns | GitHub release or changelog |

## Product Identity

Apply these requirements to anything a user installs, runs, or downloads:
applications, installers, binaries, container images, published packages, and
hosted sites. They make a shipped artifact traceable back to its source without
guesswork.

| ID | Requirement | Expected evidence |
|---|---|---|
| I01 | The built artifact embeds its product name and exact version | Bundle manifest, package manifest, image label, or binary metadata |
| I02 | The built artifact embeds its repository URL and issue tracker URL | Manifest, label, or metadata field resolved from the release build |
| I03 | The built artifact embeds its license identifier and copyright holder | Manifest, label, or metadata field, plus the bundled license text where required |
| I04 | The running product shows its version and links to the repository and issue tracker | About window, `--version` and `--help` output, site footer, or equivalent |
| I05 | A product icon is embedded in the artifact and reused across installer, store, and site surfaces | Icon asset in the built artifact and on published surfaces |
| I06 | Embedded identity metadata is produced by the build, not maintained by hand | Release workflow or build script deriving values from the tag and repository |
| I07 | Every application and website has a reachable About surface | About window, About page, or `--version` output, linked from primary navigation, menu, or footer |
| I08 | The About surface states the product name, version, copyright holder and year, and license | About surface content plus the bundled or linked license text |
| I09 | The About surface links to the source repository and to a way to report an issue | Repository URL and issue tracker or security-reporting link on the About surface |

Example for a macOS application bundle: `CFBundleName`,
`CFBundleShortVersionString`, `NSHumanReadableCopyright`, and `CFBundleIconFile`
are set in `Info.plist`; repository and issue URLs are added as custom keys or
shown in the About window; the release workflow injects the version from the
tag. Equivalent fields exist for other ecosystems, such as `pyproject.toml`
project URLs, npm `repository` and `bugs`, and OCI image labels
`org.opencontainers.image.source` and `org.opencontainers.image.licenses`.

### About Surface

Every application and website must expose an About surface. It is the one place
a user can reach without private context to learn what they are running, who
owns it, and where to report a problem.

An About surface is reachable in at most two steps from the product's primary
surface: an application menu or settings entry, a site footer or navigation
link, or a documented `--version` and `--help` flag for a command-line tool.

It must state:

- the product name and the exact released version, matching the artifact
  metadata required by `I01`;
- the copyright holder and year, and the license name, with the full license
  text bundled or linked;
- a link to the source repository; and
- a link to report an issue, such as the repository issue tracker, plus the
  private security-reporting path when one exists.

It may also state build metadata such as the commit or build date, third-party
notices and attributions, and links to support or privacy documentation.

Values shown on the About surface must come from the same build-generated
metadata as `I06`, so a released product can never display a version, license,
or repository link that disagrees with its artifact.

Example for a website or web application: a footer, present on every page, shows
`Product 1.4.2`, `(c) 2026 Torsten Mahr - MIT License`, a `Source` link to the
repository, and a `Report an issue` link to the issue tracker, with the version
injected at build time from the release tag.

## Documentation Repositories

| ID | Requirement | Expected evidence |
|---|---|---|
| T01 | Scope, audience, navigation, status, and freshness are visible | README or index and document metadata |
| T02 | Internal links and generated output are validated where practical | Link checker or documented review command |
| T03 | Sources and evidence are distinguishable from conclusions | Citations, references, or source notes |
| T04 | Generated artifacts identify their source and regeneration process | Build or export documentation |
| T05 | Stale or superseded material is archived or clearly marked | Status markers and archive structure |

## Archived Repositories

Archived repositories do not need to satisfy the active baseline.

| ID | Requirement | Expected evidence |
|---|---|---|
| A01 | GitHub archive state is enabled | GitHub settings |
| A02 | README states why and when maintenance ended | `README.md` |
| A03 | A successor or migration destination is linked when one exists | `README.md` |
| A04 | No active deployment or undocumented dependency remains | Deployment records or inventories |

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
README.md
LICENSE
SECURITY.md
CONTRIBUTING.md
CODE_OF_CONDUCT.md
CHANGELOG.md
.gitignore
.github/
  CODEOWNERS
  dependabot.yml
  ISSUE_TEMPLATE/
  pull_request_template.md
  workflows/
    ci.yml
    release.yml
docs/
tests/
```

Equivalent evidence is valid when it is durable, discoverable, and testable.
