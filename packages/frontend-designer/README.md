# Frontend designer

An agent that researches a repository and the product it ships, then designs and
writes a static site made for that specific project — not from a shared kit, not
from a framework default. It ships as a versioned
[Agent Package Manager](https://github.com/microsoft/apm) package, the same way
as the account's other packages.

**This is a writer, not a reviewer**, unlike [`apple-hig-review`](../apple-hig-review/README.md),
[`performance-review`](../performance-review/README.md), and
[`site-content-reviewer`](../site-content-reviewer/README.md). It edits files in
the working tree: it writes the site. It runs locally, needs no CI, no token,
and no repository setting beyond writing those files, and it never commits or
opens a pull request itself — you review what it built the way you would review
a human designer's draft, then commit it yourself.

## Why a writer can do this well

[Decision 0013](../../docs/decisions/0013-sites-are-designed-not-templated.md)
retired this account's own shared design language because nine unrelated
products sharing one look told a visitor nothing about any of them. That is a
real risk for an agent too: an agent that designs many sites without looking
closely at each one converges on its own default, which is the same failure
with one more author. This package's entire design is built against that risk:
it reads the specific repository and product first — the source, the README,
existing branding, the product's own voice — and is instructed to actively
avoid repeating a look it has already produced, before it writes a single
colour value. See the agent file for exactly what it reads and in what order.

## What is in it

| File | Installed as |
|---|---|
| [`.apm/agents/frontend-designer.agent.md`](.apm/agents/frontend-designer.agent.md) | The designer agent |
| [`.apm/instructions/frontend-design.instructions.md`](.apm/instructions/frontend-design.instructions.md) | The research-first process and the standard's constraints (`W01`-`W04`, `W07`, `W08`, `W09`) |
| [`.apm/prompts/design-site.prompt.md`](.apm/prompts/design-site.prompt.md) | The request to design and write the site |

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
       - trsdn/.github/packages/frontend-designer#v1.26.0
   ```

3. Run `apm install`. It writes the agent, instructions, prompt and rule files
   for each declared target and records them in `apm.lock.yaml`. Commit the
   installed files and the lock file.

## Run it

With a `trsdn/.github` checkout on your machine, ask your agent runtime to
follow the installed prompt (in Claude Code, the installed slash command; in
Copilot, the equivalent reusable prompt) or to act as the `frontend-designer`
agent. It will research the repository, explain its design choices as it goes,
write the site into `docs/` or `site/`, and stop — leaving the files for you to
look at, adjust, and commit.

Look at the result before committing. A generated design is a strong first
draft, not a finished one: check that the voice actually sounds like the
product, that a screenshot or example is real rather than generic, and that
nothing reads as though it could describe any other project just as well. If
your agent runtime supports live-previewing a page as you iterate, use it —
the instructions ask the agent to do the same where it can.

Run [`site-content-reviewer`](../site-content-reviewer/README.md) afterward to
check the mechanical parts (`W01`-`W04`, `W07`, `W08`, and `W09`'s enumerated
Fail cases) before you publish.

## Versions

Pinned by tag, the same convention as the account's other packages.

## Verified, and not

Not yet installed or run. The package layout and `apm.yml`/`targets`
requirements follow the pattern the account's other packages verified with
`apm` 0.31.0, but a writer agent with edit access is a new shape for this
account's packages, and neither the install nor an actual design run against a
real repository has been tested yet. Verify both before relying on it.
