# Repository security settings

The security settings the standard reads are repository settings, not files, so
nothing in a checkout shows whether they are on. This guide gives the command for
each, and the one loop that applies them to every public repository of an account.

The criteria that read them are
[`P03`](../repository-quality-standard.md#p03),
[`S05`](../repository-quality-standard.md#s05),
[`P12`](../repository-quality-standard.md#p12),
[`P13`](../repository-quality-standard.md#p13), and
[`B16`](../repository-quality-standard.md#b16). All of these settings are free for
a public repository. Changing a repository's settings needs an admin token, and a
repository's own instructions may reserve that to the maintainer, so check before
running these from an agent.

## Public repositories only

Everything below applies to a public repository. A private repository on a plan
without minutes and without GitHub's scanners turns Dependabot **off** and does
not use the scanners at all; see
[Private repositories](private-repositories.md). To switch Dependabot off:

```sh
gh api -X DELETE repos/OWNER/REPO/automated-security-fixes
gh api -X DELETE repos/OWNER/REPO/vulnerability-alerts
```

## The settings, one repository

Replace `OWNER/REPO`. The `PUT` and `PATCH` commands are safe to repeat and reversible with
`-X DELETE` or the matching `false` or `not-configured` value. The ruleset `POST`
below is not safe to repeat: it fails when the ruleset already exists.

```sh
# P03: private vulnerability reporting
gh api -X PUT repos/OWNER/REPO/private-vulnerability-reporting

# P12: Dependabot alerts, then Dependabot security updates
gh api -X PUT repos/OWNER/REPO/vulnerability-alerts
gh api -X PUT repos/OWNER/REPO/automated-security-fixes

# S05: secret scanning and push protection
gh api -X PATCH repos/OWNER/REPO --input - <<'JSON'
{"security_and_analysis": {
  "secret_scanning": {"status": "enabled"},
  "secret_scanning_push_protection": {"status": "enabled"}}}
JSON
```

Read them back with the same paths and `GET`:

```sh
gh api repos/OWNER/REPO/private-vulnerability-reporting --jq .enabled
gh api repos/OWNER/REPO/vulnerability-alerts -i | head -1        # 204 means enabled
gh api repos/OWNER/REPO/automated-security-fixes --jq .enabled
gh api repos/OWNER/REPO --jq .security_and_analysis
```

## Code scanning

Enable GitHub's default setup only for a repository that has no CodeQL workflow of
its own, because the two cannot both be on. [The CodeQL guide](codeql.md) explains
the choice and how to switch the default setup off:

```sh
gh api -X PATCH repos/OWNER/REPO/code-scanning/default-setup \
  -F state=configured -f query_suite=default
```

## The default branch

`B16` asks that the default branch cannot be force-pushed or deleted. A ruleset
does it, and does not depend on a paid plan for a public repository:

```sh
gh api -X POST repos/OWNER/REPO/rulesets --input - <<'JSON'
{"name": "protect-default-branch", "target": "branch", "enforcement": "active",
 "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
 "rules": [{"type": "deletion"}, {"type": "non_fast_forward"}]}
JSON
```

Requiring status checks, the part `S09` reads, is a further rule of type
`required_status_checks` in the same ruleset. Add it only for checks the
repository already runs.

## Every public repository of an account

```sh
for repo in $(gh repo list OWNER --limit 1000 --visibility public --no-archived \
    --json name,isFork --jq '.[] | select(.isFork | not) | .name'); do
  echo "$repo"
  gh api -X PUT "repos/OWNER/$repo/private-vulnerability-reporting" >/dev/null
  gh api -X PUT "repos/OWNER/$repo/vulnerability-alerts" >/dev/null
  gh api -X PUT "repos/OWNER/$repo/automated-security-fixes" >/dev/null
done
```

Skip forks, because their settings belong to the relationship with the upstream
repository. Do not enable the CodeQL default setup in a loop before checking each
repository for a workflow that already uses `github/codeql-action`: in a
repository that has one, the default setup makes GitHub reject the workflow's
results. Check first with
`gh api repos/OWNER/REPO/contents/.github/workflows --jq '.[].name'` and read the
files.

Two settings are deliberately not asked for: scanning for non-provider secret
patterns, which produces many false alarms, and secret validity checks, which help
little in a repository that holds few credentials.
