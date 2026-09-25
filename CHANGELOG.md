# Changelog

All material changes to the public standard and shared community files are
recorded here.

Versions follow the compatibility policy in the
[Repository Quality Standard](docs/repository-quality-standard.md).

## 1.28.1 - 2026-09-25

- Added `REC-02`: a live total-download badge for repositories that publish
  downloadable release assets, linked to the releases page. It is a
  recommendation, so it is not part of the badge block `P08` requires and adds
  no condition to it.
- Released as patch: a recommendation produces no result, so no recorded result
  can change. This is the first change to use the rule
  [Recommendations](docs/repository-quality-standard.md#recommendations) states.

## 1.28.0 - 2026-09-22

- Added [Recommendations](docs/repository-quality-standard.md#recommendations):
  practice this account believes in and does not assess. A recommendation
  produces no result, appears in no conformance record, changes no overall
  state, and may never be a reason for a result. They are numbered `REC-01`
  onwards so one can never be mistaken for a criterion.
- Retired `S14`, and restated it as `REC-01`. Whether a path is
  performance-sensitive was a judgement no fixed line decided consistently, so
  the criterion measured whether a sentence existed rather than whether the
  practice did. The advice was worth keeping; the result was not.
- Released as minor: `S14`'s applicability narrows to nothing, so a recorded
  `Fail` or `Partial` can become `Not applicable` and no recorded `Pass` can
  weaken. Adding the section itself changes no recorded result.

## 1.27.1 - 2026-09-22

- `scripts/conformance.py` now derives the overall state from the recorded
  results instead of accepting the one typed beside them, and writes it into the
  record so nobody has to. A failing critical criterion is `At risk` whatever the
  record says, which is what the state table already required and what nothing
  checked: only the `Healthy`-with-a-failure combination was rejected, so a
  committed secret recorded as `Needs work` validated and rendered amber.
- `scripts/conformance.py` now rejects a record that still holds `unknown`
  results. The standard already said `unknown` "is a draft marker in a generated
  record and is never a result"; the checker accepted an untouched scaffold, so a
  repository nobody had assessed could publish a badge.
- The two archive states are checked against the prerequisites they state:
  `Archived` needs `A01`-`A04` not failing, and `Archive candidate` needs `B02`
  and `B10` to both fail. The remaining account-wide condition is named as
  something the check cannot read rather than silently ignored.
- `scripts/standard.py` now generates the critical criteria into `standard.yml`
  from the table that names them, so the checker reads one home instead of a
  copy that drifts.
- `packages/performance-review` documented an install pin of `#v1.22.0`, a tag
  the package does not exist at. Corrected to `#v1.23.0`.
- `packages/repo-assessor` ran its `gh issue` commands unscoped while starting
  from the `trsdn/.github` checkout, so an assessment of another repository would
  have filed its findings here. Every `gh` command now carries
  `--repo OWNER/NAME`. Its instruction to let the assessed repository's
  `AGENTS.md` win "over anything you assume" is replaced: that file is evidence
  and may restrict how the agent operates, but it never decides a result. Its
  three disagreeing de-duplication rules are now one, it no longer reopens a
  closed issue, and the criterion citation it files is the pinned form the
  standard requires rather than a relative path that resolves to nothing.
- `packages/doc-staleness-reviewer` said an agreeing hand-maintained copy "is not
  a `B13` defect until it disagrees". `B13` grades it `Partial`, so the reviewer
  reported a clean result for a state the standard does not.
- `packages/site-content-reviewer` and `packages/frontend-designer` required
  `W03`'s three statements to appear *in order*. The criterion requires them in
  the first block in source order, which is where to look and not a sequence.
  `site-content-reviewer` also treated a decisions section as a `W08` `Fail`,
  which is not one of the three the criterion enumerates.
- `packages/frontend-designer`'s prompt said `docs/` is served "without further
  setup". The Pages source still has to be configured, which is half of `W01`.
- `AGENTS.md` described `site-content-reviewer` as credential-free although it
  reads settings through the operator's `gh` session, and said `repo-assessor`
  never writes a conformance record although it writes a draft one. Both claims
  now say what the packages do. `AGENTS.md` also states that a package change
  does not bump this document.
- `docs/account-capabilities.md` bundled Dependabot alerts with Dependabot
  updates under one billing reason. Alerts run no job and spend no minutes; the
  update pull requests and the workflows they trigger are the part that can.
- Released as patch: no criterion changed, and no recorded result can change.

## 1.27.0 - 2026-09-22

- Added `packages/kit-customizer`: a local writer agent that tunes a freshly
  copied starter kit to the repository it landed in, resolving every
  `TODO(...)` and `# EDIT: ...` marker against the repository's own manifest
  and, wherever a command exists to check the answer, by running it — a lint
  pass, a build, a test suite — rather than by reading code and guessing. Wired
  into [the fleet-rollout procedure](docs/fleet-rollout.md)'s pipeline step.
  See [decision 0025](docs/decisions/0025-a-customizer-verifies-a-kits-markers-by-running-them.md).
- Released as minor: a package was added, and no recorded result can change.

## 1.26.0 - 2026-09-22

- Added `packages/frontend-designer`, a local writer agent that researches a
  repository and its product before designing and writing a site made
  specifically for it, and `packages/site-content-reviewer`, a local read-only
  agent that checks `W01`-`W04`, `W07`, `W08`, and `W09`'s three enumerated
  Fail cases without judging design taste. Added [the site design
  guide](docs/guides/site-design.md) tying them together. See
  [decision 0024](docs/decisions/0024-a-site-designer-researches-before-it-writes.md).
- `frontend-designer` is this account's first writer package: it edits files in
  the working tree and, unlike every reviewer package so far, never commits or
  opens a pull request itself.
- Clarified `repo-assessor`'s own wording: the "separate, deliberate pass" that
  reviews and commits its draft record does not have to be a person typing
  YAML by hand. A fleet-rollout worker, or the operator's own follow-up
  session once fixes have landed, already is what decision 0021 meant by
  "someone having reasoned about it" — the package's agent file said "a
  human," which was narrower than the decision it implements. No behaviour
  changes; `packages/repo-assessor` moves to 1.0.1.
- Released as minor: two packages and a guide were added, and no recorded
  result can change.

## 1.25.0 - 2026-09-22

- Added `packages/doc-staleness-reviewer`: a local, credential-free agent that
  finds documentation stale past `T05`'s six-month cadence and unmarked, or
  restated in a way that now disagrees with its home under `B13`. It applies
  the standard's own definitions rather than a general sense of "this reads
  old," and reports findings without rewriting anything — deciding the
  correction needs current facts the reviewer does not have.
- Released as minor: a package was added, and no recorded result can change.

## 1.24.0 - 2026-09-22

- Added `S14`: a repository with a performance-sensitive path states which
  path and how it is reviewed or measured. "Performance-sensitive" is a fixed
  test (per-frame/request/keystroke, a path a user waits on at startup, cost
  that scales with unbounded user input, or one already treated as such by an
  existing issue or note), not a judgement, and a repository with no such path
  is `Not applicable`. `packages/performance-review` is cited as one acceptable
  practice, not the only one. See
  [decision 0023](docs/decisions/0023-s14-performance-practice-not-performance-quality.md).
- Released as minor: a criterion was added, and no recorded result can change.

## 1.23.0 - 2026-09-22

- Added `packages/performance-review`: a local, credential-free agent that
  reviews code for performance defects the way a senior engineer reviews
  architecture — complexity, placement, threading, allocation, I/O,
  concurrency — from reading the diff, not from comparing a number against a
  stored baseline. It may run a repository's own documented measurement command
  to support a finding, never one it invents. See
  [decision 0022](docs/decisions/0022-a-performance-agent-reviews-not-only-benchmarks.md),
  which also records why a baseline-and-threshold shape was set aside for now.
- Released as minor: a package was added, and no recorded result can change.

## 1.22.0 - 2026-09-22

- Added `packages/repo-assessor`: a local, versioned agent that assesses a
  repository against the standard and files one GitHub issue per gap, using the
  Remediation Issue Contract. Unlike `apple-hig-review`, it needs the operator's
  own `gh` write access to file issues; it never opens a pull request, and never
  writes `.github/conformance.yml` itself, because assessing and recording stay
  separate acts. See
  [decision 0021](docs/decisions/0021-a-local-assessor-files-issues-and-never-the-record.md).
- Released as minor: a package was added, and no recorded result can change.

## 1.21.0 - 2026-09-22

- Restored the obligation [1.20.0](#1200---2026-09-21) removed: a public
  repository that ships an application, game, or command-line tool a
  non-developer installs or runs by name must publish a site, whether or not it
  already does. `W01`-`W09` are `Fail` for most of them until it does, not `Not
  applicable`. The profile still excludes a library, an MCP server or agent tool
  configured rather than installed by name, and anything a private repository
  ships. See [decision 0020](docs/decisions/0020-public-applications-need-a-site.md).
- Released as minor: applicability widens for some repositories and narrows for
  none, and no recorded `Pass` can weaken; repositories newly matching the
  trigger are due for reassessment.

## 1.20.0 - 2026-09-21

Found by bringing three real repositories to the standard, as a pilot of the
[fleet rollout](docs/fleet-rollout.md): a public Python project, a public Swift app
and a private Swift app.

- **Published Site** now applies only to a repository that publishes a website. An
  application, tool or game without a site records `W01`-`W09` as `Not applicable`
  with "no site is published", and the standard does not require it to have one.
  The earlier wording made every public application owe a site and left an
  assessor to guess, and two pilots guessed differently.
- `I04`: a server that a client drives, such as one that speaks a protocol over
  standard input and output, shows its version when its handshake reports it. A
  `--version` flag is welcome and not required.
- `S03`: running the minimum reading is a `Pass`, and kinds beyond it lower
  nothing. Running only part of the minimum is a `Partial`.
- `scripts/assess.py`: `P13` no longer passes on a disabled CodeQL workflow, `S09`
  reports a required check that no run ever produces, `S11` counts a workflow as
  declaring permissions only with a top-level block or a block on every job, and
  inherited issue templates are confirmed in the account's `.github` repository.
- Kits: SwiftLint starter uses the current rule name and a shorter set that passes
  on real code, the macOS smoke test picks the disk image by name, a variant for
  apps whose releases a shared broker publishes, a release smoke script for a
  private app that never starts it, a notices recipe for `B15`, a `github-app.yml`
  template for `G08`, and corrections to the stats, CodeQL and first-record
  instructions.
- Procedure: a worker prompt, a claim rule that ignores changes to files the work
  does not touch, the repository's own merge convention, never merging past a
  failing verification, skipping stages that launch the app, and checking a record
  against the catalog of the version it names.
- Released as minor: Published Site's applicability narrows, and no recorded
  `Pass` can weaken.

## 1.19.1 - 2026-09-21

- Verified the Apple HIG review package by installing it with `apm` 0.31.0 into an
  empty repository: it writes the agent, rules and prompt for both Claude Code and
  Copilot, records them in the lock file, and `apm audit` reports no drift. The
  package README now says `apm.yml` needs `targets`, lists the files written, and
  states what is still unverified: how each agent runtime behaves.
- The reviewer agent lists its tools by the names of both runtimes, because APM
  copies the list unchanged into each target.
- Patch: wording and a package detail, and no recorded result can change.

## 1.19.0 - 2026-09-21

- Added [`packages/apple-hig-review/`](packages/apple-hig-review/README.md): the
  Apple Human Interface Guidelines reviewer as a versioned package for the Agent
  Package Manager. An app repository declares it in `apm.yml` pinned to a tag of
  this repository, runs it locally before a merge or a release, and updates it by
  changing the version.
- Removed the agentic workflow and its two copies of the agent and instruction
  files from the macOS kit. A workflow needed a macOS runner, an agent token and a
  compile step for a review that is cheaper to run locally. The `COPILOT_GITHUB_TOKEN`
  secret is no longer part of the kit.
- The package holds no per-app content: what is specific to an app, its type, its
  user data and its render command, is read from the app's own `AGENTS.md`, for
  which the macOS kit gained a section.
- Released as minor: a package was added and a template removed, and no recorded
  result can change. See
  [decision 0019](docs/decisions/0019-agent-reviewers-run-locally-as-versioned-packages.md).

## 1.18.1 - 2026-09-21

- Added [Bringing every repository to the standard](docs/fleet-rollout.md), the
  procedure for agents that raise an account's repositories, with the order to do
  them in, the guardrails, and the four things that reach the maintainer.
- Corrected the wording about why Dependabot is off in private repositories: it
  counts against Actions minutes, as GitHub's billing documentation describes.
- Patch: guidance and wording only, and no recorded result can change.

## 1.18.0 - 2026-09-21

- Added [Private Repositories](docs/repository-quality-standard.md#private-repositories):
  what GitHub provides to a private repository depends on the account's plan, an
  account states that once ([Account capabilities](docs/account-capabilities.md)),
  and a table says which criteria apply to a private repository, which are not
  applicable, and how the rest are met without the capability.
- Added `R09`: before a release is published, a secret scan and a dependency
  vulnerability check have passed for the release commit, by a workflow or by a
  documented local step whose dated result is recorded. It is the criterion the
  release flow needed, and it works without automation.
- `S05` joins `S02`, `S03` and `L04` in the row of Automation Availability for
  checks the repository owns: without automation and without GitHub's secret
  scanning, a documented scan command with a recorded run is a `Pass`.
- Added the [local gate](templates/local-gate/README.md), a script that runs the
  two `R09` checks with `gitleaks` and `osv-scanner`, rates advisories by severity,
  and never reports a pass for a check it could not run, and the
  [private repositories guide](docs/guides/private-repositories.md), which also
  says what code scanning is possible without GitHub's.
- Dependabot alerts and security updates were switched off on the private
  repositories that had them, because Dependabot runs on the minutes the account
  does not have. `P12` and `P13` stay public-only.
- Released as minor: a criterion and a section were added, and no recorded result
  can change. See
  [decision 0018](docs/decisions/0018-private-repositories-run-their-own-checks.md).

## 1.17.0 - 2026-09-21

- Added [Implementation Guides](docs/repository-quality-standard.md#implementation-guides)
  and the material it points to, so that a repository does not have to work out
  how to meet a criterion. There is a [guide](docs/guides/README.md) per group of
  criteria with worked examples, reusable workflows for the secret scan and for
  CodeQL, and a starter kit for Python, Node, .NET, documentation repositories and
  macOS applications. The macOS kit carries the Apple Human Interface Guidelines
  review agent, its instructions and the agentic workflow source, taken from the
  repository that developed them.
- `P13`: default setup and a CodeQL workflow of the repository's own are mutually
  exclusive, so a repository with a workflow is assessed on it and the default
  setup stays off. A Swift package whose default autobuild fails needs the
  workflow with a manual build. This clarifies the criterion and changes no result.
- Released as minor: a section was added, and no recorded result can change. See
  [decision 0017](docs/decisions/0017-how-to-is-published-next-to-what.md).

## 1.16.0 - 2026-09-21

- Added `P12`: Dependabot alerts and Dependabot security updates are enabled on a
  public repository. Both are free, so there is no `Not applicable`. It covers
  the platform half of dependency safety, and `S08` keeps the process half.
- Added `P13`: code scanning runs where CodeQL supports a language of the
  repository, by the default setup, a CodeQL workflow, or an equivalent scanner.
  It is `Not applicable` for a repository with no supported language, and joins
  `S04`, `S09` and `P09` in the runner-only row of
  [Automation Availability](docs/repository-quality-standard.md#automation-availability).
- `scripts/assess.py` reads both from the API, so an agent no longer reads them
  by hand.
- Released as minor: adding criteria cannot weaken a recorded result, and a
  repository assessed against an earlier version is due for reassessment. See
  [decision 0016](docs/decisions/0016-public-repositories-run-the-free-security-scanners.md).
- The settings `P03`, `S05`, `P12` and `P13` describe were enabled on every
  active, non-fork public repository in the account on the day of release.

## 1.15.0 - 2026-09-20

- Added [Deciding Without The Maintainer](docs/repository-quality-standard.md#deciding-without-the-maintainer)
  to Assessment. The assessor decides every result itself, including which gaps
  are intended, from a fixed list of reasons and a fixed order of questions. An
  intended deviation the criterion does not allow is a `Partial` that does not
  lower the state. Intent never excuses the critical and high-priority gaps.
- Reworked `R05` around a smoke kit: a documented command that checks the
  published artifact without anyone operating the product, run by an agent, with
  the result recorded. Operating the core function is no longer required. A
  repository whose artifact cannot be checked without an operator passes on the
  checks that remain, with the limit stated.
- Reworked `D03`: health verification must be a runnable command, and the way
  back must be documented. A rehearsed rollback is welcome and not required.
- Went through all 104 criteria one at a time against an audit of whether the
  text decides a result and whether an agent can meet it. Each criterion now
  states its Pass, Partial, Fail and Not applicable boundaries, or relies on the
  new default results, and where a threshold was needed it gives a minimum
  reading. Nothing was renumbered, removed or added. The audit found no
  criterion that needs a human, and two, `B05` and `R05`, that need a documented
  procedure in the repository.
- Added default results (multi-part criteria, `Not applicable`, judgement words,
  the latest release) to
  [Deciding Without The Maintainer](docs/repository-quality-standard.md#deciding-without-the-maintainer).
- [Overall State](docs/repository-quality-standard.md#overall-state) is now
  computed from the recorded results: `Healthy` when no criterion is `Fail`,
  `Needs work` for any `Fail`, and `At risk` for a `Fail` on a named critical
  criterion. This states what `scripts/conformance.py` already enforced.
- Narrowed the **Deployable** profile to a standing deployment the maintainer
  operates. An application installed from a release, or a script run by hand, is
  no longer Deployable and records `D01`-`D06` as `Not applicable`.
- Repository Statistics: the `P09` card may be published to a dedicated branch,
  `STATS_TOKEN` is never required, and a runner with no card is a `Fail`.
- `A01`-`A04` are `Not applicable` for a repository that is not archived, and
  `B09` and `B12` are `Not applicable` for one that is.
- `unknown` is stated to be a draft marker, not a result, and
  `docs/conformance-record.md` no longer says otherwise.
- `scripts/assess.py` counts templates inherited from the account for `P04`,
  `P10` and `P11`, and decides `A01`-`A04`, `B09` and `B12` for archived
  repositories.
- Closed ten gaps that a first assessment of a real repository exposed, each a
  clarification or widening: `S02` defines the main entry point for a graphical
  application, `S04` covers a range claim with a job on the newest version, `R05`
  says when signature checks alone are a kit and what an assessor that does not
  run downloaded software records, `B13` grades a stale restatement, `P08` treats
  a computed badge as derived, `G02` accepts a linked green run, `G04` no longer
  counts an agreeing repetition as divergence, static hosting such as GitHub Pages
  is not Deployable, `L05` exempts sorting identifiers, and `W04` accepts a page
  that describes the latest release.
- Clarified the evidence for `X01` and `X03`: the assessing agent's review of the
  source counts.
- Released as minor: these changes widen criteria, so a recorded `Fail` may now
  be a `Pass` and no recorded `Pass` can weaken, under
  [Versioning And Compatibility](docs/repository-quality-standard.md#versioning-and-compatibility).
  See [decision 0015](docs/decisions/0015-the-assessor-decides-including-intended-gaps.md).

## 1.14.0 - 2026-09-20

- Widened `R03`: a manual release qualifies when the repository documents the
  steps and the artifacts are built from the commit the tag names. Automation is
  encouraged, not required.
- Widened `R07`: the release notes may link to the changelog entry instead of
  copying it. The failing gate is recommended, not required, and a link to an
  entry with meaningful content also satisfies `R06`.
- Widened `R08`: a true statement that a provenance mechanism is available and
  not used, naming what a consumer can check instead, is a `Pass`. A statement
  that a mechanism is unavailable where it plainly is available remains a `Fail`.
- Clarified `R05`: a smoke-test record stands for later releases until one
  changes how the artifact is built, signed, or packaged.
- Widened `S12`: a third-party action may be pinned by a major-version tag in a
  job with a read-only token and no secret. A commit SHA is asked for only where
  the job can read a secret or write to the repository.
- Stated in [Assessment](docs/repository-quality-standard.md#assessment) that an
  assessment is made by whoever reads the evidence, normally an AI agent, and
  that no maintainer has to perform or attend it. This changes no result.
- `R03` and `R07` leave the runner-only list in
  [Automation Availability](docs/repository-quality-standard.md#automation-availability),
  because both can now be met without a workflow run. A repository with no runner
  that recorded either as `Not applicable` is due for assessment on them. See
  [decision 0014](docs/decisions/0014-release-and-pinning-criteria-scale-with-what-they-protect.md).
- Released as minor: these changes widen a criterion, so a recorded `Fail` may now
  be a `Pass` and no recorded `Pass` can weaken, under
  [Versioning And Compatibility](docs/repository-quality-standard.md#versioning-and-compatibility).

## 1.13.0 - 2026-09-19

- Widened `R07`: the changelog gate may live in a shared release pipeline that
  publishes the repository's releases, provided that pipeline refuses to publish
  without the entry and the repository documents it. A repository does not have
  to own a release workflow to keep release notes and changelog from drifting.
- Widened `R05`: a built artifact needs to have been smoke-tested once as a
  consumer receives it (the published file, installed and launched), with the
  result recorded. A clean environment and automation are no longer required,
  and `R05` no longer needs a runner, so it leaves the runner lists in
  [Automation Availability](docs/repository-quality-standard.md#automation-availability).
- Widened `R08`: where a shared pipeline the repository documents builds and
  publishes its releases, that pipeline's own verifiable record (for a macOS app,
  the Developer ID signature and notarization) is sufficient evidence of origin.
- Widened `R03`: a shared release pipeline started for a specific tag counts as
  automation; the tag push does not have to start it.
- Widened `R01`: where the manifest format has no field for a property, the
  artifact's own metadata file (for an application, `Info.plist`) is its home.
- Released as minor: these changes widen a criterion, so a recorded `Fail` may now
  be a `Pass` and no recorded `Pass` can weaken, under
  [Versioning And Compatibility](docs/repository-quality-standard.md#versioning-and-compatibility).

## 1.12.0 - 2026-09-17

- Retired `W05` and `W06`, which required every published site to vendor
  **Instrument Workshop**, the shared design language. Added `W09`: a site's
  visual design must be made for the project it describes, not left at a
  framework default or reused unchanged from another project. Sites may still
  use Instrument Workshop where it fits; nothing requires or recommends it as
  the default any longer.
  [Site Design](docs/repository-quality-standard.md#site-design) replaces the
  former Design Language subsection. See
  [decision 0013](docs/decisions/0013-sites-are-designed-not-templated.md).
- Released as minor: retiring a criterion narrows applicability and adding one
  widens the catalog, and neither can turn a recorded `Pass` into a `Fail`
  under [Versioning And Compatibility](docs/repository-quality-standard.md#versioning-and-compatibility).

## 1.11.1 - 2026-09-02

- Made
  [Versioning And Compatibility](docs/repository-quality-standard.md#versioning-and-compatibility)
  decided by a property rather than by its four rows. Two changes this repository
  had already shipped landed on no row: a criterion widening so a recorded `Fail`
  could become a `Pass`, which is what correcting `R08`'s escape hatch did in
  1.11.0, and applicability narrowing by a *section* rather than by a profile,
  which is what [Automation
  Availability](docs/repository-quality-standard.md#automation-availability) did
  for `S04`, `S09`, `R03`, `R05`, and `R07` in 1.9.0 and for `P09` in 1.11.0. The
  row covering `Not applicable` read "A profile's applicability narrows", and
  that section is not a profile.
- Both were released as minor, which was right, but the answer was reached by
  reasoning from the two paragraphs under the table rather than from the table
  itself. That reasoning was the actual rule and is now stated as one: the impact
  is decided by what a change can do to a result already recorded against an
  earlier version. The rows are retained as examples, and two are added for the
  cases that were missing.
- This is the same correction 1.9.1 and 1.11.0 applied elsewhere, and the third
  instance of one pattern:
  [decision 0011](docs/decisions/0011-criteria-are-decided-by-the-rule-text.md)
  requires an outcome to attach to a property rather than to an enumeration, and
  a four-row table with no residual case is an enumeration. This one governs
  every change made to the document, including its own.
- Patch, on its own terms: no recorded result can change, since this states the
  rule that has been applied in practice since 1.9.0.

## 1.11.0 - 2026-09-01

- Restated both rows of the
  [Automation Availability](docs/repository-quality-standard.md#automation-availability)
  results table as properties, and added `P09` to the
  `Not applicable` row. Membership was decided by a list of five names rather
  than by the property the row is about, which is the failure
  [decision 0011](docs/decisions/0011-criteria-are-decided-by-the-rule-text.md)
  describes: an outcome attaches to a property because a property survives
  someone extending a list later. The list proved it — written in 1.9.0, it was
  already incomplete against 1.8.0's own `R08`. Each row now states its property
  and names the criteria matching it at this version, so the list illustrates
  the rule instead of being it.
- Corrected `R08`'s escape hatch, which turned on the wrong property. It read
  "where no such mechanism *exists*", so a repository with a runner-derived
  mechanism it could not reach had only `Fail` available, while its siblings
  `R03`, `R05`, and `R07` were `Not applicable` for the identical cause. It now
  turns on whether a mechanism is *available to this repository*, with the two
  ways availability fails named: an ecosystem issuing no provenance at all, and a
  repository with no runner. A repository that could use a mechanism and has not
  is still a `Fail`. `R08` is therefore assessed normally and is not narrowed by
  Automation Availability: its evidence can be a recorded statement, which needs
  no run. Putting it on the `Not applicable` row instead would have repeated the
  defect this release fixes one level down, because membership would then have
  turned on a property of the ecosystem rather than of the criterion, and it
  would have left two stated results for one repository — `Pass` from `R08`'s own
  text and `Not applicable` from the table. It also keeps signal that
  `Not applicable` discards: a repository with no runner must still state that
  its artifacts carry no provenance and why, which is the entire point of a
  criterion whose requirement ends "or the repository states why they cannot".
- `P09` requires a card a workflow reproduces and regenerates on a schedule, and
  says outright that a committed SVG no workflow reproduces is a `Fail`. It is
  Public-profile, so its membership is narrow, but the section already gives the
  case: a public repository whose account has disabled Actions has no runner
  available. Stated the override in both directions, so the `Not applicable`
  covers a repository publishing no card and does not licence one: committing a
  card and presenting it as generated remains a `Fail`, being a false claim
  rather than an absence.
- Swept every criterion whose evidence names a workflow and recorded the result
  here so it is not re-derived. Kept outside the section, each with the reason
  now stated in its closing paragraph: `I06`, which accepts a build script;
  `R04`, which asks whether a tag, a version, and a title agree rather than what
  compared them; `R08`, whose corrected escape hatch a repository with no runner
  can reach; `W01`, which asks for a repeatable documented process rather
  than a workflow; and `S11`, `S12`, and `S13`, which are properties of a
  workflow file that hold whether or not it ever runs. Also checked and left
  outside: `B05` and `G02`, whose successful run is of a documented command
  rather than of a workflow; `R06`, which a changelog alone satisfies; and
  `S05`, whose secret scanning is a platform feature rather than an Actions one.
  `S02`, `S03`, and `L04` stay on the first row, unchanged.
- Fixed the closing paragraph, which claimed the section narrowed "eight
  criteria and one badge position". It narrows nine at this version, and the
  count is now stated as a property of the version rather than as a fact about
  the document.
- Required in [`AGENTS.md`](AGENTS.md) that a new or changed criterion naming a
  workflow run be classified against this section in the same change, and that a
  criterion with an escape hatch be assessed by asking whether the hatch is
  reachable without a runner. Also recorded there that a version bump reassesses
  this repository's own record in the same change, and that `assessed_on` is
  dated in UTC, since the check evaluates it in UTC and a local clock ahead of
  UTC passes every local check before failing in CI.
- This is a minor bump: a recorded `Fail` on `P09` may become `Not applicable`,
  and a recorded `Fail` on `R08` may become `Pass` where no provenance mechanism
  is available to the repository. Both directions are named as minor by
  [Versioning And Compatibility](docs/repository-quality-standard.md#versioning-and-compatibility).
  No recorded `Pass` is invalidated, and no criterion is added, renumbered, or
  retired.

## 1.10.0 - 2026-09-01

- Added `B16`, which requires that the default branch cannot be force-pushed
  over or deleted, evidenced by a branch ruleset or classic branch protection.
  `S09` covers required checks and nothing else, so
  [Automation Availability](docs/repository-quality-standard.md#automation-availability)
  correctly records it as `Not applicable` where no runner is available — and
  once it does, no criterion asked for the branch to survive. `B06` asks only
  that the merge policy be intentional, and "anyone may force push" is an
  intentional policy. A private repository with no runner could therefore record
  `Healthy` with a default branch that could be rewritten or deleted.
- `B16` separates from `S09` by what it protects: `S09` gates what enters the
  branch, `B16` keeps the branch. Blocking a force push and a deletion needs no
  runner, so `B16` is assessed on its ordinary terms everywhere. It is not named
  in the Automation Availability results table, and that section's closing
  paragraph — "So does every criterion not named in the table above" — already
  states that it is assessed normally, so no second statement was added.
- Stated every case `B16` names. Both blocked is a `Pass`, one of the two is a
  `Partial`, neither is a `Fail`, and so is a default branch no ruleset or
  protection covers. A repository whose plan offers no ruleset or branch
  protection mechanism at all records `Not applicable`, and has to say so in the
  evidence its conformance record links to, on the same terms as a missing
  runner. Whether the repository's own administrators may bypass the setting is
  explicitly not part of the criterion, because the person who can lift the
  protection is the person who set it.
- Recorded the scope judgement as
  [decision 0012](docs/decisions/0012-history-on-the-default-branch-is-protected.md),
  including why narrowing `B06` was rejected: it would turn a recorded `Pass`
  into a `Fail`, which is a major change under
  [Versioning And Compatibility](docs/repository-quality-standard.md#versioning-and-compatibility)
  and would invalidate every result in the estate for a gap an appended
  criterion closes at minor cost.
- This is a minor bump: a criterion is added, so no recorded result is
  invalidated and every repository is simply due for reassessment. No criterion
  is renumbered or retired, and no prefix is claimed; `B` is already registered
  to Baseline.
- Taught the draft assessor to decide `B16` from the branch protection facts it
  already collects, and to leave it unknown where that endpoint does not answer.
  A ruleset, an uncovered branch, and a plan without the mechanism all return
  the same `404`, and the standard gives those three cases different results.

## 1.9.1 - 2026-09-01

- Closed a hole in the first
  [Automation Availability](docs/repository-quality-standard.md#automation-availability)
  result row, which 1.9.0 introduced. Its three conditions turned on three
  different properties — whether a successful run could be produced, whether a
  documented command ran the check, and whether the check existed — so they
  sampled rather than partitioned. A repository with a check, a documented
  `B05` command that runs it, and a run that fails matched no condition and had
  no stated result, which is the defect
  [decision 0011](docs/decisions/0011-criteria-are-decided-by-the-rule-text.md)
  exists to prevent. The row now turns on one property, whether the check
  exists: `Fail` where it does not, and otherwise `Pass` where the documented
  `B05` command runs it and the linked evidence records a successful run of
  that command, `Partial` where it does not. The three results are exhaustive
  and mutually exclusive. The `Not applicable` row states one result for a
  named enumeration and has no equivalent hole.
- This is a patch bump: it states an outcome the 1.9.0 text left unstated and
  changes no outcome that text decided. `Pass` and `Fail` keep the cases they
  already had, and the only cases moving into `Partial` are ones that
  previously had no result at all. Precedent is 1.6.1.

## 1.9.0 - 2026-09-01

- Added
  [Automation Availability](docs/repository-quality-standard.md#automation-availability),
  which states what an assessor records for the criteria that name a workflow
  run as their evidence when the repository has no runner. Eight criteria and
  one badge position were previously undecidable in that case: two assessors
  reading `S02` would reasonably record `Fail` and `Not applicable`
  respectively, which is the failure
  [decision 0011](docs/decisions/0011-criteria-are-decided-by-the-rule-text.md)
  exists to prevent. No criterion is added, renumbered, or retired.
- Scoped the rule to whether a runner is available rather than to whether the
  repository is private. Visibility is the common cause and not the property:
  a private repository with a self-hosted runner has automation available, and
  a public repository whose account has disabled Actions does not.
- Split the outcome by what the criterion requires rather than listing eight
  individual answers. `S02`, `S03`, and `L04` describe a check the repository
  owns, so the documented `B05` command produces a `Pass`; `S04`, `S09`, `R03`,
  `R05`, and `R07` describe something a runner does, so they are
  `Not applicable`. `P08` omits the CI badge and promotes nothing into its
  place; committing an image of a status no run produced remains a `Fail`.
- Required the state to be recorded in the evidence the conformance record
  links to before it can be claimed. An unstated possibility is not evidence,
  and the sentence has to be removed when a runner appears.
- This is a minor bump: it narrows criteria so that a result recorded as `Fail`
  may become `Not applicable` or `Pass`, and widens nothing.

## 1.8.0 - 2026-09-01

- Added `S11`, `S12`, and `S13`, covering the part of a repository that runs with
  the most authority and is read the least often. `S11` requires declared token
  permissions, `S12` requires that an executable reference cannot change
  underneath the repository, and `S13` keeps repository secrets out of workflows
  triggered by untrusted contributions. `S12` is graduated by who controls the
  target rather than applied uniformly: a third-party action needs a commit SHA,
  an action published by GitHub may be referenced by major-version tag, and a
  workflow from within the assessed account may be referenced by branch. The
  last is a permission and is stated as one, because pinning a shared reusable
  workflow to a tag would mean re-tagging every consumer before a fix could
  reach them.
- Added `R08`, requiring that a consumer can verify an artifact came from the
  repository that published it, or that the repository states why they cannot.
  `R03` and `R05` already establish that automation built the artifact and that
  it works, and neither says anything about origin. Provenance derived from the
  publishing workflow satisfies it; artifact signing with maintainer-held keys
  and a software bill of materials are both deliberately not required.
- Added `P10` and `P11`, which ask whether issue and pull-request intake collects
  enough to act on. `P04` already asked whether intake was structured, and a
  single box labelled "Description" satisfies that while leaving every report to
  be triaged by conversation. Both are assessed on the information gathered
  rather than on headings or wording.
- Added `B14`, requiring a repository that holds a credential to state how an
  exposed one is revoked and replaced. `S05` detects exposure and `D02` prevents
  it; nothing said what happens afterwards. `GITHUB_TOKEN` alone does not bring a
  repository into scope, since it is issued and revoked per run.
- Added `B15`, requiring a repository that redistributes third-party code to
  state how the obligations of those licences are met. `B03` and `P01` cover a
  repository's own licence only. A repository whose dependencies are resolved by
  the consumer at install time redistributes nothing, and saying so is a `Pass`;
  no inventory, scanner, or compatibility analysis is required.
- Added [Changing This Standard](docs/repository-quality-standard.md#changing-this-standard),
  stating how a criterion is proposed or contested, that the maintainer decides
  and records the reasoning, and that a disputed result is resolved by
  reassessing rather than by editing the record. It also records why proposals
  are ordinary issues: the publishing repository's issue forms are inherited by
  every repository in the account that defines none, so a form specific to this
  document cannot live there.

## 1.7.0 - 2026-08-31

- Added `R07`, requiring that published release notes are generated from the
  changelog entry for the version being released, gated by automation that fails
  the release when the entry is missing, empty, or still held in an unreleased
  section. A repository can keep an exemplary changelog and still publish
  releases whose notes are fixed boilerplate, because nothing connects the two.
  The entries then reach nobody, and the release page is the surface a consumer
  actually lands on.
- Left `R06` unchanged. Narrowing it so that boilerplate notes over an unread
  changelog could no longer pass would be a major change, and it would buy no
  coverage that `R07` does not already provide. The two now divide the work:
  `R06` is about content, `R07` about provenance. See
  [decision 0010](docs/decisions/0010-release-notes-come-from-the-changelog.md).
- Published [`templates/release-notes/`](templates/release-notes/) as the
  reference gate for `R07`, linked from the criterion's prose. A criterion that
  mandates automation has to say where the automation comes from, or every
  repository invents it again.

## 1.6.1 - 2026-08-31

- Closed an ambiguity in the badge image rule, found by the first repository
  assessed against 1.6.0. The committing bullet named license, platform, and
  conformance as qualifying for a committed image, and the following bullet
  granted a `Pass` to a live third-party image "everywhere else". Read together,
  the three named values fell outside "everywhere else" and were left with no
  stated result at all — neither `Pass` nor `Partial` nor `Fail` — which let
  `may` be read as `must`. Committing a qualifying value is now stated as
  permitted and never required, and the `Pass` is tied to the absence of a
  first-party image rather than to "everywhere else". No result changes; 1.6.0
  already excluded a reading that turns a recorded `Pass` into a `Fail`, and
  this states in the rule text what that exclusion implied.

## 1.6.0 - 2026-08-31

- Corrected the reason given for self-hosting images. Both `P08` and `P09`
  claimed that a README image lets its host observe every reader. Markdown
  rendered on `github.com` loads external images through GitHub's proxy, so the
  host sees the proxy, not the reader. The standard already knew this — the
  statistics section relies on the same proxy when it rejects
  `prefers-color-scheme` inside an SVG. `Y02` still carries the argument for a
  published site, where the browser fetches directly and `W07` applies.
- Replaced "served from the repository or a first-party source where practical"
  in the badge section. *Where practical* is not assessable, so every repository
  with a status badge landed on `Partial` with nothing to do about it. The rule
  now turns on how the value changes: a badge image is committed only when a
  repository event regenerates it, and a value that moves on its own is served
  live. A committed image of a moving value is stale by construction, which is
  the failure the section exists to prevent.
- Named GitHub's workflow badge endpoint as the first-party source for CI
  status, so the one required badge that has a first-party live image is no
  longer served by a third party for want of a pointer. A third-party render
  stays a `Pass` and is replaced at reassessment.
- Recorded that a live third-party image is a `Pass` where no first-party source
  exists, which is the case for the latest release. No recorded result can turn
  into a `Fail` from any of this.

## 1.5.1 - 2026-08-30

- Named the Published Site profile in the Language section. A site is the most
  public surface a project has, and it was the one surface the section did not
  name. No outcome changes: every site-publishing repository already matched
  `Software` or `Documentation`, so `L01` and `L02` already applied to it.

## 1.5.0 - 2026-08-30

- Narrowed the **Published Site** profile. The 1.4.0 trigger caught any
  repository whose audience "includes readers who will never open the
  repository", which swept in specifications and templates — documents applied
  *to* repositories by people who are already inside one. The profile now asks
  whether the repository ships something an audience uses without needing the
  source. A page in front of a specification adds a surface to maintain and
  answers nothing its readers were asking.
- Added a versioning rule for exactly this case: narrowing a profile's
  applicability is a minor change, because no recorded `Pass` can become a
  `Fail`. The 1.4.0 table had no row for it.
- Recorded that the shared design language **may** be vendored into public
  repositories. This was the open disclosure question in 1.4.0; copying the
  stylesheets is now expressly permitted, which unblocks `W05`.

## 1.4.0 - 2026-08-29

- Added the **Published Site** profile and criteria `W01`-`W08`. A repository is
  read by contributors; a site is read by everyone else, and serving the second
  audience from a README is why READMEs grow until nobody reads them. The
  profile covers publication, two-way linking between repository and site, what
  a landing page carries, use of the shared design language, and the absence of
  third-party resources.
- Added **Content Boundaries**, which states where each fact lives across the
  description, the site, `README.md`, `docs/`, decision records, the changelog,
  and `AGENTS.md`. A fact stated twice gets updated once, and the stale copy
  still looks authoritative.
- Added `B13`, requiring that each fact has one home and other documents link to
  it rather than restate it. Generated restatement is explicitly exempt: a
  badge, a record, or a statistics card cannot drift, because none of them is
  edited by hand.
- Claimed the `W` prefix.

## 1.3.3 - 2026-08-25

- The account overview now reports the repository count as `sources / all`, for
  example `68 / 79`. The cards deliberately ignore forks, but GitHub's profile
  page counts them, so the bare source count looked like a miscount. The second
  figure is omitted when the account owns no forks.

## 1.3.2 - 2026-08-25

- Stopped tracking generated statistics cards on `main`, where stale copies
  survived every run and were carried onto the `stats` branch.
- Fixed the repository card drawing a row of minimum-height bars when GitHub
  has not computed commit activity yet, which read as a broken chart rather
  than as missing data.

## 1.3.1 - 2026-08-25

- Fixed generated statistics cards sizing themselves from hard-coded heights,
  which pushed the twelfth repository row and the footer outside the card.
- Fixed the repository table overflowing its right edge and truncating language
  names.
- Removed the animations from every card so they render identically in browsers
  and in renderers that snapshot the first frame.
- Added month, weekday and intensity labels to the contribution graph, placed
  days by their real weekday, and replaced the multi-hue heat scale with an
  ordered single-hue ramp.
- Fixed `cards.account` being ignored, so configuring the card list now works.
- Changed relative minutes from `m` to `min`, which was indistinguishable from
  months, and shortened the generated timestamp to minute precision.

## 1.3.0 - 2026-08-24

- Added the public criterion `P09` and the Repository Statistics section,
  requiring repository activity to be shown from a self-hosted generated card
  rather than a third-party image service.
- Added a self-hosted statistics generator, a reusable workflow that renders and
  commits a per-repository card, account-level cards for the profile README,
  copy-paste templates, documentation, and tests.
- Updated this repository's conformance record for `P09` and aligned the
  statistics tests with the standard-library `unittest` convention.

## 1.2.0 - 2026-08-22

- Added a versioning and compatibility policy, the append-only rule for
  criterion identifiers, a prefix register, and a pinned citation form.
- Added per-criterion anchors and published `standard.yml`, a generated
  machine-readable catalog kept in sync by a required check.
- Added the Agent Readiness criteria `G01`-`G08`, covering tool-neutral
  `AGENTS.md` instructions, authoritative commands, explicit forbidden
  operations, and attribution of agent-authored changes.
- Added the Language And Localization criteria `L01`-`L07`, establishing English
  as the default user-facing language, requiring localization support to be
  declared, and documenting the German-content exception.
- Added the Accessibility criteria `X01`-`X05`, scoped to barriers a single
  maintainer can reasonably avoid without paid tooling.
- Added the Data Protection And Privacy criteria `Y01`-`Y06`, covering
  disclosure of collected data, network destinations, telemetry defaults, and
  third-party recipients.
- Added baseline criteria `B11` and `B12` for conformance records and the
  `trsdn-standard` discovery topic, and public criterion `P08` for the badge
  convention.
- Added the conformance record format, a reusable badge workflow, and this
  repository's own self-assessment.
- Added `tests/`, covering both validation scripts through their command line and
  asserting the specific diagnostic for every rejection path, run in CI as
  `Script tests`.
- Fixed ageing in `scripts/conformance.py --check`: a record older than the
  review cadence previously only failed when the badge also disagreed, so
  regenerating the badge silenced the reminder without a reassessment. Ageing is
  now an independent failure that only a fresh assessment clears.

## 1.1.0 - 2026-08-21

- Added the Product Identity requirements `I01`-`I06`, covering embedded
  version, repository and issue tracker URLs, license and copyright, an
  in-product version and links, product icons, and build-generated metadata.
- Rewrote the shared security, contribution, conduct, support, issue, and
  pull-request defaults so they are correct for every repository that inherits
  them, instead of describing this repository only.

## 1.0.0 - 2026-08-21

- Published the canonical public repository quality standard.
- Added default security, contribution, conduct, support, issue, and pull-request
  guidance for public `trsdn` repositories.
- Added Markdown validation and dependency-update automation.
