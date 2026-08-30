# Changelog

All material changes to the public standard and shared community files are
recorded here.

Versions follow the compatibility policy in the
[Repository Quality Standard](docs/repository-quality-standard.md).

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
