# 0004 - Language and localization

- Status: Accepted
- Date: 2026-08-22

## Context

The maintainer works in German; the repositories are public and read
internationally. Nothing recorded which language a product should present, so it
was decided per repository by habit, and some repositories mixed both.

## Decision

English is the default for user-facing surfaces. Localization is optional but
never implicit: a repository declares either English-only or an explicit list of
supported locales. An undeclared language fails `L01`.

Repository and contributor surfaces — README, docs, comments, identifiers, commit
messages, issues, pull requests, release notes — are English in all cases,
including in repositories whose product is not English. The product language and
the contributor language are separate decisions.

Repositories whose subject matter is inherently German declare German as their
primary user-facing language with a one-sentence rationale. The exception covers
the product surface only.

## Consequences

Existing German-content repositories need a one-line README declaration to pass
`L01`. That is the intended cost: the declaration is what makes the choice
visible.

## Alternatives considered

**Require English everywhere with no exception.** Rejected. A German archival or
genealogy project presenting itself in English serves nobody.

**Leave language unspecified.** Rejected. That is the status quo, and it produced
repositories that mix languages within a single interface.

**Require a minimum set of localized languages.** Rejected. Translations that
nobody maintains are worse than an honest English-only product.
