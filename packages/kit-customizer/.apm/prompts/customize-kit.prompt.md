---
description: Tune a freshly copied trsdn/.github starter kit to this repository, resolving every TODO(...) and EDIT marker with verified values
---

<!-- markdownlint-disable MD041 -->

Tune the kit files just copied into this repository with the `kit-customizer`
agent.

1. Find every `TODO(name)` and `# EDIT: ...` marker in the files the kit
   copied (typically under `.github/`, `.swiftlint.yml`, and an `AGENTS.md`
   section).
2. For each, read the instructions to resolve it in priority order: the
   repository's own manifest, an existing command, a linter run against the
   real code, then the kit's own fallback.
3. Run what you can to verify a value before leaving it in place — build,
   test, lint — and drop any lint rule the run shows fails on real code.
4. Report what you resolved, what you verified by running, and what you left
   in place because you could not determine it safely.

Do not commit, push, or open a pull request. Do not touch files the kit did
not copy.
