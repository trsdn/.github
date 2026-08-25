# trsdn repository standards

[![License](https://img.shields.io/github/license/trsdn/.github)](LICENSE)
[![Markdown](https://github.com/trsdn/.github/actions/workflows/markdown.yml/badge.svg)](https://github.com/trsdn/.github/actions/workflows/markdown.yml)
[![Standard](https://github.com/trsdn/.github/actions/workflows/standard.yml/badge.svg)](https://github.com/trsdn/.github/actions/workflows/standard.yml)
[![Conformance](.github/badges/conformance.svg)](docs/self-assessment.md)

This repository contains the public repository quality standard, default
community health files, and self-hosted statistics tooling for projects
maintained by `trsdn`.

Its language is English, and it ships no localized content. See `L01` and `L03`.

## Canonical standard

The [Repository Quality Standard](docs/repository-quality-standard.md) defines
the evidence required for maintainable public repositories. Repository-specific
requirements may be stricter, but must not silently weaken this baseline.

[`standard.yml`](standard.yml) is the same content in machine-readable form,
generated from the document and kept in sync by a required check.

Repository statistics for `P09` are documented in
[Repository stats](docs/repo-stats.md), and account-level cards are documented in
[Profile statistics](docs/profile-stats.md).

### Citing a criterion

Cite the pinned form, never the default branch:

```text
https://github.com/trsdn/.github/blob/v1.3.3/docs/repository-quality-standard.md#p09
```

Criterion identifiers are append-only and are never reused, so a citation keeps
its meaning. See
[decision 0001](docs/decisions/0001-criterion-identifiers-are-permanent.md).

## Applying the standard to a repository

1. Assess the repository against a published version of the standard.
2. Record the result in `.github/conformance.yml`, following the
   [record format](docs/conformance-record.md).
3. Generate the badge from the record and commit it.
4. Add the `trsdn-standard` topic so the repository appears in the inventory.
5. Call the reusable check:

   ```yaml
   jobs:
     conformance:
       uses: trsdn/.github/.github/workflows/conformance.yml@main
   ```

The topic marks a repository as *assessed*, not as *passing*. The outcome lives
only in the record.

### Inventory

```sh
gh search repos --owner trsdn --topic trsdn-standard --limit 100 \
  --json fullName,isArchived
```

The difference between that list and the full account list is the outstanding
assessment backlog.

## This repository's own result

State: **Needs work**. One criterion fails and four are partial, detailed in the
[self-assessment](docs/self-assessment.md). Publishing a green badge over known
gaps would devalue every other badge in the estate.

## Default community files

GitHub can use the governance and contribution files in this repository for
public `trsdn` repositories that do not provide their own versions. A file in an
individual repository takes precedence when project-specific guidance is
needed.

- [Security policy](SECURITY.md)
- [Contributing guide](CONTRIBUTING.md)
- [Code of conduct](CODE_OF_CONDUCT.md)
- [Support guide](SUPPORT.md)
- [Issue forms](.github/ISSUE_TEMPLATE)
- [Pull request template](.github/pull_request_template.md)

Default files improve consistency, but they do not configure branch protection,
CI, dependency updates, vulnerability alerts, or secret scanning in other
repositories. Those controls must be enabled and verified per repository.

## Templates

- [`templates/AGENTS.md`](templates/AGENTS.md) — starting point for the agent
  readiness criteria `G01` to `G08`.
- [`templates/repo-stats/`](templates/repo-stats/) — caller workflow and README
  snippet for the `P09` repository statistics card.

## Contributing

Agent and contributor guidance for this repository is in
[`AGENTS.md`](AGENTS.md). Decisions behind the standard are recorded in
[`docs/decisions/`](docs/decisions).

## Validation

From a clean checkout, run the repository validation commands:

```sh
python3 scripts/standard.py --check
python3 scripts/conformance.py --check
python3 -m unittest discover -s tests -v
npx --yes markdownlint-cli2@0.18.1 "**/*.md"
```

The standard and conformance scripts, and their tests, use the Python standard
library only. The statistics generator is separate runtime tooling and installs
`requests` from `requirements.txt` when its workflows run. Markdown linting pins
its tool version.

## Privacy

This repository collects nothing and stores no user data. Routine validation only
resolves `markdownlint-cli2` from the npm registry. The optional statistics
generator contacts the GitHub API to render repository and account SVG cards. See
`Y01` and `Y02`.

## License

The content and templates in this repository are available under the
[MIT License](LICENSE).
