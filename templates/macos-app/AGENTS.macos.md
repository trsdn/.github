<!-- markdownlint-disable MD041 -->
<!--
The macOS-specific sections for an app's AGENTS.md. Start from
../AGENTS.md, which covers the general sections, and merge these in: add the
layout rows to its Layout table, and add the other sections after its Validate
section. Replace every TODO(...) marker, delete what does not apply, and delete
this comment.

Together the two files should leave AGENTS.md satisfying the agent-instruction
criteria beginning at G01 in ../../docs/repository-quality-standard.md#g01. This
file adds what is specific to a signed, notarized macOS app: what a release
changes, which paths are generated, and which commands an agent must not run
against the machine it is on. It does not restate the criteria.
-->

## What this repository is

<!-- Replace the paragraph in the general starting point with one like this. -->

TODO(app-name) is a macOS TODO(app-kind: for example menu bar app, windowed app,
document-based app) built with TODO(build-system: Swift Package Manager or an
Xcode project) for macOS TODO(minimum-macos)+ on TODO(architectures). End users
install the signed, notarized DMG or ZIP from GitHub Releases TODO(updates:
and receive updates in place through the app itself). A bad release reaches every
installed copy, so changes to the release workflow, signing, entitlements, or
TODO(update-code-path) can strand users on an old version.

## What this repository is not

<!-- Say what an agent might assume and be wrong about. For example: -->

Not a Mac App Store app, so there is no App Store review, sandbox requirement, or
receipt validation TODO(delete-if-untrue).

## Layout

<!-- Add these rows to the Layout table. Keep the paths that exist. -->

