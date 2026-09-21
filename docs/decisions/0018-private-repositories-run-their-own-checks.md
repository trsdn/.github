# 0018 - Private repositories run their own checks

- Status: Accepted
- Date: 2026-09-21

## Context

The standard was written around public repositories, where GitHub supplies secret
scanning, code scanning, Dependabot and hosted runners for free. The account also
holds 81 private repositories, and measuring them showed none of that: no secret
scanning, no code scanning, no rulesets, and no Actions minutes to spend. The
standard said little about them beyond "the Public profile does not apply".

A first proposal was to ask every repository, private ones included, for Dependabot
alerts and security updates. That was wrong for this account, because Dependabot
runs on the minutes a private repository does not have, and the account's
allowance is used up at once.

## Decision

State what a private repository can and cannot have, and say for every criterion
whether it applies, is not applicable, or is met another way, in one table. Record
the account's capabilities once in a document that each private repository's record
cites, instead of every record arguing its own case.

Ask for the release-time checks the repository can run itself. `R09` asks that a
secret scan and a dependency check have passed for the release commit, by a
workflow or by a local step with a recorded result, and publish a script that runs
both with tools that need no GitHub feature. Move `S05` to the row of checks the
repository owns, so a documented local scan is a `Pass` without a runner.

Keep Dependabot off in private repositories that cannot afford it, and keep `P12`
and `P13` public-only.

## Consequences

- A private repository can meet nearly the whole standard with local commands, at
  the cost of running them, which an agent doing the release can do.
- The account's capabilities are a statement to keep true. A change of plan changes
  the table and, with it, results, so it is re-read when the plan changes.
- Code scanning has no equivalent for a private repository here: CodeQL is not
  offered and its command-line tool is not licensed for private code. Static
  analysers that run locally are recommended and not required.
- A private repository has no branch protection at all, so nothing but the
  repository's own rules keeps `main` from being rewritten. That is a risk the
  standard records as not applicable, and does not remove.
