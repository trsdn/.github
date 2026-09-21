# Dependabot version updates

Serves [`S08`](../repository-quality-standard.md#s08): dependency updates and
vulnerability triage have an owner and a process.

## Not for a private repository without minutes

Dependabot runs on Actions minutes in a private repository. Where the account has
none to spare, leave Dependabot off there, alerts and security updates and any
`dependabot.yml` alike, and audit dependencies at release with the
[local gate](../../templates/local-gate/README.md) instead. See
[Private repositories](private-repositories.md).

## Two different things

- **Dependabot alerts and security updates** are repository settings. They warn
  about known vulnerabilities and open fixes for them. They need no file in the
  repository, and [`P12`](../repository-quality-standard.md#p12) reads the
  settings.
- **Version updates** are configured by `.github/dependabot.yml`. They keep
  dependencies and workflow actions current. This is what `S08` looks for.

Enabling one does not enable the other.

## The file

One `updates` entry per ecosystem and per directory that holds a manifest.
Every repository with workflows needs a `github-actions` entry, which is also
what keeps pinned action SHAs current, as the
[permissions and pinning guide](workflow-permissions-and-pinning.md) explains.
Complete files per language are in the kits:
[Python](../../templates/python/.github/dependabot.yml),
[Node](../../templates/node/.github/dependabot.yml),
[.NET](../../templates/dotnet/.github/dependabot.yml), and
[documentation](../../templates/docs/.github/dependabot.yml).

Every entry starts from this shape:

```yaml
version: 2
updates:
  - package-ecosystem: ECOSYSTEM
    directory: /
    schedule:
      interval: weekly
```

## Snippets per ecosystem

Set `package-ecosystem` and `directory` as shown, and keep the rest of the shape.

| Ecosystem | `package-ecosystem` | Manifest it reads | Notes |
|---|---|---|---|
| Python with `pip` | `pip` | `requirements*.txt`, `pyproject.toml` | |
| Python with `uv` | `uv` | `uv.lock` and `pyproject.toml` | Use instead of `pip`, not beside it. |
| Node | `npm` | `package.json` and its lockfile | Also covers pnpm and yarn projects. |
| .NET | `nuget` | `*.csproj`, `Directory.Packages.props` | |
| GitHub Actions | `github-actions` | `.github/workflows/*.yml` | `directory: /` covers the workflows folder. |
| Swift | `swift` | `Package.swift` | For Swift Package Manager. Not for an Xcode project's own package references. |
| Docker | `docker` | `Dockerfile` | One entry per directory with a Dockerfile. |

Check GitHub's Dependabot documentation for the current list of ecosystem names
before relying on one here, because names and support change.

## Grouping

Grouping turns many pull requests into a few. Group the ones that move
together, or that you would merge together:

```yaml
    groups:
      github-actions:
        patterns:
          - "*"
```

For packages that must move together, name them by pattern, such as
`Microsoft.Extensions.*`. Keep major versions out of a group with
`update-types: [minor, patch]`, so a breaking change gets its own review.

## A monorepo

Add one entry per directory that has a manifest:

```yaml
  - package-ecosystem: pip
    directory: /python
    schedule:
      interval: weekly
  - package-ecosystem: npm
    directory: /web
    schedule:
      interval: weekly
```

## Owner and process

The file is the evidence that updates happen. The owner is whoever reviews the
pull requests. In a single-maintainer repository that is the maintainer, and one
sentence in the contributing guide saying updates arrive weekly and are merged
after CI passes is the process.
