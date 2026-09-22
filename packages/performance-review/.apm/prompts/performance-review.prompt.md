---
description: Review the current branch's changes for performance defects, the way a senior engineer reviews architecture
---

<!-- markdownlint-disable MD041 -->

Review the current branch's changes with the `performance-reviewer` agent.

1. Find the changes: `git diff <default branch>...HEAD`, and read enough
   surrounding code — the caller, the hot path it sits in, how often it runs —
   to judge whether the change does the right amount of work in the right
   place.
2. If `AGENTS.md` documents a measurement command and a specific finding would
   benefit from a number, run it. Otherwise review from the code alone.
3. Report findings in the format the agent defines: severity, location,
   rationale, correction. Or say plainly that there are none, and name what was
   read and, if anything, what was measured.

Do not edit any file, and do not run anything beyond a documented measurement
command.
