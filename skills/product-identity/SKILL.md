---
name: "product-identity"
description: "Audits what a built artifact embeds about itself — product name, version, repository and issue tracker URLs, licence and copyright — and whether those values are produced by the build or typed by hand. Covers I01, I02, I03 and I06 of the trsdn Repository Quality Standard, and reports I04 and I05 for a human to judge. Use when a repository ships an app, a package, a binary or an image."
---

<!-- markdownlint-disable MD041 -->

## What this is for

A shipped artifact that cannot say what it is, where it came from, or where to
report a problem with it turns every bug report into an investigation. The
Product Identity criteria ask for that metadata; this skill finds out what is
already there, in whichever manifest the repository actually uses.

It reads. It does not write: fixing identity means editing a manifest or a
release workflow, and that is ecosystem-specific enough that doing it blind is
worse than not doing it.

## How to use it

```sh
python3 scripts/audit.py --path /path/to/checkout
```

It finds `Info.plist`, `package.json`, `pyproject.toml` and `*.csproj`, merges
what they embed, and then reads the release workflows to see where the values
come from. `--json` gives machine-readable output.

Results are `met`, `gap`, `judgement`, or `unknown`, and `unknown` is the honest
answer when the repository builds nothing — in which case `I01`-`I06` are
`Not applicable` and the evidence should say what was looked for.

## What each result asks of you

**`I01` name and version, `I02` repository and issue tracker.** These are
ordinary manifest fields everywhere except a macOS bundle, where there is no
standard `Info.plist` key for either URL. The audit reports any key whose name
suggests one, so if the account has a convention, it is found; if not, pick one
and use the same key everywhere rather than a different one per app.

**`I03` licence and copyright.** Where the licence is named inside the copyright
string rather than its own field, the audit says so and leaves the call to you.
Either satisfies a reader; only one satisfies a tool that parses it.

**`I06` derived, not typed.** This is the criterion that keeps the other three
true. A version typed into a manifest is correct until the day someone forgets,
and nothing fails when they do. The audit looks for a workflow or build script
that reads the tag or the repository — `github.ref_name`, `GITHUB_REPOSITORY`,
`agvtool`, `git describe`. If it finds none, the fix is to derive the value at
build time, not to correct the literal.

**`I04` the running product.** Nothing in a checkout proves what an About window
shows. Run it, or read the code that builds that window, and say which you did.
A `--version` flag, a `--help` footer, an About panel, or a site footer all
satisfy it.

**`I05` icons.** Needs looking at the icons the product ships against any store
or site surface. It is a judgement about consistency, and it is the one criterion
here that no script should pretend to decide.

## Rules

- **Report what is embedded, not what should be.** The audit prints the values it
  found so you can check them against the repository, rather than trusting a
  pass.
- **A wrong value is worse than a missing one.** An artifact naming the wrong
  issue tracker sends reports where nobody reads them. Check the URLs resolve to
  this repository before recording `I02` as met.
- **Never commit.** Leave manifest changes in the working tree for review.
- **Say which criteria you could not reach**, and why, rather than recording a
  result the evidence does not support.
