# 0009 - Published sites carry the shared design language, and each fact has one home

- Status: Accepted
- Date: 2026-08-29
- Amended: 2026-08-30 (standard 1.5.0)

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
that publishes a site, or that ships something whose audience uses it without
ever needing the repository.

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

Copying is expressly permitted, which was settled after this record was first
written. The consequence is that the design language becomes visible in every
public site built from it, because the stylesheets ship in the open. That is
accepted: a design language earns its value from consistent use rather than from
being hidden, and every site built from it is already a rendering of it.

The cost that remains is drift. A copied stylesheet does not update when the source
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

**The profile does not apply to this repository.** The trigger as first written
asked whether the audience "includes readers who will never open the repository",
which caught any document, including this specification, and this repository was
recorded as eight failures for one day. Standard 1.5.0 narrowed it to ask whether
the repository ships something an audience uses without needing the source.

A specification is applied *to* repositories by people who are already inside
one. Putting a page in front of it adds a surface to maintain and answers nothing
its readers were asking. The repositories the standard is applied to are the ones
that ship products, and that is where `W01`-`W08` do their work — nine of them
already publish a site, which is what prompted this record in the first place.

The versioning table had no row for a narrowing of this kind. One was added:
narrowing a profile's applicability is minor, because no recorded `Pass` can turn
into a `Fail`.
