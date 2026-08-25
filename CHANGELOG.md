# Changelog

All material changes to the public standard and shared community files are
recorded here.

Versions follow the compatibility policy in the
[Repository Quality Standard](docs/repository-quality-standard.md).

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
