# Workflow permissions and pinning

Serves [`S11`](../repository-quality-standard.md#s11) (declared, minimal token
permissions), [`S12`](../repository-quality-standard.md#s12) (references that
cannot change underneath you), and
[`S13`](../repository-quality-standard.md#s13) (untrusted triggers cannot read
secrets).

## Permissions

A workflow that declares no `permissions` gets the account default, which is
often write-capable. Declare a block at the top of every workflow, start with
`contents: read`, and add to it on the job that needs more.

```yaml
permissions:
  contents: read

jobs:
  analyze:
    permissions:
      actions: read
      contents: read
      security-events: write
```

A job-level block replaces the workflow-level one for that job, so restate
`contents: read` there. A called reusable workflow can hold no more than its
caller grants.

| Job | Permissions it needs |
|---|---|
| Build, lint, test | `contents: read` |
| Secret scan | `contents: read` |
| CodeQL analysis | `contents: read`, `actions: read`, `security-events: write` |
| Conformance check | `contents: read` |
| Commit a generated file back | `contents: write`, on that job only |
| Create a release and upload assets | `contents: write`, on that job only |
| Publish to PyPI, npm, or NuGet with trusted publishing | `id-token: write` and `contents: read`, on the publishing job only |
| Deploy to GitHub Pages | `pages: write` and `id-token: write`, on the deploy job only |
| Comment on a pull request | `pull-requests: write`, on that job only |
| Upload an artifact | Nothing beyond `contents: read` |

Never write `write-all`. A write scope that no step in the job uses is not
minimal either.

## Pinning

A tag can be moved to different code after you reviewed it, and what a workflow
runs is whatever it points at that day. The standard asks for a commit SHA only
where a moved tag could reach something.

| Reference | Job holds a secret or can write | Job is read-only, no secret |
|---|---|---|
| Published by GitHub (`actions/*`, `github/*`) | Major-version tag | Major-version tag |
| Outside the account | SHA, or a recorded reason for a tag | Major-version tag is enough |
| Your own account, including shared workflows | Branch is allowed | Branch is allowed |

Publishing and release jobs are the usual case for a SHA, for example
`pypa/gh-action-pypi-publish`, `NuGet/login`, `peaceiris/actions-gh-pages`, and
`peter-evans/create-pull-request`. `@main` on `trsdn/.github/...` needs no pin.

Write the version as a trailing comment, so a reader and Dependabot can see what
the SHA means:

```yaml
- uses: lycheeverse/lychee-action@e7477775783ea5526144ba13e8db5eec57747ce8 # v2
```

A reason for a tag goes on that line or the one above it:

```yaml
# Tag accepted: read-only token, no secret in this job.
- uses: some-org/some-action@v3
```

### Looking up a SHA

For a lightweight tag, the ref points straight at a commit. For an annotated
tag, the ref points at a tag object, and the commit is one step further on.
Asking for the commit by tag name resolves both cases:

```sh
gh api repos/OWNER/REPO/commits/TAG --jq .sha
```

Or read the ref and dereference if needed:

```sh
gh api repos/OWNER/REPO/git/ref/tags/TAG --jq '.object.type + " " + .object.sha'
```

If the type printed is `tag`, fetch the object it names and use its `object.sha`:

```sh
gh api repos/OWNER/REPO/git/tags/SHA_FROM_ABOVE --jq .object.sha
```

Use the commit SHA, never the tag object's. A SHA copied from a pull request or a
fork can belong to a commit that is not in the action's own repository, so take
it from the action's own repository as above.

### Keeping SHAs current

A pinned SHA never updates on its own. The `github-actions` entry in
`dependabot.yml` proposes a pull request when the tag it was pinned from moves,
and updates the comment. Group the entries, so one pull request carries all of
them. See the [Dependabot guide](dependabot.md).

## Untrusted triggers

`S13` is about workflows started by content a contributor controls, chiefly
`pull_request_target` and `workflow_run`. Do not run code from the pull request
in those, and do not give them secrets. A repository that uses neither trigger
is not affected, and its assessment says so. `pull_request` from a fork already
runs without secrets.

## Worked example

The [Node kit's CI](../../templates/node/.github/workflows/ci.yml) declares
`contents: read` once for the whole workflow and uses GitHub-published actions by
major tag. The [documentation kit's link check](../../templates/docs/.github/workflows/links.yml)
uses an outside action, which is pinned by SHA with a `# v2` comment. Its job is
read-only, so a tag would also pass, and it shows the form. The
[.NET CodeQL workflow](../../templates/dotnet/.github/workflows/codeql.yml)
raises `security-events: write` on its one job.
