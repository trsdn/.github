# Private repositories

A private repository meets the same standard as a public one, minus the Public
profile. What it lacks is what GitHub provides for free to a public repository:
[the account's statement](../account-capabilities.md) lists what is missing. This
guide is what to do instead, with tools that need no GitHub feature and no hosted
minutes. The
[rules](../repository-quality-standard.md#private-repositories) say which criteria
apply; this says how to meet them.

## What to do instead

| Missing | Instead | Criteria |
|---|---|---|
| A CI run for tests and lint | Run the one documented validation command locally before merging and before a release, and record the dated result | [`S02`](../repository-quality-standard.md#s02), [`S03`](../repository-quality-standard.md#s03), [`B05`](../repository-quality-standard.md#b05) |
| Secret scanning | `gitleaks`, run by the [local gate](../../templates/local-gate/README.md) over the tree and the history | [`S05`](../repository-quality-standard.md#s05), [`R09`](../repository-quality-standard.md#r09) |
| Dependabot | `osv-scanner`, or `npm audit` and `pip-audit`, run by the same gate, and one sentence naming the owner and the process | [`S08`](../repository-quality-standard.md#s08), [`R09`](../repository-quality-standard.md#r09) |
| CodeQL | See below | none: static checks belong to [`S03`](../repository-quality-standard.md#s03) |
| Rulesets | Nothing. Record the absence in one sentence | [`B16`](../repository-quality-standard.md#b16), [`S09`](../repository-quality-standard.md#s09) |

## Code scanning without GitHub's

CodeQL is not offered for a private repository on this plan, and the CodeQL
command-line tool is licensed for open-source and academic use (check GitHub's
current CodeQL terms), so running it yourself on private code is not an option. What is: a static analyser that runs
locally and needs no account.

| Language | Local analyser | Note |
|---|---|---|
| Any | `semgrep scan --config auto --metrics off` | Open-source rules; the first run downloads them |
| Python | `bandit -r .` | Finds common security mistakes |
| Swift | `swiftlint` with the repository's rule set | Style and some safety rules; the compiler with warnings as errors does the rest |
| JavaScript, TypeScript | `eslint` with `eslint-plugin-security` | |
| Go | `gosec ./...` | |
| .NET | The built-in analysers with `-warnings-as-errors` | |

None of these is asked for. They are worth running by the same documented command
as the tests, and `S03` counts them as static checks where they exist.

## The release gate

[`R09`](../repository-quality-standard.md#r09) asks that a release has passed a
secret scan and a dependency check. For a repository with no automation that is a
step of the release procedure, and its result is recorded with the release:

1. Commit everything, so the record can name the commit.
2. Run `scripts/security-gate.sh --record RELEASE_CHECKLIST.md` from the
   [local gate](../../templates/local-gate/README.md).
3. Publish only if it exits `0`. An exit of `1` means a finding to fix or to record
   a reason for, and `2` means a tool is missing and nothing was checked.

An agent doing the release does exactly the same. Add the step to the
repository's release checklist, and the record it appends is the evidence.

## Running CI without minutes

Two ways exist, and both have a cost:

- **A self-hosted runner** on your own machine has no minute budget. On a personal
  account it is registered per repository, so it does not scale to many
  repositories, and it runs code from the repository on your machine, so it should
  only ever serve private repositories you trust. Never attach one to a public
  repository, where a pull request from a fork can run code on it.
- **A local check before each merge**, by the documented command, which is what
  this guide assumes. It needs discipline rather than infrastructure.

Reusable workflows in a public repository, such as the ones in
[Reusable workflows](reusable-workflows.md), can be called from a private one. They
only help where there are minutes to run them, so a private repository without a
budget copies the script, not the workflow.

## Recording an absence

A private repository states each missing capability once, in one sentence, in the
evidence its conformance record links to, and links the
[account's statement](../account-capabilities.md). For example: "Rulesets are not
offered to this repository on the account's plan (see Account capabilities), so
`B16` and `S09` are not applicable." Without the sentence the assessor records the
ordinary result.
