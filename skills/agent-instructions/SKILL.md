---
name: "agent-instructions"
description: "Finds where tool-specific agent instruction files — copilot-instructions.md, CLAUDE.md, GEMINI.md, cursor and windsurf rules — have drifted from AGENTS.md, by checking each points at it and listing rules stated in one and not the other. Covers G04 of the trsdn Repository Quality Standard. Use when a repository has more than one instruction file, or before trusting any of them."
---

<!-- markdownlint-disable MD041 -->

## What this is for

The standard says `G04` "is the criterion that decays first", and it is right
for a mechanical reason: nothing breaks when two instruction files disagree. Each
agent reads its own file, behaves differently, and both look fine in isolation.
You find out when two agents make opposite changes to the same repository.

This checks the half a script can, and prepares the half it cannot.

## How to use it

```sh
python3 scripts/audit.py --path /path/to/checkout
```

Read-only. `--json` gives machine-readable output.

It looks for the files `G04` enumerates — `.github/copilot-instructions.md`,
`CLAUDE.md`, `GEMINI.md`, `.cursorrules`, `.cursor/rules/`, `.windsurfrules`,
`.clinerules` — and reports one of:

- **gap, no `AGENTS.md`** — tool files exist and there is no tool-neutral file for
  them to agree with. Every agent is then following a different document by
  construction.
- **gap, unlinked** — a tool file never mentions `AGENTS.md`. `G04` asks it to
  point at the neutral file rather than paraphrase it.
- **judgement, drift** — the files point at `AGENTS.md`, but state rules that have
  no counterpart there. Those are listed, and they are where a contradiction
  hides.
- **met** — each tool file points at `AGENTS.md` and states no rule it does not.

## How the drift list is built, and what it is worth

The script reduces every rule-shaped line to its meaningful words and asks
whether `AGENTS.md` states something substantially similar. A rule repeated in
both is not reported — repetition is a `B13` matter, not a `G04` one. A rule that
appears in only the tool file is reported, because that is the one an agent
follows and a reader of `AGENTS.md` never sees.

It is a word overlap, so treat it as a reading list and not a verdict:

- A rule phrased differently in the two files may be flagged although both say
  the same thing. Read it and move on.
- **A direct contradiction may not be flagged at all**, because "always squash
  commits" and "never squash commits" share almost every word. The script cannot
  see the negation; you can.

That second case is the reason the result is `judgement` and never `fail`.

## What to do with the findings

The fix is almost always to **delete, not to reconcile**. A tool-specific file
should be a pointer: the tool's name, one line telling the agent to read
`AGENTS.md`, and nothing else. Every rule it holds is a rule that has to be kept
correct in two places, and the one that gets forgotten is whichever file you were
not editing that day.

Where a rule genuinely is tool-specific — a model's own quirk, a setting only one
tool honours — keep it, and keep only that. The test is whether another agent
reading it would be wrong to follow it.

## Rules

- **Never resolve a contradiction by guessing which file is right.** Ask the
  maintainer; the two files are evidence that nobody has decided.
- **`AGENTS.md` is the one that wins.** If a tool file disagrees, the tool file
  changes.
- **Never commit.** Leave edits in the working tree for review.
