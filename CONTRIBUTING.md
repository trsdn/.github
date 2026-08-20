# Contributing

Thanks for contributing. This guide applies to `trsdn` projects that do not
publish their own contributing guide.

## Before you start

Open an issue for bugs, new capabilities, or anything that changes behavior, so
the approach can be agreed before implementation. Small, focused pull requests
are reviewed faster than broad ones.

## Make the change

1. Branch from the default branch.
2. Follow the setup instructions in the project's `README.md`.
3. Match the existing structure and style of the project.
4. Add or update tests when behavior changes.
5. Update documentation and the changelog when the change is user-visible.

## Validate before review

Run the project's documented validation command from a clean checkout and make
sure it succeeds. If the project documents no command, describe in the pull
request how you verified the change.

## Open a pull request

- Describe the problem, the change, and how it was verified.
- Link the related issue.
- Call out user-visible, operational, security, or compatibility impact.
- Never include secrets, credentials, personal data, or internal-only details.

Maintainers review for correctness, security, maintainability, and scope. A pull
request may be asked to shrink, split, or add evidence before it is merged.

The quality expectations behind these projects are described in the
[Repository Quality Standard](https://github.com/trsdn/.github/blob/main/docs/repository-quality-standard.md).
