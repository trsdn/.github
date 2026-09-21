# Release smoke tests

<!--
Copy to docs/release-smoke-tests.md. Replace every TODO(...) marker and delete
this comment. The page documents the smoke kit for criterion R05 and holds the
dated record of the runs, so it must say what your kit really does and what it
does not cover.
-->

The release artifact is installed as a consumer receives it and checked without
anyone operating the app. TODO(app-name) does this automatically, so no
maintainer has to.

## How

[`smoke-test.yml`](../.github/workflows/smoke-test.yml) runs in every release,
called from `release.yml`, against the **draft** release before it is made
public. It also runs on demand for any tag, under Actions, Release smoke test,
Run workflow. It:

1. downloads the DMG and its checksum from the GitHub release and verifies the
   checksum. A draft needs the workflow's write token; the files are the ones a
   consumer gets after publishing;
2. installs the app into a temporary directory, so nothing outlives the run;
3. checks the signature, the Gatekeeper assessment, and the notarization ticket,
   which is what macOS applies to a downloaded app;
4. TODO(self-test): describe what the app's non-interactive entry point does and
   what output the kit requires. If the app has none, say so here and that steps 1
   to 3 are the whole kit.

After it passes, the `publish` job in `release.yml` makes the draft public and
downloads the DMG through its public URL to verify it against its checksum. If
the smoke test fails, the release stays a draft, so nobody is offered a build
that could not be installed.

The dated record is the job summary of each run: version, asset, macOS version,
what was exercised, and the result. Find it under the workflow run for the
release tag.

## What it does not cover

TODO(limits): name what needs a person at a logged-in desktop and therefore
cannot run on a hosted runner, such as global hotkeys, microphone or camera
capture, accessibility permissions, or anything that shows a permission prompt.
Say where those are checked instead, for example in the pull request template's
manual check.

## Status

TODO(status): after the first release that went through the kit, record the
version and the workflow run here. Until then, say that the order of draft, test,
publish has not been exercised.
