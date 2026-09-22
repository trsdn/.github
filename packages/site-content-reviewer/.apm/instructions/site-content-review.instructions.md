---
applyTo: "**/*.html,**/*.css"
---

<!-- markdownlint-disable MD041 -->

# Site content review

Apply the Repository Quality Standard's exact tests for `W01`-`W04`, `W07`,
`W08`, and `W09`'s three enumerated Fail cases. Every test below has a concrete
answer from reading the source; none of them is a matter of opinion.

## W01 — publishing process

Look for one of: a GitHub Actions workflow that builds or copies site files, a
Pages source configured to a branch and folder (`gh api
repos/OWNER/REPO/pages`), or a documented build script. Then look for one
sentence, anywhere in the README, `AGENTS.md`, or `docs/`, saying how the site
is published. Both parts present is `Pass`; one is `Partial`; neither is
`Fail`. If the site's source is not in this repository at all, it is `Not
applicable`.

## W02 — the link both ways

Repository → site: the homepage field is set and matches the site's URL. Site →
repository: a link to the repository appears on every page in a persistent
element (header, nav, or footer), or anywhere on the page for a single page.
One direction is `Partial`.

## W03 — the landing statement

Read the landing page's HTML source in order. Before any content other than
navigation, three things must appear: a statement of what the project is, who
it uses it (its audience), and a status word (maintained, experimental,
archived). All three in order is `Pass`.

## W04 — Site Content Baseline

Check each of the seven items for presence, not quality:

1. Name and one-sentence purpose.
2. Status and version, and which release the page describes (or a link to the
   latest release).
3. What it does — a screenshot, example, or sample; or, for a product with no
   visual or textual output, its shortest honest statement.
4. How to get it or read it.
5. The `Y01` privacy disclosure — one sentence is enough, including "nothing is
   collected."
6. Links to the repository, licence, security policy, and support.
7. The date the page was generated or last reviewed.

All seven present is `Pass`. At least one, fewer than seven, is `Partial`. None
is `Fail`.

## W07 — no third parties

Search the landing page's source (and any stylesheet it loads) for references
to another host: `<link href="https://...">`, `<script src="https://...">`,
`@import url(...)`, CSS `url(...)`, and `<img src="https://...">`. The site's
own host does not count. A link a visitor clicks through to another page is not
a loaded resource. Also search for cookie-setting code (`document.cookie`) and
analytics snippets (Google Analytics, Plausible, or similar identifiers). None
found is `Pass`.

## W08 — no restatement

A section titled or clearly about contributing, architecture, decisions, or a
full changelog is a `Fail` outright — that content belongs in the repository,
not on the site. Separately, check any command, version number, or policy
statement that also appears in the README or `docs/`: if the site version links
to that source rather than restating it, it is fine; if it restates without a
link, it is a `Partial` regardless of whether the two copies currently agree —
the same fact in two places is the defect the standard is testing for here,
independent of `B13`'s "does it still agree" test elsewhere.

## W09 — the three enumerated Fail cases only

Read the stylesheet or theme configuration. `Fail` only for: no stylesheet
exists; a framework or template theme is used with zero overrides to colour,
type, or layout; or the CSS and assets are another project's site, copied
unchanged (compare against other sites in this account if you have access to
more than one). Anything else — including a plain, minimal, but intentionally
authored page — is `Pass`. Never report a `Fail` or a note based on aesthetic
preference; the standard is explicit that whether a design is good is out of
scope for this criterion.
