# README snippet for repository stats

Copy the block below into the README of a repository that runs the
[repository stats workflow](../../docs/repo-stats.md). Showing this card is the
README evidence for criterion `P09`.

Where the workflow commits to the default branch, the relative paths in the first
block work. Where it commits to a separate `stats` branch, as the workflow guide
recommends for a protected default branch, a relative path resolves against the
default branch and shows nothing, so use the second block with absolute
`raw.githubusercontent.com` URLs. Replace `OWNER/REPO`, and the directory if the
workflow writes somewhere other than `.github/stats`. The image is broken until
the workflow has run once, because the files do not exist before then.

The `<picture>` element is required: GitHub serves README images through its
image proxy, so a `prefers-color-scheme` media query inside the SVG itself has
no effect. Two separate files and a `<source>` element are what make the theme
switch work.

Default branch:

```markdown
## Repository stats

<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/stats/repo-card-dark.svg">
  <img alt="Repository statistics" src=".github/stats/repo-card.svg">
</picture>
```

Separate `stats` branch:

```markdown
## Repository stats

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/OWNER/REPO/stats/.github/stats/repo-card-dark.svg">
  <img alt="Repository statistics" src="https://raw.githubusercontent.com/OWNER/REPO/stats/.github/stats/repo-card.svg">
</picture>
```
