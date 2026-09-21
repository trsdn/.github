# Apple HIG review

A read-only agent that reviews the UI changes of a macOS Swift app against Apple's
Human Interface Guidelines, run on your own machine. It ships as a versioned
[Agent Package Manager](https://github.com/microsoft/apm) package, so an app
repository declares which version it uses, and updating it is a version change.

It runs locally and needs no CI, no token, no minutes, and no repository setting.
It reads the diff and, if the app can render its screens, the images. It edits
nothing.

## What is in it

| File | Installed as |
|---|---|
| [`.apm/agents/apple-hig-reviewer.agent.md`](.apm/agents/apple-hig-reviewer.agent.md) | The reviewer agent |
| [`.apm/instructions/apple-hig-review.instructions.md`](.apm/instructions/apple-hig-review.instructions.md) | The review rules, applied to `**/*.swift` |
| [`.apm/prompts/apple-hig-review.prompt.md`](.apm/prompts/apple-hig-review.prompt.md) | The request to review the current branch |

Nothing in the package is specific to one app. What is, lives in the app's own
`AGENTS.md`, which the agent reads first: the kind of app (menu-bar, windowed,
document-based), the user data it handles, and the command that renders its
screens, if it has one.

## Use it in an app repository

1. Install APM once: `brew install apm`.
2. Declare the dependency and the tools to install for in the repository's
   `apm.yml`, pinned to a tag of this repository. APM refuses to install without
   `targets`:

   ```yaml
   name: my-app
   version: 1.0.0
   targets:
     - claude
     - copilot
   dependencies:
     apm:
       - trsdn/.github/packages/apple-hig-review#v1.19.1
   ```

3. Run `apm install`. It writes these files and `apm.lock.yaml`, which records the
   resolved commit and a hash of every file:

   | For | Written to |
   |---|---|
   | Claude Code | `.claude/agents/apple-hig-reviewer.md`, `.claude/rules/apple-hig-review.md`, `.claude/commands/apple-hig-review.md` |
   | GitHub Copilot | `.github/agents/apple-hig-reviewer.agent.md`, `.github/instructions/apple-hig-review.instructions.md`, `.github/prompts/apple-hig-review.prompt.md` |

   It also adds `apm_modules/` to `.gitignore`. Commit the installed files, the lock
   file and `apm.yml`, so a fresh clone has the reviewer without installing
   anything. Never edit the installed files by hand; change the version instead.
   `apm audit` replays the install and reports any file that differs.
4. In `AGENTS.md`, say what kind of app it is, what user data it handles, and the
   command that renders its screens, if there is one. See
   [`AGENTS.macos.md`](../../templates/macos-app/AGENTS.macos.md).

## Run it

Before merging a change that touches UI code, and before a release, ask your agent
runtime to review the branch with the `apple-hig-reviewer` agent, or run the
`apple-hig-review` prompt. Put the outcome in the pull request description: that is
the record. An agent doing the change runs it as a step of its own procedure, the
way it runs the tests.

The review is only as good as what it can see. With a renderer it looks at the
images in light and dark appearance; without one it reviews the source and says so.
A renderer is a command-line flag on the app that draws its windows offscreen at
fixed sizes and writes one PNG per screen, with animation frozen and no permissions
or network needed. It is worth writing for an app with a real interface.

## Versions

The package is versioned by the tag of this repository. Pin a tag, not `main`, so
that a change to the reviewer's rules reaches an app only when its maintainer or
its agent moves the tag and reruns `apm install`. Rerun after every move, and read
the diff of the installed files: they are the rules the review will follow.

## Verified, and not

Installed with `apm` 0.31.0 into an empty repository for the `claude` and `copilot`
targets: it writes the six files above, records them in the lock file, and
`apm audit` reports no drift. Not verified: how each agent runtime behaves when it
runs the reviewer. The agent lists its tools by both runtimes' names, because APM
copies the list unchanged into each target and Claude Code and Copilot name their
tools differently. If a runtime rejects a name it does not know, remove the other
family's names for that runtime and cut a new tag.
