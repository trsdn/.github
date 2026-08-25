# Profile statistics

The profile statistics generator renders GitHub account cards as static SVG
files. It is self-hosted: GitHub Actions collects data through the GitHub API,
renders SVG strings locally, and commits the output back to the repository. It
does not call `github-readme-stats`, Shields, Vercel, Leapcell, headless
browsers, external fonts, or remote images.

## Architecture

The Python package lives in `scripts/profile_stats/` and runs on Python 3.12 or
newer.

| Module | Responsibility |
|---|---|
| `github_api.py` | GraphQL and REST client, pagination, timeouts, and retry/backoff for rate limits |
| `collect.py` | Repository and account aggregation |
| `models.py` | Dataclasses for collected data |
| `render/` | SVG rendering, themes, primitives, escaping, and formatting |
| `languages.py` | Embedded GitHub language colors; no runtime network fetch |
| `config.py` | Restricted YAML configuration defaults and validation using the standard library |
| `cli.py` | `argparse` CLI for `repo` and `account` commands |

The default account workflow is `.github/workflows/profile-stats.yml`. It runs
every six hours, on manual dispatch, and after changes to the generator on
`main`. It renders into `assets/profile-stats` and publishes the result to the
`stats` branch, and only when a generated SVG actually changed.

## Cards

Account mode renders light and dark variants for:

- `overview-card.svg`: total commits, stars, merged PRs, authored issues, code
  reviews, followers, active repositories, and streaks.
- `activity-card.svg`: last twelve months of contributions, current streak, and
  longest streak.
- `language-card.svg`: weighted language distribution by bytes across non-fork
  repositories.
- `repos-table-card.svg`: recently active repositories with stars, commits, last
  commit, release, issues, and primary language.
- `now-building-card.svg`: three most recently changed repositories and their
  latest commit messages.

Dark mode is selected in Markdown with `<picture>` and a dark `<source>`. GitHub
serves SVGs through Camo; CSS `prefers-color-scheme` media queries inside an SVG
are not reliable there, so each theme is rendered as a separate SVG file.

## Configuration

Edit `scripts/profile_stats/config.yml`:

```yaml
username: trsdn
top_n: 12
include_private: false
repo:
  include: []
  exclude: []
cards:
  account:
    - overview
    - activity
    - language
    - repos-table
    - now-building
```

`include_private: true` requires a token that can read the private repositories
being counted. The workflow reads `secrets.STATS_TOKEN` when present and falls
back to `GITHUB_TOKEN`.

## Local usage

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
export STATS_TOKEN="$(gh auth token)"
PYTHONPATH=scripts python -m profile_stats account --username trsdn --out assets/profile-stats
```

`requests` is the only runtime dependency installed by `requirements.txt`. The
renderer validates every SVG with `xml.etree.ElementTree` before writing it.
Dynamic strings are XML-escaped, control characters are stripped, and SVG output
does not use `<script>`, `<foreignObject>`, external fonts, or external images.

## Profile README

GitHub renders [`profile/README.md`](../profile/README.md) from this repository
on the `trsdn` account profile, so no separate `trsdn/trsdn` repository is
needed.

That page embeds the account cards from raw URLs pinned to the `stats` branch
rather than from `main`. The reason is branch protection: `main` rejects pushes
from `GITHUB_TOKEN`, so a workflow that committed generated cards to `main`
would fail with `GH006`. Publishing to a separate generated branch keeps the
protection rule intact and keeps generated output out of the reviewed history.

The `stats` branch is force-pushed on every run and holds no reviewed content.
Never base work on it.
