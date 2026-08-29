# 0009 - Published sites carry the shared design language, and each fact has one home

- Status: Accepted
- Date: 2026-08-29

## Context

Nine public repositories in the estate already publish a GitHub Pages site.
Three of them — `about-me`, `ai-scrum`, and `mdviewerplus-windows` — have Pages
enabled and no homepage link set on the repository, so a visitor who arrives at
the site has no supported route back to the source, and a visitor who arrives at
the repository cannot tell a site exists. Nothing in the standard said anything
about any of this. Sites were being published, and how they looked, what they
said, and whether they connected back to anything was decided nine separate
times.

The second problem is older and quieter. A repository accumulates surfaces: the
description, the README, `docs/`, decision records, the changelog, `AGENTS.md`,
and now a site. Each new surface invites restating what the previous one already
said, because restating is easier than deciding where something belongs. This
repository was doing it: the six validation commands were listed verbatim in both
`README.md` and `AGENTS.md`, and adding two checks required editing both copies
on the same day.

Adding a site to a repository that already restates itself makes the problem
structural rather than occasional, so both are settled together.

## Decision

The `Published Site` profile and criteria `W01`-`W08` apply to any repository
that publishes a site, or whose audience includes people who will never open the
repository.

Sites use Instrument Workshop, the shared design language, and record the version
they were built against. Instrument Workshop is consumed by copying two
stylesheets into the site, not by referencing the design system repository at
build time.

`B13` and the `Content Boundaries` section state that each fact has exactly one
home, and that other documents link to it rather than restate it. Generated
restatement is explicitly exempt.

## Consequences

**Vendoring the design language.** The design system repository is private, so a
public site cannot resolve it at build time — a submodule, a package install, or
a CI checkout would all need credentials that a public Pages build does not have.
Copying is the documented consumption path and needs no build step, no package
manager, and no JavaScript.

The cost is that the first public site to satisfy `W05` also publishes the design
language, because the stylesheets ship in the open. That is acceptable: a design
language is meant to be seen, its value is in consistency rather than secrecy,
and every site built from it is already a rendering of it. It is recorded here
because it is a disclosure that happens as a side effect of a technical
constraint, and side effects nobody wrote down are the ones that surprise people.

The second cost is drift. A copied stylesheet does not update when the source
does, which is exactly why `W06` requires the version to be recorded: an
out-of-date copy is tolerable, an out-of-date copy that nobody can date is not.

**Sites load nothing from third parties.** No font CDN, no analytics, no embedded
widgets. This follows the reasoning already applied in `P09` and `Y02`: a
third-party request discloses a visitor's address and user agent to a party the
visitor never chose, and it turns someone else's uptime into a dependency of
your project looking maintained.

**Boundaries create work before they save it.** Splitting a duplicated passage is
more effort than leaving both copies, and the payoff is invisible — it is a
future contradiction that never happens. The rule is worth the cost because the
failure mode is silent: nothing breaks when two copies disagree, and both keep
reading as authoritative, so the reader who follows the stale one has no signal
that they were misled.

**Generated restatement stays allowed.** A badge restates a record, a statistics
card restates an API, and a catalog restates a document. None of them can drift,
because none of them is edited by hand and each has a check that fails when it
disagrees with its source. The rule targets hand-maintained restatement, which is
the only kind that rots.

**This repository fails its own new criteria.** The Published Site profile applies
here, no site exists, and the state returns from `Healthy` to `Needs work` the
same day it was earned. Exempting the repository that writes the standard would
have been the cheaper option and would have made every other assessment
negotiable.
