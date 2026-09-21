# Writing the first conformance record

For a repository with no `.github/conformance.yml`. The record format is in
[Conformance Record Format](../docs/conformance-record.md) and the drafting tool
is described in [Drafting a conformance record](../docs/assessing.md). This page
is the order to do it in, and does not repeat either.

## Steps

1. Check out `trsdn/.github` beside your repository, or copy `scripts/assess.py`.
   It needs Python 3 and nothing else.
2. Draft the record from what the GitHub API shows:

   ```sh
   python3 scripts/assess.py --repo OWNER/REPO --out drafts/REPO
   ```

   This writes `conformance.yml` and `assessment.md`. It settles only the
   criteria a single fact decides and leaves the rest `unknown`.
3. Decide every remaining criterion yourself, or have an agent do it. Read the
   evidence, then choose `pass`, `partial`, `fail`, or `na`. A `na` needs a
   stated reason as much as a failure does. The
   [defaults for deciding without a maintainer](../docs/repository-quality-standard.md#deciding-without-the-maintainer)
   say what to do where the evidence is silent.
4. Rewrite `assessment.md` as the evidence: one short note per criterion that is
   not a plain `pass`, saying what you saw. Save it as `docs/assessment.md` and
   point `evidence` at it.
5. Replace the `assessed_on` placeholder with today's date in UTC
   (`date -u +%F`), and set `state` from the
   [Assessment](../docs/repository-quality-standard.md#assessment) rules.
6. Copy the record to `.github/conformance.yml`.
7. Add the caller so the record is checked and the badge is generated from it:

   ```yaml
   name: Conformance

   on:
     push:
       branches: [main]
     pull_request:
       branches: [main]
     workflow_dispatch:

   permissions:
     contents: read

   jobs:
     conformance:
       uses: trsdn/.github/.github/workflows/conformance.yml@main
   ```

8. Add the `trsdn-standard` repository topic so the repository can be found as
   part of the assessed set ([`B12`](../docs/repository-quality-standard.md#b12)).
   That is a repository setting, so it is a maintainer action.

## Checking the badge against the record

The conformance badge follows the record and the check in step 7 fails when they
disagree. That covers one badge of the
[badge convention](../docs/repository-quality-standard.md#status-badges)
([`P08`](../docs/repository-quality-standard.md#p08)). A badge whose value you
typed, such as a runtime version, needs its own check, or it should be replaced
by a badge that reads the value itself. A check for a hand-typed version badge:

```yaml
- name: README badge matches the manifest
  run: |
    want=$(grep -oP '"node": *"\K[^"]+' package.json | head -n1)
    grep -q "node-${want}" README.md || {
      echo "README node badge does not say ${want}" >&2
      exit 1
    }
```

Put it in a CI job that already has `permissions: contents: read`. Adapt the
manifest field and badge text to the value you typed.

## Keeping it true

The record ages. Reassess when the standard's version changes or the review
cadence in the record format runs out, and change the record only after the
evidence changes.
