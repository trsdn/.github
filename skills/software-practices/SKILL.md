---
name: "software-practices"
description: "Reads a repository for the software practices that can be read rather than run: reproducible setup, environment-driven configuration with no exposed defaults, logs and errors that are actionable without leaking credentials, documented architecture, and terminal output that survives without colour. Covers S01, S06, S07, S10 and X04 of the trsdn Repository Quality Standard. Use before a release, when adopting the standard, or when an assessment reports one of those gaps."
---

<!-- markdownlint-disable MD041 -->

## What this is for

These four criteria are the ones a maintainer answers from memory and gets
wrong, because each is about a detail that was true when it was written and
quietly stopped being true. A home-directory path that worked on one machine. A
log line added while debugging that prints a token. A README whose setup
commands describe the previous build system.

The audit reads the repository for each and shows the lines, so the answer comes
from the source rather than recollection.

## How to use it

```sh
python3 scripts/audit.py --path /path/to/checkout
```

Read-only. `--json` gives machine-readable output. Results are `met`, `gap`,
`judgement`, or `unknown`, and `unknown` is the honest answer where the criterion
does not reach this repository — `S06` where nothing reads configuration, `S07`
where the code emits no logs. Both are `Not applicable` then, recorded with what
was looked for.

## What each result asks of you

**`S01` reproducible setup.** Two halves: the versions, and the commands. A
lockfile plus documented commands is a pass. A manifest with ranges and no
lockfile is a judgement — a library that declares ranges meets the pinning half
deliberately, an application usually should not. Check the commands in the README
still describe the build that exists now, which is the half that rots.

**`S06` configuration.** The audit flags a committed default holding a
home-directory path or a personal email address, because the criterion names
exactly those. It ignores placeholder addresses at `example.com`. A flagged line
is not automatically a secret, but it is automatically a thing that only works on
one machine.

**`S07` logs and errors.** Two failures, and the audit separates them:

- A log line naming a credential or personal field. Logging the *name* of a token
  is fine; logging its value is the failure. The audit cannot tell which, so it
  shows the line and you decide.
- A message that does not say what failed. `"error"` is the example the standard
  gives of the minimum not being met. The audit only catches the blatant ones —
  a message can be a full sentence and still be useless.

**`S10` architecture.** The audit finds candidate documents; it cannot judge
whether they name the components and the constraints. Read them against the
question the criterion actually asks: *what could a new contributor break without
knowing it?* A required ordering, an external service, a compatibility floor. If
the answer is not written anywhere, that is the gap, whatever else the document
covers.

**`X04` output without colour.** A command's output is read through a pipe, in a
log, and by a screen reader as often as it is read in a colourful terminal. Two
failures: colour with no way to turn it off, and meaning carried only by a symbol.
A green tick that is the *only* signal of success disappears the moment the output
is piped; a tick beside the word "passed" is decoration and is fine. The audit
cannot tell those apart, which is why it reports the lines and asks.

## Rules

- **A flagged log line is a question, not a verdict.** Read it before changing
  it, and never "fix" one by deleting the log. A silent failure is worse than a
  noisy one.
- **If you find a real credential, stop.** Tell the maintainer which one and what
  it unlocks. Do not rotate it, delete it, or rewrite history yourself.
- **Fix the cause for `S06`.** Moving a home path into an environment variable is
  the fix; adding it to `.gitignore` after it was committed is not.
- **Never commit.** Leave changes in the working tree for review.
- **Say what you could not read.** A file the audit skipped is not a file with
  nothing in it.
