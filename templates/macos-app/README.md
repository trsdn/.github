# macOS app starter kit

Files to copy into a macOS app repository that is new to the Repository Quality
Standard, or that lags behind it. Every file is a copy-and-edit starting point:
the values that differ per repository are marked `TODO(name)`, and a comment at
the top of the file says what to change. Search for `TODO(` after copying, and
do not commit while any remain.

The kit assumes a Swift Package Manager app that is signed, notarized, and
distributed outside the Mac App Store as a DMG and ZIP from GitHub Releases. Where
an Xcode project or a different distribution changes a file, the file says so.

The guide [Bringing a macOS app to the standard](../../docs/guides/macos-app.md)
walks through the same steps with the reasons.

## What is in the kit

Each row names the criteria the file provides evidence for. The criteria are
defined in [the standard](../../docs/repository-quality-standard.md); this table
only points at them.

| File | Copy to | Provides evidence for |
|---|---|---|
| [`AGENTS.macos.md`](AGENTS.macos.md) | Merged into `AGENTS.md`, beside [the general starting point](../AGENTS.md) | [G02](../../docs/repository-quality-standard.md#g02), [G03](../../docs/repository-quality-standard.md#g03), [G06](../../docs/repository-quality-standard.md#g06) |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | `.github/workflows/ci.yml` | [B05](../../docs/repository-quality-standard.md#b05), [S02](../../docs/repository-quality-standard.md#s02), [S03](../../docs/repository-quality-standard.md#s03), [S04](../../docs/repository-quality-standard.md#s04), [S11](../../docs/repository-quality-standard.md#s11) |
| [`.swiftlint.yml`](.swiftlint.yml) | `.swiftlint.yml` | [S03](../../docs/repository-quality-standard.md#s03) |
| [`.github/dependabot.yml`](.github/dependabot.yml) | `.github/dependabot.yml` | [S08](../../docs/repository-quality-standard.md#s08), [S12](../../docs/repository-quality-standard.md#s12) |
| [`.github/workflows/secret-scan.yml`](.github/workflows/secret-scan.yml) | `.github/workflows/secret-scan.yml` | [S05](../../docs/repository-quality-standard.md#s05), [S11](../../docs/repository-quality-standard.md#s11) |
| [`.github/workflows/conformance.yml`](.github/workflows/conformance.yml) | `.github/workflows/conformance.yml` | [B11](../../docs/repository-quality-standard.md#b11), [P08](../../docs/repository-quality-standard.md#p08) |
| [`.github/workflows/codeql.yml`](.github/workflows/codeql.yml) | `.github/workflows/codeql.yml`, only if default setup fails | [P13](../../docs/repository-quality-standard.md#p13) |
| [`.github/workflows/smoke-test.yml`](.github/workflows/smoke-test.yml), [`docs/release-smoke-tests.md`](docs/release-smoke-tests.md) | Same paths | [R05](../../docs/repository-quality-standard.md#r05) |
| [`.github/workflows/release.yml`](.github/workflows/release.yml) | `.github/workflows/release.yml` | [R03](../../docs/repository-quality-standard.md#r03), [R04](../../docs/repository-quality-standard.md#r04), [R07](../../docs/repository-quality-standard.md#r07), with the smoke test [R05](../../docs/repository-quality-standard.md#r05) |
| The [Apple HIG review package](../../packages/apple-hig-review/README.md) | Declared in `apm.yml`, see [the Apple HIG review](#the-apple-hig-review) | Optional. No criterion asks for it |

Every workflow declares `permissions` and pins what it runs. Actions published by
GitHub use a major-version tag. The shared workflows are called at `@main`.

What the kit does not provide: the build, sign, notarize, and DMG scripts that
`release.yml` calls, which differ for every app (the contract they must meet is at
the top of `release.yml`); the app's own `--self-test` style entry point;
provenance for the published artifact, which [R08](../../docs/repository-quality-standard.md#r08)
asks about; and the issue and pull-request templates, which the repository
inherits.

## Order of adoption

1. Write `AGENTS.md` from [`../AGENTS.md`](../AGENTS.md) and merge in
   [`AGENTS.macos.md`](AGENTS.macos.md). Fill in the validation commands honestly
   first; the later steps depend on them.
2. Add `ci.yml`, `.swiftlint.yml`, and `dependabot.yml`. Get CI green on a pull
   request before adding anything else.
3. Add `secret-scan.yml`. Then create the conformance record from
   [`../conformance.yml`](../conformance.yml) and add `conformance.yml`.
4. Turn on code scanning. Try GitHub's default setup first. Add `codeql.yml` only
   if the default setup's Swift analysis fails.
5. Add the release pieces together: `release.yml`, `smoke-test.yml`, and
   `docs/release-smoke-tests.md`, then write the scripts `release.yml` calls, then
   the secrets below. Release a version to prove the whole path.
6. Optionally add the Apple HIG review, which runs locally.

## Secrets

Values never appear in any file. A secret is created under Settings, Secrets and
variables, Actions. If one is exposed, revoke it at its source first, then update
the secret.

| Secret | What it is | How it is revoked |
|---|---|---|
| `MACOS_CERTIFICATE` | The Developer ID Application certificate with its private key, exported as a `.p12` and base64 encoded | Revoke the certificate in the Apple Developer portal, issue a new one, export it again, and update this secret and `MACOS_CERTIFICATE_PWD` |
| `MACOS_CERTIFICATE_PWD` | The password set when the `.p12` was exported | Set with the new export; revoking the certificate makes the old one useless |
| `APPLE_ID` | The Apple ID that submits the app for notarization | An identifier. Change the secret if the account changes |
| `APPLE_TEAM_ID` | The ten-character Apple Developer Team ID | An identifier, not a credential. Nothing to revoke |
| `APPLE_APP_PASSWORD` | An app-specific password for that Apple ID, used by `notarytool` | Revoke it at appleid.apple.com, create a new one, and update this secret |

The workflows read these by name in `release.yml`. The
default `GITHUB_TOKEN` needs no setup.

A repository variable, not a secret, `ENABLE_PRIVATE_SECRET_SCAN`, turns the secret
scan on in a private repository. `secret-scan.yml` explains it.

## Checks to make after copying

- The shared workflows this kit calls, `secret-scan.yml`, `codeql-swift.yml`, and
  `conformance.yml` in `trsdn/.github`, define their own inputs. Read the
  `workflow_call` section of each and make the `with:` block in the caller match.
- A job that calls a shared workflow is reported to branch rules as `<job> /
  <inner job>`. After the first run, read the check names on a pull request, then
  require those exact names in the branch ruleset.
- `release.yml` cannot be tried without a real tag. Run it once for a
  pre-release-shaped version such as `v0.1.0` in a repository where publishing is
  harmless, and read the run before the first real release.

## The Apple HIG review

An optional, local review. A read-only agent checks the UI changes of the app, and
its rendered screens if the app can draw them, against Apple's Human Interface
Guidelines. It runs on your machine when you ask your agent runtime to, before a
merge or a release. It is not a workflow, because a workflow for it needs a
macOS runner, an agent token and a compile step, and costs more than the review is
worth.

It is published as a versioned package, so a repository declares a version and
updates by changing it. See
[the package](../../packages/apple-hig-review/README.md) for how to install and run
it. What an app provides is small: its own `AGENTS.md` says what kind of app it is
and what user data it handles, and, if it has one, the command that renders its
screens.

