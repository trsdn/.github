# Guides

The [standard](../repository-quality-standard.md) says what must be true. These
guides and the [templates](../../templates/) say how to make it true, with worked
examples taken from repositories that already meet the criteria. A guide never
replaces the criterion: where they disagree, the criterion decides, and a copied
file is not evidence until the repository has it and it works there.

## By criterion

| Criteria | Read |
|---|---|
| [`P03`](../repository-quality-standard.md#p03), [`P12`](../repository-quality-standard.md#p12), [`S05`](../repository-quality-standard.md#s05), [`B16`](../repository-quality-standard.md#b16), [`S09`](../repository-quality-standard.md#s09) | [Repository security settings](repository-security-settings.md) |
| [`P13`](../repository-quality-standard.md#p13) | [CodeQL](codeql.md) |
| [`S08`](../repository-quality-standard.md#s08), [`P12`](../repository-quality-standard.md#p12) | [Dependabot version updates](dependabot.md) |
| [`S05`](../repository-quality-standard.md#s05) | [Secret scanning](secret-scanning.md) |
| [`S11`](../repository-quality-standard.md#s11), [`S12`](../repository-quality-standard.md#s12), [`S13`](../repository-quality-standard.md#s13) | [Workflow permissions and pinning](workflow-permissions-and-pinning.md) |
| [`S02`](../repository-quality-standard.md#s02), [`S03`](../repository-quality-standard.md#s03) | [Tests and lint](tests-and-lint.md) |
| [`B11`](../repository-quality-standard.md#b11) | [The first conformance record](../../templates/conformance-first-record.md) |
| Any workflow that several repositories share | [Reusable workflows](reusable-workflows.md) |
| A macOS application: `R03`, `R05`, `R07`, `R08`, `I01`-`I06`, `X01`-`X03`, `S03` | [Bringing a macOS app to the standard](macos-app.md) |

## Starter kits

Copy the kit for the repository's language family, edit the `TODO(...)` markers,
and read its README first. Each kit says which criteria its files serve.

| Kit | For |
|---|---|
| [`templates/macos-app/`](../../templates/macos-app/README.md) | A Swift package or Xcode macOS application, with the Apple Human Interface Guidelines review agent |
| [`templates/python/`](../../templates/python/README.md) | A Python project |
| [`templates/node/`](../../templates/node/README.md) | A Node or TypeScript project |
| [`templates/dotnet/`](../../templates/dotnet/README.md) | A .NET project, including CodeQL for C# |
| [`templates/docs/`](../../templates/docs/README.md) | A repository of documentation or content |

Older single-purpose templates remain:
[`templates/AGENTS.md`](../../templates/AGENTS.md),
[`templates/release-notes/`](../../templates/release-notes/), and
[`templates/repo-stats/`](../../templates/repo-stats/).

## Shared workflows

These are referenced from another repository in the account instead of copied, as
`trsdn/.github/.github/workflows/NAME.yml@main`. [The guide](reusable-workflows.md)
lists them, their inputs, and how to change one without breaking its callers.
