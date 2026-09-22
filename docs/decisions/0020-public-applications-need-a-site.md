# 0020 - Public applications need a site

- Status: Accepted
- Date: 2026-09-22

## Context

[1.20.0](../../CHANGELOG.md) narrowed the Published Site profile to repositories
that already publish a website, after two pilots read the earlier wording
differently: one treated a public application with no site as owing one, the
other treated it as `Not applicable`. The fix removed the disagreement by
removing the obligation, so a public application never needed a site at all.

That went further than intended. The maintainer wants every public application to
have a site: an installable product should be findable and presentable outside
GitHub, on the same reasoning `P07` already applies to discovery metadata. The
actual defect was that the trigger gave an assessor no test to apply
consistently, not that the obligation was wrong.

## Decision

Restore the obligation, with the test the two pilots lacked. The Published Site
profile applies to a public repository that ships a product a non-developer
installs or runs by name — an application, a game, a command-line tool used
directly — regardless of the platform, and regardless of whether a site exists
yet. It excludes a library, an MCP server or agent tool that other software or a
developer configures rather than installs by name, and any product a private
repository ships, because nobody outside the account could reach a site for it.

A public repository that matches the trigger and has no site records `W01`-`W09`
at their ordinary results, which is `Fail` for most of them, rather than `Not
applicable`. Building the site is the remediation.

## Consequences

- A public application repository with no site now fails several criteria it
  passed as `Not applicable` under 1.20.0. That is the intended effect: existing
  records for such repositories are due for reassessment, and some will need a
  site before they reassess `Healthy`.
- The MCP-server and library exclusion is a judgement call an assessor makes once
  per repository, not a fact read from a setting. Two repositories that look
  alike may be assessed differently if their actual audience differs, and the
  assessor's reading is recorded.
- Private application repositories keep no obligation to publish anything, which
  matches the private repositories rules.
