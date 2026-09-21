---
# GitHub Agentic Workflow source. Copy to .github/workflows/apple-hig-visual-review.md,
# replace every TODO(...) marker, then run `gh aw compile` and commit the compiled
# .lock.yml it produces. The README beside this kit says how, and lists the risks.
#
#   TODO(app-name)         The app's display name.
#   TODO(source-glob)      Glob for the Swift sources, for example "Sources/MyApp/**/*.swift".
#   TODO(source-dir)       The directory that glob is under, for the diff, for example Sources/MyApp.
#   TODO(test-file)        The test that pins the snapshot plan, for example Tests/MyAppTests/UISnapshotPlanTests.swift.
#   TODO(binary-path)      The built executable, for example .build/release/MyApp.
#   TODO(render-flag)      The command-line flag that makes the app write its snapshots and exit.
#   TODO(snapshot-count)   How many PNGs the renderer writes. Set it in both places it appears.
#   TODO(build-command)    The build, for example swift build -c release -Xswiftc -warnings-as-errors.
#   TODO(artifact-prefix)  A lowercase name for the artifact, for example myapp.
#   TODO(extra-paths)      Other files whose change should trigger a review, such as the icon and
#                          Info.plist, or delete those lines.
#
# The workflow needs a renderer in the app: a headless entry point that draws the
# app's windows offscreen at fixed sizes and writes one PNG per surface, without
# permissions, network, or the keychain. This kit cannot supply it.
name: Apple HIG visual review
description: Generates deterministic macOS UI screenshots and submits one read-only HIG review on relevant pull requests
on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]
    paths:
      - "TODO(source-glob)"
      - "TODO(test-file)"
      - "TODO(extra-paths)"
      - ".github/instructions/apple-hig-review.instructions.md"
      - ".github/agents/apple-hig-reviewer.agent.md"
      - ".github/workflows/apple-hig-visual-review.md"
      - ".github/workflows/apple-hig-visual-review.lock.yml"
permissions:
  contents: read
  pull-requests: read
  copilot-requests: none
checkout:
  fetch-depth: 0
engine:
  id: copilot
  agent: apple-hig-reviewer
network: {}
tools:
  edit: false
  cli-proxy: false
  bash:
    - cat
    - file
    - find
    - git diff
    - git status
    - ls
    - shasum
    - wc
safe-outputs:
  noop:
    report-as-issue: false
  missing-tool:
    create-issue: false
  missing-data:
    create-issue: false
  report-incomplete: false
  report-failure-as-issue: false
  report-failed-jobs: false
  submit-pull-request-review:
    max: 1
    allowed-events: [COMMENT]
jobs:
  snapshots:
    name: Render UI snapshots
    runs-on: macos-latest
    timeout-minutes: 15
    permissions:
      contents: read
    steps:
      - name: Checkout
        # actions/checkout v7
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1

      - name: Build snapshot renderer
        run: TODO(build-command)

      - name: Generate and validate snapshots
        env:
          EXPECTED_SNAPSHOTS: "TODO(snapshot-count)"
        run: |
          set -euo pipefail
          snapshots="$RUNNER_TEMP/ui-snapshots"
          TODO(binary-path) TODO(render-flag) "$snapshots"

          count="$(find "$snapshots" -type f -name '*.png' | wc -l | tr -d ' ')"
          if [ "$count" -ne "$EXPECTED_SNAPSHOTS" ]; then
            echo "::error::Expected $EXPECTED_SNAPSHOTS UI snapshots, found $count."
            exit 1
          fi
          while IFS= read -r snapshot; do
            test -s "$snapshot"
            file "$snapshot" | grep -q 'PNG image data'
          done < <(find "$snapshots" -type f -name '*.png' | sort)

      - name: Upload deterministic UI snapshots
        # actions/upload-artifact v7
        uses: actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a
        with:
          name: TODO(artifact-prefix)-ui-snapshots-${{ github.event.pull_request.number }}
          path: ${{ runner.temp }}/ui-snapshots
          if-no-files-found: error
          retention-days: 14

  agent:
    needs: snapshots
    timeout-minutes: 25
steps:
  - name: Download UI snapshot evidence
    # actions/download-artifact v8
    uses: actions/download-artifact@3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c
    with:
      name: TODO(artifact-prefix)-ui-snapshots-${{ github.event.pull_request.number }}
      path: /tmp/gh-aw/agent/ui-snapshots

  - name: Validate and prepare review evidence
    env:
      BASE_SHA: ${{ github.event.pull_request.base.sha }}
      HEAD_SHA: ${{ github.event.pull_request.head.sha }}
      EXPECTED_SNAPSHOTS: "TODO(snapshot-count)"
    run: |
      set -euo pipefail
      evidence=/tmp/gh-aw/agent
      snapshots="$evidence/ui-snapshots"

      count="$(find "$snapshots" -type f -name '*.png' | wc -l | tr -d ' ')"
      if [ "$count" -ne "$EXPECTED_SNAPSHOTS" ]; then
        echo "::error::Expected $EXPECTED_SNAPSHOTS UI snapshots, found $count."
        exit 1
      fi
      while IFS= read -r snapshot; do
        test -s "$snapshot"
        file "$snapshot" | grep -q 'PNG image data'
      done < <(find "$snapshots" -type f -name '*.png' | sort)

      git diff --no-ext-diff "$BASE_SHA" "$HEAD_SHA" -- \
        TODO(source-dir) \
        TODO(test-file) \
        TODO(extra-paths) \
        .github/instructions/apple-hig-review.instructions.md \
        .github/agents/apple-hig-reviewer.agent.md \
        > "$evidence/pr-ui-diff.patch"
      cp .github/instructions/apple-hig-review.instructions.md "$evidence/"
      cp .github/agents/apple-hig-reviewer.agent.md "$evidence/"
---

# Review the rendered macOS UI

Review pull request #${{ github.event.pull_request.number }} without editing any
file.

The deterministic evidence is already prepared:

- `/tmp/gh-aw/agent/ui-snapshots/` contains TODO(surfaces: the production
  surfaces the renderer draws, for example Settings, About, and the main window,
  in light and dark appearances, plus larger accessibility-text variants).
- `/tmp/gh-aw/agent/pr-ui-diff.patch` contains the relevant pull-request diff.
- `/tmp/gh-aw/agent/apple-hig-review.instructions.md` contains the repository's
  HIG criteria.
- `/tmp/gh-aw/agent/apple-hig-reviewer.agent.md` contains the custom reviewer
  contract.

Inspect every PNG and compare corresponding light/dark images and the
larger-text variants. Correlate any visible issue with the diff and surrounding
source. Report only high-confidence, actionable defects introduced or exposed
by this pull request. Do not report subjective polish, do not infer unrendered
behavior from screenshots, and do not duplicate existing review comments.

Submit exactly one pull-request review with event `COMMENT`:

- If findings exist, use a concise list. Each item must include severity,
  repository-relative location, visible or concrete impact, and a specific
  correction.
- If no qualifying findings exist, state that no high-confidence actionable HIG
  defects were found and list the rendered surfaces and variants reviewed.

Do not test the safe-output tool or construct its payload with shell commands.
After the review body is final, invoke `submit_pull_request_review` exactly once
with that final body.

Do not edit code, create commits, push branches, create issues, or emit any other
safe output.