| Path | Purpose |
|---|---|
| `Sources/TODO(app-name)/` | The app. TODO(entry-point: name the file that holds the app's state and what owns it.) |
| `Tests/TODO(app-name)Tests/` | Unit tests. State what they cover and what they do not: UI, permissions, and system integration usually are not covered. |
| `Info.plist` | Bundle identity: name, version, copyright, licence, repository and issue URLs. `Package.swift` has no fields for these, so they live here. The release build reads the version from it and the release gate compares it with the tag. |
| `TODO(app-name).entitlements` | The app's entitlements. Keep them minimal; each one is justified in this file. |
| `scripts/` | Build, sign, notarize, DMG, and release scripts. The release workflow calls them. |
| `.github/workflows/release.yml` | Builds, signs, notarizes, and publishes a release for a pushed tag. |
| `.github/workflows/smoke-test.yml` | Installs the published DMG and checks it as a consumer receives it. |

## Generated, vendored, and machine-owned paths

Anything not listed here is hand-maintained.

- Generated, never hand-edit: `.build/` (SwiftPM output and the built `.app`),
  `dist/` (release output), `*.dmg` and `*.dmg.sha256`. All are git-ignored.
  Regenerate with `swift build -c release` or the release scripts.
- Machine-owned: `Package.resolved`. Change it only by updating `Package.swift`
  or by merging a Dependabot pull request.
- TODO(project-file): if the Xcode project is generated from a manifest, list the
  generated project and the command that regenerates it.

## Signing and notarization

- Every build that leaves the machine is signed with a Developer ID Application
  certificate and notarized, and the ticket is stapled. The build script exits
  with an error when no identity is available and creates no certificate.
- Never ad-hoc sign. macOS treats an ad-hoc signed app as a different app on
  every build and resets its permissions.
- Notarize the app and stapled ZIP first, build the DMG from the stapled app, then
  notarize the DMG separately.
- The hardened runtime is on. An entitlement is added only with a reason written
  next to it here, in a pull request the maintainer approves.
- Signing credentials exist only as GitHub Actions secrets and in the
  maintainer's keychain. They are never in the tree, never printed, and never
  passed on a command line that a log would echo. See Credentials and revocation.
- A local build for development uses a development certificate from the local
  keychain. It is never uploaded anywhere.

## In-app updates

<!-- Keep this section if the app updates itself. Delete it otherwise. -->

TODO(app-name) is distributed outside the Mac App Store. TODO(updater: name the
library or mechanism) checks GitHub Releases for a newer signed DMG and installs
it in place.

- Asset naming: TODO(asset-names: the exact names the updater looks for, and the
  release step that creates them). Renaming an asset breaks every installed
  copy's update check.
- Verification: TODO(what the updater verifies about the download, for example
  the signing identity, Team ID, and bundle identifier).
- TODO(constraints: anything an agent must not re-enable or change because it has
  broken a release before, with the issue number.)
- The updater quiesces the app before installing, so a swap and relaunch cannot
  interrupt work in progress.

## Validate before proposing a change

These commands must all succeed, and CI runs them on every pull request:

```sh
swift build -c release -Xswiftc -warnings-as-errors
swiftlint lint --strict
swift test
```

The build type-checks the whole package under Swift strict concurrency with
warnings as errors and links the executable. `swiftlint lint --strict` runs the
small rule set in `.swiftlint.yml`, which passes today, so any violation is a
regression. `swift test` runs the unit tests. TODO(coverage-limits): say what the
tests do not cover, such as audio, hotkeys, paste, overlays, permissions, or
updates. For a change to those areas, also run the built app and check the
affected flow by hand, and say in the pull request what you tried.

## Conventions

- Release identity comes from `Info.plist` (`CFBundleShortVersionString` and
  `CFBundleVersion`). Bump both in a release change before tagging.
- User-facing changes get an entry in `CHANGELOG.md`. The release workflow
  publishes that entry as the release notes and fails when it is missing or empty,
  when entries are still held under an unreleased heading, or when `Info.plist`
  disagrees with the tag.
- Log with `os.Logger`. Never log user content, credentials, prompts, or tokens.
- TODO(other-conventions): where state lives, which actor owns it, and where
  blocking work runs, if an agent could otherwise get them wrong.

## Do not do these

<!-- Add these to the general list of forbidden operations. -->

- Do not publish a release, create or move tags, dispatch the release workflow,
  or change repository settings. The maintainer (TODO(maintainer-handle)) does
  this. Pushing a version tag starts a signed, notarized release that reaches
  users.
- Do not edit `.github/workflows/release.yml`, the signing and notarization
  scripts, `Info.plist` version keys, or entitlements without a pull request the
  maintainer approves.
- Do not sign with an ad-hoc identity, disable the hardened runtime, or skip
  notarization to make a build pass.
- Do not commit certificates, `.p12` files, keychains, provisioning material,
  notary profiles, or `.release.env`. Commit only the `.release.env.example`
  template.
- Do not run destructive commands against the machine you are on: no
  `defaults delete` for the app's domain, no removal of `~/Library` state, no
  `tccutil reset`, no `security delete-keychain` outside `.build/`.
- Do not hand-edit the generated paths listed above.
- Do not add or upgrade dependencies without a pull request the maintainer
  approves. Dependabot proposes routine updates weekly.
- TODO(product-specific): add a line for anything specific that has broken users
  before.

## Credentials and revocation

Release credentials are held as GitHub Actions secrets and are never in the tree.
If one is exposed, revoke it at its source first, then update the secret.

| Credential | Where it lives | If exposed |
|---|---|---|
| `MACOS_CERTIFICATE`, `MACOS_CERTIFICATE_PWD` (Developer ID Application `.p12`, base64 encoded, and its password) | Actions secrets | Revoke the certificate in the Apple Developer portal, issue a new one, re-export the `.p12`, update both secrets. Maintainer only. |
| `APPLE_ID`, `APPLE_APP_PASSWORD` | Actions secrets | Revoke the app-specific password at appleid.apple.com, create a new one, update `APPLE_APP_PASSWORD`. Maintainer only. |
| `APPLE_TEAM_ID` | Actions secret | An identifier, not a credential. Nothing to revoke. |
| Local notary profile (`xcrun notarytool store-credentials`) | The maintainer's login keychain | Revoke the app-specific password as above and store the profile again. |
| TODO(user-credentials: for example provider API keys the user enters) | The user's macOS Keychain | The user revokes it with the provider. The repository holds none. Delete the row if there are none. |
