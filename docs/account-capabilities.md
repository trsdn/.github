# Account capabilities

What GitHub provides to a repository depends on the account's plan, and the
[private repositories rules](repository-quality-standard.md#private-repositories)
turn on it. This is the statement for the `trsdn` account. A private repository's
conformance record cites it in place of restating it, so the answer lives once.

Read on 2026-09-21. Re-read it when the plan changes or a result looks wrong; the
commands are below.

## Private repositories

| Capability | State | How it was read |
|---|---|---|
| Hosted Actions minutes | Not available: the allowance is used up at once, so a private repository is without automation | Stated by the maintainer. `gh api repos/OWNER/REPO/actions/permissions` says Actions is enabled and does not report the budget |
| GitHub secret scanning and push protection | Not offered | `security_and_analysis` is empty: `gh api repos/OWNER/REPO --jq .security_and_analysis` |
| Code scanning, including CodeQL | Not offered | `gh api repos/OWNER/REPO/code-scanning/default-setup` answers `403` |
| Rulesets and branch protection | Not offered | `gh api repos/OWNER/REPO/rulesets` answers `403` |
| Dependabot alerts and security updates | Switched off on purpose by the maintainer, because Dependabot jobs count against Actions minutes in a private repository (check GitHub's current billing documentation) | `gh api -i repos/OWNER/REPO/vulnerability-alerts` answers `404` |
| Private vulnerability reporting | Not applicable to a private repository | `gh api repos/OWNER/REPO/private-vulnerability-reporting` answers `404` |

The same facts held for all 81 active private, non-fork repositories in the
account when this was read.

## Public repositories

Every one of these is free for a public repository and is enabled on every active,
non-fork public repository in the account. See
[Repository security settings](guides/repository-security-settings.md).

## What follows

A private repository records the absence of each capability above once, in one
sentence that links here, as the standard requires. It then meets the criteria the
capability would have met by running the check itself. The
[private repositories guide](guides/private-repositories.md) says how.
