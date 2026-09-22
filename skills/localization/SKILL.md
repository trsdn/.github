---
name: "localization"
description: "Checks localization catalogs for missing, unfinished, and orphaned keys, and guides the German and English disclosure the Language criteria ask for. Covers L01 to L07 of the trsdn Repository Quality Standard, and provides the validation command L04 requires. Use when a product ships more than one language, when adding a locale, or before a release that changed user-facing strings."
---

<!-- markdownlint-disable MD041 -->

## What this is for

A string catalog drifts silently. A new feature adds ten English strings, the
German translations follow a week later or never, and nothing fails — the app
just shows English in the middle of a German window. `L04` exists for that, and
it asks for a command, which is what this provides.

## How to use it

```sh
python3 scripts/catalog-check.py --path /path/to/checkout --locales de,en
```

It exits non-zero when a catalog is incomplete, so **this is the `L04`
validation command**: document it in the README as the check, and run it before a
release. It needs no runner, so it satisfies the criterion in a private
repository too.

It reads `.xcstrings` catalogs (including the translation state Xcode records),
`.lproj/*.strings` compared against the development language, and locale JSON
under `locales/`, `i18n/` or `lang/`. `--json` gives machine-readable output.

It reports four things:

- **missing** — the key exists in the source language and not in that locale
- **unfinished** — a translation exists but Xcode marks it new, needs review, or
  stale. Present is not the same as done
- **orphaned** — a translation whose source string is gone
- **declared but absent** — a locale `L03` claims that the catalog carries
  nothing for. That is the claim and the reality disagreeing, and it is the one
  a reader cannot see

## German and English

For a product shipping both, the criteria come apart like this:

**`L01` and `L07` are about different audiences and pull in different
directions.** `L01` is the *product's* primary language. `L07` is the
*repository's*: README, `docs/`, code comments, identifiers, commit messages,
issues and pull requests are English, so a contributor who does not read German
can work on it. Both can be true at once, and for a German-language product they
must be: German in the interface, English in the source.

This is the easiest one to get wrong when the maintainer is a German speaker,
because the slip is invisible to the person making it. Worth checking German has
not leaked into an identifier, a commit message, or a code comment.

**`L03` declare the list.** One line in the README: *"Interface available in
English and German."* Then pass the same list to `--locales`, so the claim is
checked rather than trusted.

**`L02` no hardcoded strings.** Every user-facing string comes from the catalog.
A German literal in the source is both a `L02` failure and a string that can
never be translated.

**`L05` platform locale APIs.** Dates, numbers, currency and sorting go through
the platform's formatter, not string interpolation. German date order, decimal
comma, and umlaut sorting all come free from the API and are all wrong when hand
built. This needs reading the source; the catalog check does not see it.

**`L06` traceability.** A translation should be traceable to its source string
and to where it came from — a person, a service, or a model. `.xcstrings` keeps
the source string as the key, which covers half of it; say in the README or a
translation note how the translations are produced, which covers the rest.

## Rules

- **Run it before a release, not after.** A missing translation found after a
  build is a release you cannot ship without another one.
- **Never machine-translate silently.** If translations come from a model, `L06`
  wants that said. A user is entitled to know why a sentence reads oddly.
- **Never delete an orphan to clear the check.** Find out whether the source
  string was renamed, which makes it a translation to move, not to bin.
- **Never commit.** Leave catalog changes in the working tree for review.
