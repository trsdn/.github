# CodeQL: default setup or an advanced workflow

Serves [`P13`](../repository-quality-standard.md#p13): code scanning covers the
repository's languages where CodeQL supports one.

## The rule that causes most failures

A repository can have CodeQL default setup or an advanced workflow file, not
both. While default setup is on, GitHub rejects the results an advanced workflow
uploads, and the workflow run fails. Choosing an advanced workflow therefore
starts with switching default setup off.

## Which to use

Default setup needs nothing in the repository. Turn it on in the repository's
code security settings. It is enough for most repositories.

| Situation | Use |
|---|---|
| Python, JavaScript or TypeScript, GitHub Actions, or another language that CodeQL analyses without a build | Default setup |
| Swift, or C# and Java where CodeQL can analyse without a build | Default setup, if a run succeeds |
| A compiled language that needs a real build with a specific SDK or runner | An advanced workflow |
| Extra queries such as `security-extended`, or a config file that excludes paths | An advanced workflow |
| A runner that is not the default, such as `windows-latest` for `net*-windows` projects | An advanced workflow |

Default setup is not a lesser option. Twelve of the account's repositories use
it successfully, Swift ones included. Reach for a workflow when you need
something default setup cannot express, not to be thorough.

## Which languages count

List every language in the repository that CodeQL supports, not only the main
one. A repository with TypeScript and C# lists both. Check GitHub's current list
of supported languages before deciding a language is not covered, because the
list has changed over time and this page does not repeat it. A language with no
CodeQL support, such as shell scripts, is not a gap.

Default setup reports the languages it detected in the `languages` field of
`gh api repos/OWNER/REPO/code-scanning/default-setup`. That is what it found, not
proof that each was analysed. Read `state` as well.

## Switching default setup off

This is a repository settings change, so a maintainer does it:

```sh
gh api -X PATCH repos/OWNER/REPO/code-scanning/default-setup -F state=not-configured
```

Do it before, or in the same change as, merging the workflow file. Confirm with
`gh api repos/OWNER/REPO/code-scanning/default-setup --jq .state`, which should
print `not-configured`.

## Advanced workflow, no build

For languages that need no build, call the shared workflow. Its caller is in the
[Python](../../templates/python/.github/workflows/codeql.yml) and
[Node](../../templates/node/.github/workflows/codeql.yml) kits. The caller grants
`security-events: write`, because a called workflow cannot hold more permission
than its caller gives it.

## Advanced workflow, C# with a build

A worked example is the [.NET kit workflow](../../templates/dotnet/.github/workflows/codeql.yml).
The decisions in it:

- **Build mode.** `none` analyses without building and works on any runner.
  `manual` runs your restore and build steps between `init` and `analyze` and
  gives the fullest results. `autobuild` lets CodeQL guess. Use `manual` when
  `none` misses code or the solution needs a particular SDK.
- **Runner.** Projects targeting `net*-windows` restore and build only on
  Windows, so the job runs on `windows-latest`.
- **Paths filter.** There is none on `pull_request`. A required check that is
  skipped by a paths filter never reports, and the pull request waits forever.
- **Category.** `/language:csharp` keeps results from different languages
  apart.
- **Extra queries.** `queries: +security-extended` adds to the default set.

To cover a second language, add it to the matrix. The kit shows how the manual
build steps are skipped for a language that needs none.

## Worked example

A repository holds a C# solution and a TypeScript extension. Default setup is
on. Steps: switch it off with the command above, copy the .NET kit workflow,
change the matrix to `[csharp, javascript-typescript]`, set the solution name,
and open a pull request. The two jobs upload under separate categories, and the
`P13` result is `pass` for both languages.
