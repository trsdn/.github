---
applyTo: ".github/**,.swiftlint.yml,AGENTS.md,AGENTS.macos.md"
---

<!-- markdownlint-disable MD041 -->

# Tuning a copied kit

The `trsdn/.github` kits under `templates/` are deliberately generic; two
marker conventions mark what a specific repository has to decide:

- `TODO(name)`, used by the macOS app kit.
- A trailing `# EDIT: ...` comment, used by the Python, Node, and .NET kits.

Resolve every one with a value verified against this repository, following the
priority order below.

## 1. Read the manifest before anything else

- Swift: `Package.swift`'s `platforms:` array gives the minimum OS version;
  its targets give the source and test directories.
- Node: `package.json`'s `engines` field, or a `.nvmrc`, gives the runtime
  version; its `scripts` give the real lint, build, and test commands.
- Python: `pyproject.toml`'s `requires-python` gives the version range; its
  build backend and existing `noxfile.py`/`tox.ini`, if any, give the real
  commands.
- .NET: the `.csproj` or `.sln`'s `TargetFramework`(s) give the runtime
  version and the project or solution file name the build commands need.

A kit's placeholder version (for example .NET's `9.0.x`) is a plausible
example, not a default to keep — replace it with what the manifest states even
when it happens to match.

## 2. Prefer an existing command over inventing one

If the repository already has a working build, test, or lint command
documented in its README or `AGENTS.md`, or defined in `package.json` scripts
or similar, use that instead of the kit's suggested one. The kit's command is
a fallback for a repository that has none yet.

## 3. Tune lint rule sets by running them, not by reading them

Run the exact lint command the kit configures, with the kit's starter rule
set, against the repository as it stands. For every rule that reports a
violation: drop it from the config, in this same pass, unless you are also
fixing the violation in this same pass. This is the ratchet principle the
kits already document — every remaining rule must be true today. Check the
installed tool's current rule names (`swiftlint rules`, `eslint --print-config`,
or the equivalent) rather than assuming the kit's file matches the version
installed; a renamed or removed rule silently does nothing instead of failing
loudly, which is worse than an error.

## 4. Ecosystem and language markers

For Dependabot: keep an ecosystem entry only where a manifest for it exists in
the repository (a `Package.swift` for `swift`, a `package.json` for `npm`, and
so on); remove the rest. Set a directory value only to a path that actually
holds the manifest.

For CodeQL: list only the languages the repository actually contains, and only
add the advanced (build-mode) workflow where the default setup genuinely
cannot analyse the language without a build — see
`docs/guides/codeql.md` in the `trsdn/.github` checkout for exactly when that
is true. Never enable both the default setup and an advanced workflow for the
same repository; that is the caller's decision, made once, not something this
pass should silently duplicate.

## 5. When you cannot verify a value

Leave the marker in place, with a comment stating what you tried and why it
did not resolve (a scheme you could not find, a grouping decision that needs
the maintainer's judgement about what belongs together). A marker left in
place with an honest note is correct; a marker replaced with a value nobody
checked is not, even if it happens to be right.

## What is out of scope

Do not refactor code, do not change what the repository's own tests assert,
and do not touch files the kit did not copy in this adoption pass. This is
tuning a template to fit, not a general review of the repository.
