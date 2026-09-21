# Local gate

The two checks that [`R09`](../../docs/repository-quality-standard.md#r09) asks for
before a release, run on your own machine, for a repository that has no hosted
Actions minutes to run them on. Use it for private repositories on a plan without
GitHub's scanners, and for any repository that would rather gate its releases
locally.

| File | For |
|---|---|
| [`security-gate.sh`](security-gate.sh) | Scans the tree and the history for secrets, audits the dependencies for high and critical advisories, and prints a result block |

## Adopt it

1. Copy `security-gate.sh` to `scripts/security-gate.sh` and make it executable.
2. Install the tools it reports missing: `brew install gitleaks osv-scanner`. The
   script does not install anything and never reports a pass for a check it could
   not run.
3. Add a step to the repository's release checklist: run
   `scripts/security-gate.sh --record RELEASE_CHECKLIST.md` on the release commit
   and publish only on exit `0`.
4. Name the script and the tools in the README or `AGENTS.md`, so the command is
   documented, which [`S05`](../../docs/repository-quality-standard.md#s05) and
   [`S08`](../../docs/repository-quality-standard.md#s08) rely on.

## What it decides

| Check | Passes when | Fails when |
|---|---|---|
| Secret scan | `gitleaks` finds nothing in the tree or the history | It finds a secret, including one a later commit removed |
| Dependencies | `osv-scanner` finds no advisory at high severity (CVSS 7.0) or above, and none unrated | It does. Lower-severity advisories are counted and do not fail the gate |

A repository that tracks no lockfile records the dependency check as not
applicable. Exit codes: `0` every check passed or does not apply, `1` a check
found something, `2` a check could not run.

A found secret in history means the secret is compromised: revoke it, as the
repository's credential policy in [`B14`](../../docs/repository-quality-standard.md#b14)
describes, before anything else. Removing the commit does not undo the exposure.

## Limits

It checks what is in the repository, not what runs elsewhere. `osv-scanner` needs
the network to reach the advisory database. The severity filter reads the score the
database gives, and an advisory without a score is treated as high, because nobody
has said it is not.
