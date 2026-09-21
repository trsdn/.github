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
2. Declare the dependency in the repository's `apm.yml`, pinned to a tag of this
   repository:

   ```yaml
   name: my-app
   version: 1.0.0
   dependencies:
     apm:
       - trsdn/.github/packages/apple-hig-review#v1.19.0
   ```

3. Run `apm install`. It writes the agent, the instructions and the prompt into the
   directories your agent runtimes read, and records the resolved source and content
   hashes in the lock file. Commit the installed files and the lock file, so a fresh
   clone has the reviewer without installing anything. Never edit the installed
   files by hand; change the version instead. `apm audit` reports hand edits.
4. In `AGENTS.md`, say what kind of app it is, what user data it handles, and the
   command that renders its screens to images, if there is one. See
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

## Not verified

The manifest and layout follow APM's documented `.apm/` package layout. The package
has not been installed with `apm` yet, and how APM maps the agent's `tools` list to
each runtime is not confirmed. The first installation in a repository is the test:
if it needs a change, change the package and cut a new tag.
