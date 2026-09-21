# .NET starter kit

Copy-and-edit workflows for a C# repository. Nothing here is applied to a
repository automatically.

## Contents

| File | What it does |
|---|---|
| `.github/workflows/ci.yml` | Restore, `dotnet format --verify-no-changes`, build, and test. Runs on Windows by default. |
| `.github/workflows/codeql.yml` | CodeQL for C# with a manual build. This is an advanced workflow and cannot be a shared one, because the build is yours. |
| `.github/workflows/secret-scan.yml` | Calls the shared secret scan on push, pull request, and weekly. |
| `.github/dependabot.yml` | Version updates for `nuget`, optional `npm`, and `github-actions`, with grouping examples. |

## Order of adoption

1. Copy `ci.yml`. Replace `MySolution.sln`, the SDK version, and the runner.
   Use `ubuntu-latest` if nothing targets `net*-windows`.
2. Copy `secret-scan.yml` and `dependabot.yml`. Delete the `npm` entry if there
   is no `package.json`.
3. Decide about CodeQL, with the [CodeQL guide](../../docs/guides/codeql.md).
   Default setup can analyse C# with no build. If you want a real build, extra
   queries, or a Windows runner, copy `codeql.yml` and switch default setup off
   first: the two cannot both be enabled.
4. Write a [first conformance record](../conformance-first-record.md).

## Criteria this kit serves

| Criterion | Where |
|---|---|
| [`S02`](../../docs/repository-quality-standard.md#s02) | The test step. The [tests and lint guide](../../docs/guides/tests-and-lint.md) says what a useful suite contains. |
| [`S03`](../../docs/repository-quality-standard.md#s03) | The format check, which goes beyond compiling. |
| [`S05`](../../docs/repository-quality-standard.md#s05) | `secret-scan.yml`. See the [secret scanning guide](../../docs/guides/secret-scanning.md). |
| [`S08`](../../docs/repository-quality-standard.md#s08) | `dependabot.yml`. See the [Dependabot guide](../../docs/guides/dependabot.md). |
| [`S11`](../../docs/repository-quality-standard.md#s11), [`S12`](../../docs/repository-quality-standard.md#s12) | `permissions` in every workflow, and the pinning choices. See the [permissions and pinning guide](../../docs/guides/workflow-permissions-and-pinning.md). |
| [`P13`](../../docs/repository-quality-standard.md#p13) | `codeql.yml`, or default setup. A repository with C# and TypeScript lists both languages. |
| [`B05`](../../docs/repository-quality-standard.md#b05) | The `dotnet` commands in `ci.yml` are the ones to document in your README. |
