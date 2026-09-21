# Decisions

Architectural decision records for the Repository Quality Standard. Each record
captures a decision that is not obvious from the standard itself, so that a
future reader can see why it is the way it is before changing it.

| ID | Decision | Status |
|---|---|---|
| [0001](0001-criterion-identifiers-are-permanent.md) | Criterion identifiers are permanent and prefixes are centrally registered | Accepted |
| [0002](0002-versioning-and-citation.md) | The standard is versioned, tagged, and cited by pinned reference | Accepted |
| [0003](0003-agent-readiness.md) | Agent instructions live in a tool-neutral `AGENTS.md` | Accepted |
| [0004](0004-language-and-localization.md) | English is the default language, with a declared exception | Accepted |
| [0005](0005-proportionate-accessibility-and-privacy.md) | Accessibility and privacy criteria stay at a level one maintainer can meet | Accepted |
| [0006](0006-conformance-topic-badge-and-record.md) | Conformance is recorded in a file, discovered by topic, and shown by a generated badge | Accepted |
| [0007](0007-testing-the-validation-scripts.md) | The validation scripts are tested through their command line, asserting exit code and diagnostic | Accepted |
| [0008](0008-internal-links-are-checked-external-links-are-not.md) | Internal links and anchors are checked in CI; external links are deliberately not | Accepted |
| [0009](0009-published-sites-and-content-boundaries.md) | Published sites carry the shared design language, and each fact has one home | Accepted |
| [0010](0010-release-notes-come-from-the-changelog.md) | Release notes are generated from the changelog, and `R06` stays as it is | Accepted |
| [0011](0011-criteria-are-decided-by-the-rule-text.md) | A criterion is decided by its rule text alone, and a rule this repository cannot violate visibly is untested here | Accepted |
| [0012](0012-history-on-the-default-branch-is-protected.md) | History on the default branch is protected by its own criterion rather than by narrowing `B06` | Accepted |
| [0014](0014-release-and-pinning-criteria-scale-with-what-they-protect.md) | Release and pinning criteria ask for the property, and recommend the mechanism | Accepted |
| [0015](0015-the-assessor-decides-including-intended-gaps.md) | The assessor decides every result, including which gaps are intended, from a closed list of reasons | Accepted |
| [0016](0016-public-repositories-run-the-free-security-scanners.md) | Public repositories run the free security scanners | Accepted |
| [0017](0017-how-to-is-published-next-to-what.md) | How to meet a criterion is published next to it, as guides, starter kits and reusable workflows, and never replaces it | Accepted |
| [0018](0018-private-repositories-run-their-own-checks.md) | Private repositories run their own release checks, and the standard says per criterion what applies to them | Accepted |
| [0019](0019-agent-reviewers-run-locally-as-versioned-packages.md) | Agent reviewers run locally as versioned packages, not as workflows | Accepted |
