# Site content review

A read-only agent that checks a published site's content and mechanics against
the standard's `W01`-`W04`, `W07`, `W08`, and `W09`'s three enumerated Fail
cases, run on your own machine. It ships as a versioned
[Agent Package Manager](https://github.com/microsoft/apm) package, the same way
as the account's other packages.

It runs locally and needs no CI, no minutes, no dedicated token, and no
repository setting. It reads the homepage field and the Pages configuration
through your own already-authenticated `gh` session, which `W01` and `W02`
cannot be checked without. It edits nothing, and it does not judge design taste: `W09` itself
says whether a design is good is outside what the criterion decides, and this
package holds that line — it reports only the three mechanical cases the
standard actually names as a `Fail` (no stylesheet, an unmodified framework
theme, another project's site copied unchanged), never an aesthetic opinion.
For an actual design pass, use
[`frontend-designer`](../frontend-designer/README.md).

## What is in it

| File | Installed as |
|---|---|
| [`.apm/agents/site-content-reviewer.agent.md`](.apm/agents/site-content-reviewer.agent.md) | The reviewer agent |
| [`.apm/instructions/site-content-review.instructions.md`](.apm/instructions/site-content-review.instructions.md) | The exact test for each of `W01`-`W04`, `W07`, `W08`, `W09` |
| [`.apm/prompts/site-content-review.prompt.md`](.apm/prompts/site-content-review.prompt.md) | The request to review the current site |

## Use it in a repository

1. Install APM once: `brew install apm`.
2. Declare the dependency in the repository's `apm.yml`, pinned to a tag of
   this repository:

   ```yaml
   name: my-repo
   version: 1.0.0
   targets:
     - claude
     - copilot
   dependencies:
     apm:
       - trsdn/.github/packages/site-content-reviewer#v1.26.0
   ```

3. Run `apm install`. It writes the agent, instructions, prompt and rule files
   for each declared target and records them in `apm.lock.yaml`. Commit the
   installed files and the lock file.

## Run it

Ask your agent runtime to follow the installed prompt, or tell it to act as the
`site-content-reviewer` agent against the repository's published site. Worth
running after [`frontend-designer`](../frontend-designer/README.md) drafts or
changes a site, and before a release.

## Versions

Pinned by tag, the same convention as the account's other packages.

## Verified, and not

Installed with `apm` 0.31.0 into an empty repository for the `claude` and
`copilot` targets: it writes the agent, instructions, prompt and rule files for
both, records them in the lock file, and `apm audit` reports no drift. Not
verified: an actual review run against a real published site.
