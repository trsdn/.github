# Hi, I'm Torsten

I build small, focused macOS tools and developer tooling — things that do one job
and stay out of the way. Most of it is open source under MIT.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/trsdn/.github/stats/assets/profile-stats/overview-card-dark.svg">
  <img alt="GitHub account overview" src="https://raw.githubusercontent.com/trsdn/.github/stats/assets/profile-stats/overview-card.svg">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/trsdn/.github/stats/assets/profile-stats/activity-card-dark.svg">
  <img alt="Contribution activity over the last twelve months" src="https://raw.githubusercontent.com/trsdn/.github/stats/assets/profile-stats/activity-card.svg">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/trsdn/.github/stats/assets/profile-stats/language-card-dark.svg">
  <img alt="Language distribution across repositories" src="https://raw.githubusercontent.com/trsdn/.github/stats/assets/profile-stats/language-card.svg">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/trsdn/.github/stats/assets/profile-stats/repos-table-card-dark.svg">
  <img alt="Recently active repositories" src="https://raw.githubusercontent.com/trsdn/.github/stats/assets/profile-stats/repos-table-card.svg">
</picture>


## How these cards work

They are not fetched from a statistics service. A scheduled workflow in
[`trsdn/.github`](https://github.com/trsdn/.github) queries the GitHub API,
renders plain SVG, and commits the result to that repository's `stats` branch.
No third party observes anybody who visits this page.

The same generator publishes a per-repository card that any of my repositories
can call. Both are described in
[Repository stats](https://github.com/trsdn/.github/blob/main/docs/repo-stats.md)
and [Profile stats](https://github.com/trsdn/.github/blob/main/docs/profile-stats.md).
The requirement behind them is criterion `P09` of my
[Repository Quality Standard](https://github.com/trsdn/.github/blob/main/docs/repository-quality-standard.md).
