# README snippet for repository stats

Copy the block below into the README of a repository that runs the
[repository stats workflow](../../docs/repo-stats.md). Adjust the paths if the
workflow writes to a directory other than `.github/stats`. Showing this card is
the README evidence for criterion `P09`.

The `<picture>` element is required: GitHub serves README images through its
image proxy, so a `prefers-color-scheme` media query inside the SVG itself has
no effect. Two separate files and a `<source>` element are what make the theme
switch work.

```markdown
## Repository stats

<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/stats/repo-card-dark.svg">
  <img alt="Repository statistics" src=".github/stats/repo-card.svg">
</picture>
```
