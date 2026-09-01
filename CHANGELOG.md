# Changelog

All material changes to the public standard and shared community files are
recorded here.

Versions follow the compatibility policy in the
[Repository Quality Standard](docs/repository-quality-standard.md).

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
