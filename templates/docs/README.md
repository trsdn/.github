# Documentation and content starter kit

Copy-and-edit workflows for a repository that is mostly prose, such as notes,
a guide, or a static site's content. Nothing here is applied to a repository
automatically.

## Contents

| File | What it does |
|---|---|
| `.github/workflows/markdown.yml` | Lints every Markdown file with a pinned `markdownlint-cli2`. |
| `.github/workflows/links.yml` | Fails when a relative link between files in the repository is broken. External links are not checked. |
| `.github/workflows/secret-scan.yml` | Calls the shared secret scan on push, pull request, and weekly. |
| `.github/dependabot.yml` | Version updates for `github-actions`, the only ecosystem a prose repository has. |

The Markdown workflow is a copy, not a call, because the workflow in the shared
repository is not published as a reusable one.

## Order of adoption

1. Copy `markdown.yml` and run `npx --yes markdownlint-cli2@0.18.1 "**/*.md"`
   locally first. Add a `.markdownlint-cli2.yaml` for the rules you decide to
   relax, with a reason next to each.
2. Copy `links.yml`.
3. Copy `secret-scan.yml` and `dependabot.yml`.
4. CodeQL has nothing to analyse in prose, so `P13` is not applicable unless the
   repository holds code. If it holds scripts, follow the
   [CodeQL guide](../../docs/guides/codeql.md).
5. Write a [first conformance record](../conformance-first-record.md).

## Criteria this kit serves

| Criterion | Where |
|---|---|
| [`S02`](../../docs/repository-quality-standard.md#s02) | The link check is a check that fails. The [tests and lint guide](../../docs/guides/tests-and-lint.md) shows a failure-path check for a content repository. |
| [`S03`](../../docs/repository-quality-standard.md#s03) | `markdown.yml`. |
| [`S05`](../../docs/repository-quality-standard.md#s05) | `secret-scan.yml`. See the [secret scanning guide](../../docs/guides/secret-scanning.md). |
| [`S08`](../../docs/repository-quality-standard.md#s08) | `dependabot.yml`. See the [Dependabot guide](../../docs/guides/dependabot.md). |
| [`S11`](../../docs/repository-quality-standard.md#s11), [`S12`](../../docs/repository-quality-standard.md#s12) | `permissions` in every workflow, and one outside action pinned by SHA as the worked example. See the [permissions and pinning guide](../../docs/guides/workflow-permissions-and-pinning.md). |
| [`B05`](../../docs/repository-quality-standard.md#b05) | The lint command is the one to document in your README. |
