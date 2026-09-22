# Kit customizer

An agent that tunes a starter kit just copied from `trsdn/.github`'s
[`templates/`](../../templates/) to the specific repository it landed in —
resolving every `TODO(...)` and `# EDIT: ...` marker with a value verified
against the actual code, not a plausible guess. It ships as a versioned
[Agent Package Manager](https://github.com/microsoft/apm) package, the same way
as the account's other packages.

**This is a writer**, like [`frontend-designer`](../frontend-designer/README.md):
it edits files in the working tree and never commits or opens a pull request
itself. It runs locally, needs no CI, no token, and no repository setting.

## Why this exists

The kits are deliberately generic — a lint rule set, a CI version matrix, a
Dependabot ecosystem list that has to fit whatever repository adopts it. Three
pilots that adopted `templates/macos-app` by hand found exactly the gaps a
generic kit leaves: a SwiftLint rule the installed version had renamed, a rule
set that failed the moment it ran against real code, a smoke-test workflow
whose permissions didn't match the order it actually ran in. None of those were
defects in the kit; they were the customization step nobody had done yet. This
package does that step, and verifies its own answers by running the tool it is
configuring rather than reading code and guessing.

## What is in it

| File | Installed as |
|---|---|
| [`.apm/agents/kit-customizer.agent.md`](.apm/agents/kit-customizer.agent.md) | The customizer agent |
| [`.apm/instructions/kit-customization.instructions.md`](.apm/instructions/kit-customization.instructions.md) | How to resolve each marker, in priority order, per kit |
| [`.apm/prompts/customize-kit.prompt.md`](.apm/prompts/customize-kit.prompt.md) | The request to tune the kit files just copied in |

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
       - trsdn/.github/packages/kit-customizer#v1.27.0
   ```

3. Run `apm install`. It writes the agent, instructions, prompt and rule files
   for each declared target and records them in `apm.lock.yaml`. Commit the
   installed files and the lock file.

## Run it

Right after copying a kit from `templates/` (or as part of the
[fleet-rollout procedure](../../docs/fleet-rollout.md)'s pipeline step), ask
your agent runtime to follow the installed prompt, or tell it to act as the
`kit-customizer` agent, against the files just copied in. It searches for
`TODO(...)` and `# EDIT: ...` markers, resolves each against the repository's
actual manifest and, where a command exists to check its answer, runs it —
building, testing, or linting — before leaving a value in place. Look at its
report before committing: it names every marker it could not verify and left
untouched, and those need your judgement, not a guess.

## Versions

Pinned by tag, the same convention as the account's other packages.

## Verified, and not

Not yet installed or run. The package layout follows the pattern the
account's other packages verified with `apm` 0.31.0, but neither the install
nor an actual customization pass against a real, freshly copied kit has been
tested yet. Verify both before relying on it.
