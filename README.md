# trsdn repository standards

This repository contains the public repository quality standard and default
community health files for projects maintained by `trsdn`.

## Canonical standard

The [Repository Quality Standard](docs/repository-quality-standard.md) defines
the evidence required for maintainable public repositories. Repository-specific
requirements may be stricter, but must not silently weaken this baseline.

## Statistics

- [Profile statistics](docs/profile-stats.md) describes the self-hosted account cards rendered for `trsdn`.
- [Repository stats](docs/repo-stats.md) explains how an individual repository adds its generated stats card.

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

## Validation

From a clean checkout, run:

```sh
npx --yes markdownlint-cli2@0.18.1 "**/*.md"
```

## License

The content and templates in this repository are available under the
[MIT License](LICENSE).
