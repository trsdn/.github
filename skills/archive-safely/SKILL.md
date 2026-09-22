---
name: "archive-safely"
description: "Checks whether a repository is safe to archive: whether a launchd job it defines is still loaded on this machine, whether the README says why and when maintenance ended, and whether a successor is linked. Covers A01 to A04 of the trsdn Repository Quality Standard. Use before archiving anything, especially anything that ran on a schedule."
---

<!-- markdownlint-disable MD041 -->

## What this is for

Archiving is the one repository change that cannot be undone by reading the
repository afterwards. It makes the code read-only and, far more importantly, it
tells every future reader that nothing here is running.

That claim is false in the most dangerous case: a launchd agent installed from
this repository is still loaded. The repository goes read-only, the agent keeps
running on a schedule, and the next person wondering why something still happens
every morning finds an archived repository and concludes it cannot be the cause.

So this checks the machine, not only the files.

## How to use it

```sh
python3 scripts/pre-archive-check.py --path /path/to/checkout --repo OWNER/NAME
```

It exits non-zero when it finds a loaded job, so it can gate an archive step. It
only reads: it never unloads anything, never archives, and never edits.

**Run it on the machine that operates the deployment.** `launchctl` only knows
about jobs on the machine it runs on, so a clean result from a laptop says
nothing about the Mac mini in the cupboard. Where `launchctl` cannot be read at
all, the result is `unknown` and says so rather than passing.

## What each result asks of you

**`A04` nothing is still running.** The check compares every `Label` in the
repository's plists against what launchd currently has loaded. A match is the
finding, and the fix is to unload it first:

```sh
launchctl bootout gui/$UID/<label>
```

Where jobs are defined but none is loaded here, the result is a judgement, not a
pass, because the criterion also covers *undocumented dependencies*: something
else that reads this repository's output, a scheduled task on another machine, a
shortcut that calls its binary. Those are yours to think about; no script finds
them.

**`A01` the archive switch.** Assessed last, deliberately. Everything else here
is what to do *before* flipping it.

**`A02` why and when.** A reader arriving in two years wants one sentence: what
this was, why it stopped, and when. "Unmaintained" without a date leaves them
guessing whether it stopped last month or five years ago.

**`A03` the successor.** Only applies where something replaced it. If nothing
did, that is `Not applicable`, and saying so is better than silence — it answers
the question a reader would otherwise go looking for.

## Rules

- **Never unload, stop, or delete anything yourself.** Report it. The maintainer
  decides whether that job should stop, and stopping something on a schedule is
  exactly the kind of change that should not happen inside a review.
- **Never archive a repository.** That is a maintainer action and a settings
  change.
- **A clean result from the wrong machine is not a clean result.** Say which
  machine you ran on.
- **Write the README sentences before archiving, not after.** Once it is
  archived, a pull request to fix the README is no longer possible without
  unarchiving it.
