# Repository stats

Every active `trsdn` repository can publish a self-hosted repository statistics card in its README. The reusable workflow in this repository renders static SVG files and commits them into the caller repository. No third-party statistics service or image proxy is used.

## Add the workflow

Copy `templates/repo-stats/stats.yml` to the target repository as `.github/workflows/stats.yml`:

```yaml
name: Repository stats

on:
  workflow_dispatch:
  schedule:
    - cron: "23 */6 * * *"

permissions:
  contents: write

jobs:
  stats:
    uses: trsdn/.github/.github/workflows/repo-stats.yml@main
    with:
      output-dir: .github/stats
      theme: both
      cards: repo-card
    secrets:
      STATS_TOKEN: ${{ secrets.STATS_TOKEN }}
```

For public repositories, the caller repository `GITHUB_TOKEN` is usually enough. For private repositories or higher API limits, create a fine-grained PAT and store it as `STATS_TOKEN`.

Required token access:

- Repository access: the target repository, or all repositories that should render cards.
- Permissions: `Contents: read and write` for committing SVGs.
- Permissions for private statistics: `Metadata: read` and repository read access. Add `Pull requests: read` and `Issues: read` if the repository is private and those counts must be included.

## Add the README snippet

Copy `templates/repo-stats/README-snippet.md` into the target README:

```md
<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/stats/repo-card-dark.svg">
  <img alt="Repository statistics" src=".github/stats/repo-card.svg">
</picture>
```

Use `<picture>` for light and dark mode. Do not rely on CSS `prefers-color-scheme` inside the SVG; GitHub serves images through Camo and does not consistently preserve that behavior.

## Reusable workflow inputs

| Input | Default | Meaning |
|---|---|---|
| `repository` | caller repository | Repository to render in `owner/name` form |
| `output-dir` | `.github/stats` | Output directory in the caller repository |
| `theme` | `both` | `light`, `dark`, or `both` |
| `cards` | `repo-card` | Reserved list of rendered card names |
| `commit-message` | `chore(stats): update repository stats` | Commit message when output changes |
| `branch` | caller ref | Branch to update |

The card includes repository name, description, commit count, latest commit, release information, release count, stars, forks, watchers, open issues, open PRs, contributors, language distribution, repository size, license, default branch, and 52 weeks of commit activity.

## Local rendering

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
export STATS_TOKEN="$(gh auth token)"
PYTHONPATH=scripts python -m profile_stats repo --repo trsdn/OpenLens --out out/openlens
```

## Troubleshooting

- If the workflow succeeds but the README image looks stale, GitHub Camo may be serving a cached copy. Open the raw SVG URL directly, wait a few minutes, or change the README image URL with a harmless query string such as `repo-card.svg?v=2`.
- If commits are not pushed, verify the workflow has `permissions: contents: write` and that branch protection allows GitHub Actions to push to the selected branch.
- If private repository counts are incomplete, use `STATS_TOKEN` with the fine-grained PAT permissions listed above.
- If commit activity is temporarily empty, GitHub may still be computing `/stats/commit_activity`. The client retries 202 responses, and the next scheduled run should fill the chart.
