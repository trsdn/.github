# Bringing a macOS app to the standard

This guide takes a macOS app repository that is new, or behind, to a state where
the [Repository Quality Standard](../repository-quality-standard.md) can be
assessed against it. It uses the files in
[`templates/macos-app/`](../../templates/macos-app/), whose
[README](../../templates/macos-app/README.md) lists each file and the criteria it
gives evidence for. The guide adds the order and the reasons. It does not restate
the criteria; follow the links for what each one asks.

It assumes a Swift app built with Swift Package Manager and distributed as a
signed, notarized DMG from GitHub Releases. Xcode-project apps follow the same
order, and the templates say where they differ.

## 1. Write the agent instructions first

Start with `AGENTS.md`, because every later step needs a validation command an
agent can run. Copy [`templates/AGENTS.md`](../../templates/AGENTS.md) and merge
in [`AGENTS.macos.md`](../../templates/macos-app/AGENTS.macos.md), which holds the
macOS-specific sections: the layout rows, the rules for signing and
notarization, the release and tag prohibitions, and the in-app update notes. The
criteria this serves start at [G01](../repository-quality-standard.md#g01); the
ones that most often fail for a macOS app are
[G03](../repository-quality-standard.md#g03), because the release and
destructive-command prohibitions are missing, and
[G06](../repository-quality-standard.md#g06), because the generated build output
is not marked.

Fill in the validation commands from what actually passes today. A command listed
here that fails on a clean checkout is worse than none.

## 2. Add CI, linting, and dependency updates

Copy `ci.yml`, `.swiftlint.yml`, and `dependabot.yml` from the kit. CI builds in
release mode with warnings as errors, runs the linter, and runs the tests. See
[S02](../repository-quality-standard.md#s02),
[S03](../repository-quality-standard.md#s03) and
[S08](../repository-quality-standard.md#s08).

The lint file is a ratchet. Its rule set is deliberately small, and every rule in
it passes on the whole codebase today, so a violation means something got worse.
Run the linter against the file, delete any rule that reports a violation you are
not fixing in the same change, and add rules back only as the code earns them. Do
not start with a large rule set and a backlog of exceptions.

Open a pull request with just these files and get it green before going on. The
runner matrix in `ci.yml` builds on an older macOS image and on the latest one,
because a newer SDK can hide errors an older one reports.

## 3. Add the secret scan and the first conformance record

Copy `secret-scan.yml`, which calls the shared workflow
([S05](../repository-quality-standard.md#s05)). Then create the conformance
record, which is the repository's dated statement of what it meets.

Generate it rather than typing it. The commands and the file format are in
[Conformance Record Format](../conformance-record.md#starting-a-record), and
[Drafting a conformance record](../assessing.md) describes a script that drafts
one from what the GitHub API shows. Either way the result needs an assessor to
read each criterion against the repository and set a result with a note. Do not
mark a criterion as met because the kit contains a file for it; the file has to
exist in the repository, be filled in, and have run. Then copy `conformance.yml`,
which checks the record and the committed badge on every change
([B11](../repository-quality-standard.md#b11)).

A first record with several failing criteria is the normal result and is the
point. It lists what the remaining steps of this guide fix.

## 4. Turn on code scanning

Criterion [P13](../repository-quality-standard.md#p13) asks that code scanning
cover the repository's languages, and CodeQL supports Swift. There are two ways to
get it, and they cannot both be enabled at once.

**Try default setup first.** Under Settings, Code security, Code scanning,
enable CodeQL default setup. GitHub builds and analyses Swift on a macOS runner
with no file in the repository. It handles most Swift packages, package-only apps
included, so it is the ordinary case.

**Switch to an advanced workflow only when default setup fails.** OpenWritr is the
one that needed it: GitHub's Swift autobuild failed on that package, so the
default setup was turned off and an advanced workflow was written that builds
with the same command as CI. If the default setup's run reports that autobuild
failed, or the analysis comes back with no Swift files, do this:

1. Turn default setup off. Leave it on and the advanced workflow's results are
   rejected or duplicated.
2. Copy [`codeql.yml`](../../templates/macos-app/.github/workflows/codeql.yml).
   It calls the shared Swift workflow on `macos-latest` with a manual build, so
   CodeQL traces exactly the build that ships. Swift analysis needs a macOS
   runner; there is no Linux option.
3. Set the build command to the one in `ci.yml`. An app whose project is
   generated, or that is an Xcode project, needs the generation step first, which
   the autobuild cannot do for it. Such apps should expect to need the advanced
   workflow.

The Swift analysis builds the whole app and can take half an hour, so the
template runs it on pull requests only when source paths change, and always on
pushes to the default branch and weekly. Remove the `paths` filter if a ruleset
requires the check, because a required check that a filter skips never reports. Expect the first advanced runs to
fail while the build command is tuned, and look at the analyses the API reports
before treating scanning as working.

## 5. The Apple HIG review

This step is optional and no criterion asks for it. It adds a read-only review of
the app's UI changes, and of its rendered screens where the app can draw them,
against Apple's Human Interface Guidelines. It runs locally, on request, before a
merge or a release: a workflow for it would need a macOS runner, an agent token and
a compile step, which costs more than the review is worth.

The agent, its rules and the request are published as a versioned package, so the
app declares a version in its `apm.yml` and updates by changing it. Install and run
it as [the package README](../../packages/apple-hig-review/README.md) describes,
including the `targets` that `apm.yml` needs.
The app itself only needs to say in its `AGENTS.md` what kind of app it is, what
user data it handles, and, if it has one, the command that renders its screens.

## 6. The release pipeline

Add the release pieces together, because each one depends on the others:
[`release.yml`](../../templates/macos-app/.github/workflows/release.yml),
[`smoke-test.yml`](../../templates/macos-app/.github/workflows/smoke-test.yml),
and [`release-smoke-tests.md`](../../templates/macos-app/docs/release-smoke-tests.md).

The pipeline gates before it builds: the tag must be a version, the app's
`Info.plist` must agree with it, and the changelog must have a non-empty entry for
it. Those are [R04](../repository-quality-standard.md#r04) and
[R07](../repository-quality-standard.md#r07). It then imports the signing
certificate, signs, notarizes the app and the DMG, and attaches the artifacts to a
draft release whose notes are the changelog entry
([R03](../repository-quality-standard.md#r03)). It smoke-tests the draft, and only
then publishes and confirms the public download is the tested file.

The smoke test is [R05](../repository-quality-standard.md#r05). It installs the
DMG the way a consumer would, checks the signature, the Gatekeeper assessment, and
the notarization ticket, and runs the app's non-interactive entry point when it
has one. A menu bar or window app that cannot start unattended still has the
signature and launch-policy check, and the record in `release-smoke-tests.md`
should say that is the whole kit and what it does not cover. Adding a
`--self-test` style entry point to the app makes the kit much stronger and is
worth the work.

What you write yourself: the build, notarize, and DMG scripts that the workflow
calls. Their contract is at the top of `release.yml`. Then create the secrets the
[kit README](../../templates/macos-app/README.md#secrets) lists, each with how it
is revoked. Set them as repository secrets and never paste a value into a file,
an issue, or a pull request.

Run the pipeline once for a low-risk version before the first real release, and
read the whole run. Only a completed run shows that the draft, smoke test, and
publish order works, and the record of that run is what
[R05](../repository-quality-standard.md#r05) asks for.

## 7. Reassess

When the steps above are in place, reassess the repository against the standard,
update the conformance record with what changed, and let the check confirm the
badge. An assessment that lags the repository turns the conformance check red on
schedule, which is intended; only a new assessment clears it.
