# Secret scanning

Serves [`S05`](../repository-quality-standard.md#s05): secret scanning runs on
commits and pull requests.

## A private repository

GitHub's secret scanning and push protection are not offered to a private
repository on a plan without them, and a scanner workflow needs minutes. Run
`gitleaks` locally through the
[local gate](../../templates/local-gate/README.md), which scans the history too.
See [Private repositories](private-repositories.md).

## Two mechanisms

**GitHub secret scanning and push protection** are repository settings. Secret
scanning looks for known credential formats in the repository. Push protection
rejects a push that contains one before it lands. They cost nothing on a public
repository and need no file.

**A Gitleaks workflow** runs in CI on every push and pull request and scans the
commits in it. It is a file, so it is visible evidence in the repository, and it
also catches patterns GitHub does not.

Either satisfies `S05`. The trouble with the settings alone is evidence: an
assessor without admin rights often cannot read them, so a repository relying on
them should say so in its assessment. The trouble with a workflow alone is that
it reports after the push, not before. Using both is inexpensive: the setting
prevents, the workflow proves.

A hand-written script that greps for a few patterns is not a substitute. It
misses most credential formats.

## The shared workflow

Call the shared workflow instead of copying a scan into every repository:

```yaml
name: Secret scan

on:
  push:
    branches: [main]
  pull_request:
  schedule:
    - cron: "17 4 * * 1"
  workflow_dispatch:

permissions:
  contents: read

jobs:
  scan:
    uses: trsdn/.github/.github/workflows/secret-scan.yml@main
```

The same file is in every language kit, for example the
[Python kit](../../templates/python/.github/workflows/secret-scan.yml). Because
the reference is to a workflow in the same account, `main` is allowed, and a
fix to the scan reaches every repository without a pull request in each. See
[`S12`](../repository-quality-standard.md#s12).

The weekly run covers history that a push-only scan never revisits.

## Licence

Gitleaks' own action requires a licence key for repositories owned by an
organisation. A repository owned by a personal account does not need one. The
standard does not require a paid tool, so if a repository moves into an
organisation, use the GitHub setting for `S05` or run the free Gitleaks binary
directly rather than buying a licence.

## If a secret is found

Treat it as leaked. Rotate it first, then remove it from the code. Rewriting
history does not un-leak it. Push protection reporting a block means stop and
rotate, not retry.
