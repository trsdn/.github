# Python starter kit

Copy-and-edit workflows for a Python repository. Nothing here is applied to a
repository automatically.

## Contents

| File | What it does |
|---|---|
| `.github/workflows/ci.yml` | Lint, format check, tests with a coverage floor, and a build, on a version matrix. Uses `uv`. |
| `.github/workflows/secret-scan.yml` | Calls the shared secret scan on push, pull request, and weekly. |
| `.github/workflows/codeql.yml` | Optional. Calls the shared CodeQL workflow for Python. |
| `.github/dependabot.yml` | Version updates for `uv` (or `pip`) and `github-actions`. |

## Order of adoption

1. Copy `.github/workflows/ci.yml` and replace `PACKAGE_NAME` and the version
   matrix. Commit a `uv.lock` and a `pytest` and `ruff` dev dependency group.
   Skip this step if you use `pip` and adapt the install and run lines.
2. Copy `secret-scan.yml`.
3. Copy `dependabot.yml`. Pick `uv` or `pip`, and add an entry for every
   directory that has a manifest.
4. Decide about CodeQL. Default setup already covers Python, so most
   repositories copy nothing. Read the [CodeQL guide](../../docs/guides/codeql.md)
   before adding `codeql.yml`, because the two cannot both be enabled.
5. Write a [first conformance record](../conformance-first-record.md).

## Criteria this kit serves

| Criterion | Where |
|---|---|
| [`S02`](../../docs/repository-quality-standard.md#s02) | The test step. The [tests and lint guide](../../docs/guides/tests-and-lint.md) says what a useful suite contains. |
| [`S03`](../../docs/repository-quality-standard.md#s03) | The lint and format steps. A type checker is optional and commented in. |
| [`S05`](../../docs/repository-quality-standard.md#s05) | `secret-scan.yml`. See the [secret scanning guide](../../docs/guides/secret-scanning.md). |
| [`S08`](../../docs/repository-quality-standard.md#s08) | `dependabot.yml`. See the [Dependabot guide](../../docs/guides/dependabot.md). |
| [`S11`](../../docs/repository-quality-standard.md#s11), [`S12`](../../docs/repository-quality-standard.md#s12) | `permissions` in every workflow, and the pinning choices. See the [permissions and pinning guide](../../docs/guides/workflow-permissions-and-pinning.md). |
| [`P13`](../../docs/repository-quality-standard.md#p13) | `codeql.yml`, or default setup. |
| [`B05`](../../docs/repository-quality-standard.md#b05) | The commands in `ci.yml` are the ones to document in your README. |
