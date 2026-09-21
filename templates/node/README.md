# Node and TypeScript starter kit

Copy-and-edit workflows for a Node or TypeScript repository. Nothing here is
applied to a repository automatically.

## Contents

| File | What it does |
|---|---|
| `.github/workflows/ci.yml` | Lint, tests on a Node version matrix, and a package dry run. Expects `lint`, `build`, and `test` scripts. |
| `.github/workflows/secret-scan.yml` | Calls the shared secret scan on push, pull request, and weekly. |
| `.github/workflows/codeql.yml` | Optional. Calls the shared CodeQL workflow for `javascript-typescript`. |
| `.github/dependabot.yml` | Version updates for `npm` and `github-actions`, with minor and patch updates grouped. |

## Order of adoption

1. Make sure `package.json` has `lint` and `test` scripts and that `npm ci`
   works from a committed lockfile. For TypeScript, have `lint` or a second
   script run `tsc --noEmit`.
2. Copy `.github/workflows/ci.yml`. Set the Node versions you support. Delete
   the `package` job for an application.
3. Copy `secret-scan.yml` and `dependabot.yml`.
4. Decide about CodeQL. Default setup already covers JavaScript and
   TypeScript, so most repositories copy nothing. Read the
   [CodeQL guide](../../docs/guides/codeql.md) before adding `codeql.yml`,
   because the two cannot both be enabled.
5. Write a [first conformance record](../conformance-first-record.md).

## Criteria this kit serves

| Criterion | Where |
|---|---|
| [`S02`](../../docs/repository-quality-standard.md#s02) | The test job. The [tests and lint guide](../../docs/guides/tests-and-lint.md) says what a useful suite contains, including for a static site. |
| [`S03`](../../docs/repository-quality-standard.md#s03) | The lint job. |
| [`S05`](../../docs/repository-quality-standard.md#s05) | `secret-scan.yml`. See the [secret scanning guide](../../docs/guides/secret-scanning.md). |
| [`S08`](../../docs/repository-quality-standard.md#s08) | `dependabot.yml`. See the [Dependabot guide](../../docs/guides/dependabot.md). |
| [`S11`](../../docs/repository-quality-standard.md#s11), [`S12`](../../docs/repository-quality-standard.md#s12) | `permissions` in every workflow, and the pinning choices. See the [permissions and pinning guide](../../docs/guides/workflow-permissions-and-pinning.md). |
| [`P13`](../../docs/repository-quality-standard.md#p13) | `codeql.yml`, or default setup. |
| [`B05`](../../docs/repository-quality-standard.md#b05) | The scripts `ci.yml` runs are the commands to document in your README. |
