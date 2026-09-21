# Reusable Workflows

This repository publishes three reusable GitHub Actions workflows in
`.github/workflows/`. A repository that calls one has no copy of it to drift.
[S12](../repository-quality-standard.md#s12) permits referencing a workflow from
the same account by branch, so the examples below use `@main`. Permissions in the
callers follow [S11](../repository-quality-standard.md#s11).

A caller decides the triggers, including any schedule. A called workflow cannot
be granted more token permission than its caller declares, so the caller's job
must list the permissions shown.

## Secret scan

`secret-scan.yml` scans the repository history with gitleaks. It needs no secret
beyond the default token. The gitleaks action comes from outside the account and
is pinned by commit SHA, which
[S12](../repository-quality-standard.md#s12) asks for in a job like this.

```yaml
name: Secret scan
on:
  push:
    branches: [main]
  pull_request:
permissions:
  contents: read
jobs:
  scan:
    permissions:
      contents: read
    uses: trsdn/.github/.github/workflows/secret-scan.yml@main
```

| Input | Type | Default | Meaning |
|---|---|---|---|
| `runner` | string | `ubuntu-latest` | Runner label. |
| `fetch-depth` | number | `0` | Commits fetched; `0` scans all history. |

What to change: delete a repository's own copy of a secret-scan workflow when
adopting this one. Rules specific to a repository go in its `.gitleaks.toml`.

## CodeQL for languages without a build

`codeql.yml` runs CodeQL with build mode `none`, which covers `python`,
`javascript-typescript`, `actions` and other languages that need no build. It
runs one job per language.

Do not use it together with GitHub's default setup for the same repository. Both
would analyze the same languages, and default setup rejects results uploaded by
an advanced workflow. Turn default setup off first, then add the caller. This
repository stays on default setup, so it does not call this workflow.

```yaml
name: CodeQL
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: "41 3 * * 1"
permissions:
  contents: read
jobs:
  analyze:
    permissions:
      contents: read
      actions: read
      security-events: write
    uses: trsdn/.github/.github/workflows/codeql.yml@main
    with:
      languages: '["actions","python"]'
```

| Input | Type | Default | Meaning |
|---|---|---|---|
| `languages` | string | `["actions","python"]` | JSON array of languages. |
| `runner` | string | `ubuntu-latest` | Runner label. |
| `timeout-minutes` | number | `30` | Limit for each language job. |

What to change: set `languages` to what the repository contains. Remove a CodeQL
workflow that lists a language needing no build only to run an autobuild.

## CodeQL for Swift

`codeql-swift.yml` builds a Swift package with an explicit command and analyzes
it. It can also analyze `actions` and `python` without a build. The build is
explicit because default setup's autobuild failed on the package this was taken
from, and an explicit command analyzes what CI builds. The same rule about
default setup applies: turn it off before adding the caller.

```yaml
name: CodeQL
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
    paths:
      - Sources/**
      - Tests/**
      - Package.swift
      - .github/workflows/**
  schedule:
    - cron: "41 3 * * 1"
permissions:
  contents: read
jobs:
  analyze:
    permissions:
      contents: read
      actions: read
      security-events: write
    uses: trsdn/.github/.github/workflows/codeql-swift.yml@main
```

| Input | Type | Default | Meaning |
|---|---|---|---|
| `build-command` | string | `swift build -c release -Xswiftc -warnings-as-errors` | Command run before analysis. |
| `runner` | string | `macos-latest` | Runner label; Swift needs macOS. |
| `analyze-actions` | boolean | `true` | Also analyze workflows. |
| `analyze-python` | boolean | `true` | Also analyze Python. |
| `timeout-minutes` | number | `60` | Limit for each language job. |

What to change: set `build-command` to the command CI uses, and turn off the
languages the repository does not contain. Limit the `pull_request` paths as
shown, because the Swift build is slow.

## Branch reference or template

| Situation | Use |
|---|---|
| The file is the same in every repository and a fix should reach all of them | Reference the reusable workflow by branch |
| The repository needs steps the inputs cannot express | Copy a template and own it |
| A change must not reach a repository until it has been tested there | Reference a release tag, or copy |
| The caller is outside the account | Copy; an outside account can change what a branch reference runs, which [S12](../repository-quality-standard.md#s12) does not permit |

## Changing a reusable workflow

A change to one of these files reaches every caller on its next run. To keep that
safe:

- Add inputs with defaults that keep the old behavior. Do not rename or remove an
  input, or change a default, in place.
- Keep the permissions a caller must declare unchanged. Adding one breaks every
  caller until it is edited.
- For a breaking change, publish a new file name or a tag, and move callers over
  one at a time.
- Let the pull request test the change. This repository calls `secret-scan.yml`
  from `.github/workflows/secret-scan-self.yml` by relative path, so the version
  under review is the one that runs.
