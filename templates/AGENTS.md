# Agent instructions

<!--
Starting point for satisfying criteria G01 to G08 of the Repository Quality
Standard. Replace every bracketed placeholder, delete what does not apply, and
delete this comment.

A section you cannot fill in honestly is a finding, not a formatting problem.
"There is no validation command" means an agent cannot check its own work, which
is criterion G05 failing.
-->

Read this before changing anything in this repository.

## What this repository is

[One paragraph: what it produces, who consumes it, and what breaks elsewhere
when it changes. An agent that does not know the blast radius cannot judge
risk.]

## What this repository is not

[The adjacent thing people mistake it for. Prevents work landing in the wrong
place.]

## Layout

| Path | Purpose |
|---|---|
| `[path]` | [What lives here and who owns it.] |

Mark generated, vendored, and machine-owned paths explicitly. Anything not
listed as generated is assumed to be hand-maintained and editable.

- Generated, never hand-edit: [paths, and the command that regenerates them]
- Vendored, update through [tool] only: [paths]

## Setup

```sh
[commands that take a clean checkout to a working state]
```

[Required runtime versions and where they are pinned.]

## Run

```sh
[how to start the thing during development]
```

## Validate before proposing a change

This is the single command that must succeed:

```sh
[test, lint, type-check, or build command]
```

[If several commands are needed, list them all and state that all must pass.
State what each one catches, so a failure is diagnosable rather than mysterious.]

## Conventions

[Only what is not obvious from reading the code: naming, structure, error
handling, logging, and where new code of a given kind belongs.]

## Do not do these

<!-- Required by G03. Keep the entries that apply, add repository-specific ones. -->

- Do not rewrite history, force push, or delete branches.
- Do not commit secrets, tokens, credentials, or personal data.
- Do not deploy, publish a release, create or move tags, or change repository
  settings. [State who does, and how.]
- Do not run destructive data commands, including migrations against real data,
  bulk deletes, or resets. [Name the specific commands.]
- Do not hand-edit generated files. [Name them and their regeneration command.]
- Do not add dependencies without [stated approval path].

## Attribution

[How agent-authored changes are identified and reviewed: commit trailers, pull
request labels, or a stated review expectation. Required by G07.]
