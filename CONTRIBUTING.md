# Contributing

Contributions that improve the public repository standard or shared templates
are welcome.

Changes must preserve the outcomes and evidence model in the
[Repository Quality Standard](docs/repository-quality-standard.md).

## Propose a change

1. Open an issue describing the repository problem or use case.
2. Create a focused branch and update the standard or template.
3. Run the documented validation command from a clean checkout.
4. Open a pull request with the evidence requested by the template.

Keep requirements outcome-focused and technology-neutral. A new requirement
must identify durable evidence and must not assume access to private systems.
Repository-specific requirements belong in that repository.

## Validation

```sh
npx --yes markdownlint-cli2@0.18.1 "**/*.md"
```

The command must exit successfully before review. Update affected examples and
templates with the standard so they do not drift.

## Review expectations

- Link the issue or rationale for the change.
- Explain compatibility or migration impact.
- Do not include secrets, private repository details, personal data, or private
  incident information.
- Record material semantic changes in the pull request description.
