# Changelog

All material changes to the public standard and shared community files are
recorded here.

Versions follow the compatibility policy in the
[Repository Quality Standard](docs/repository-quality-standard.md).

## 1.8.0 - 2026-09-01

- Added [Automation Without A Runner](docs/repository-quality-standard.md#automation-without-a-runner),
  which states what an assessor records for `S02`, `S03`, `S04`, `R03`, `R05`,
  `R07`, and the continuous integration badge when the repository has no runner
  available to it. Hosted Actions minutes are free for public repositories and
  metered for private ones, and no self-hosted runner has to exist, so a private
  repository can be maintained to a high standard and still be unable to produce
  a workflow run. None of those criteria said what happens then, which left the
  result to the assessor and made it unreproducible — the defect
  [decision 0011](docs/decisions/0011-criteria-are-decided-by-the-rule-text.md)
  exists to prevent.
- Defined runner availability as a property of the repository rather than of its
  visibility, established from its Actions settings and the owning account's
  allowance. A private repository with a minutes allowance or a self-hosted
  runner has a runner and is assessed as written, and a missing workflow file is
  never an exemption.
- Narrowed `S04` so it is `Not applicable` where the repository has no runner. A
  matrix over runtimes cannot be produced by one maintainer on one machine, so
  the previous reading could only ever record `Fail` for a reason unrelated to
  quality. This is the minor case in the compatibility table: a recorded `Fail`
  can become `Not applicable`, and no recorded `Pass` is invalidated.
- Left `S09`, `L04`, and `B05` untouched, and said so in the rule text. `S09` is
  already limited to checks that exist, `L04` already accepts a validation
  command in place of a CI check, and `B05` is the criterion that carries the
  substitute work. Naming them keeps the next reader from inferring a scope the
  section does not have.
- No recorded `Pass` becomes a `Fail` from any of this, and unlike 1.6.1 that is
  a property of the rule text rather than a sentence in this entry: reaching
  `Pass` on the affected criteria already required a workflow run, so a
  repository that reached one has a runner and this section never applies to it.

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
