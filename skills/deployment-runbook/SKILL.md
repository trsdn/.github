---
name: "deployment-runbook"
description: "Audits a repository that runs something standing — a launchd agent, a container, a systemd unit — for the Deployable criteria: documented target and command, secrets referenced rather than committed, health verification and a way back, constrained runtimes, operational history, and backup where it holds state. Covers D01 to D06 of the trsdn Repository Quality Standard. Use for anything that runs without someone starting it."
---

<!-- markdownlint-disable MD041 -->

## What this is for

Five of these six criteria are ones the standard calls **critical**: their
failure is what makes a repository `At risk` rather than merely `Needs work`.
That is the right weighting, because a standing deployment is the software that
fails while nobody is watching, and the questions here — where does it run, what
does it need, how do I know it is working, how do I put it back — are the ones
asked at the worst possible moment.

The Deployable profile is narrower than it looks and wider than people assume.
It is not "has a Dockerfile". It is *the maintainer operates a standing
deployment*, which includes **an installation on a workstation that runs or is
scheduled without the maintainer starting it**. A launchd agent with `RunAtLoad`
is a deployment. A CLI you type is not.

## How to use it

```sh
python3 scripts/audit.py --path /path/to/checkout
```

Read-only. `--json` gives machine-readable output. It finds launchd plists with
`RunAtLoad` or `ProgramArguments`, Dockerfiles and Compose files, and systemd
units, and reports nothing but `unknown` when it finds none of them — which is
the answer for a repository the profile does not reach.

## What each result asks of you

**`D01` the runbook.** Four things, not one: where it runs, what it needs first,
how it is configured, and the command. An installer script is evidence for the
command and silent about the other three. The audit points at candidates; read
them for all four.

**`D02` secrets.** Reported as `Not applicable` where nothing in the repository
references a secret at all, rather than as a gap — a utility that needs no
credential does not fail for having no vault. Where secrets *are* used, the
criterion wants them referenced and their safe location written down. If the
audit reports a committed secret value, **stop**: tell the maintainer which
credential and what it unlocks, and do not rotate, delete, or rewrite history
yourself.

**`D03` health and the way back.** Both, and they fail independently. A health
step that is "check it works" is not a command or an observable. For a launchd
agent the way back is usually the previous binary plus a reload; for a container
it is the previous tag. Write whichever it is, because the moment you need it is
not the moment to work it out.

**`D04` constrained runtime.** An image without a tag, or one pinned to
`:latest`, is not constrained. Neither is a program launched through
`/usr/bin/env`, where the interpreter is whatever the `PATH` finds at load time.
Where the unit file is a **template** with a placeholder substituted at install
time, the audit says so instead of claiming it is pinned — the real constraint is
whatever the installer writes, so read that.

**`D05` operational history.** A changelog, decision records, releases, or linked
issues all satisfy it. Check which this repository already uses before adding a
file nobody will maintain.

**`D06` state.** The audit treats a working directory or a declared volume as
state, and deliberately does *not* count a log path: a log is worth having and is
not a thing you restore from backup. Where it does hold state, say what would be
lost and how it comes back.

## Rules

- **A deployment bound to one home directory is worth reporting even when no
  criterion names it.** A `WorkingDirectory` under `/Users/<someone>` means the
  deployment only exists on one machine, and nothing here will tell you that on
  the day that machine is replaced.
- **Never change a running deployment to satisfy an audit.** Write the runbook
  first; the fix belongs to a deliberate change, not to a review.
- **Never commit.** Leave documentation in the working tree for review.
- **Say what you could not read.** A critical criterion recorded from a guess is
  worse than one recorded as unknown.
