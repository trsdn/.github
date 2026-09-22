# 0024 - A site designer researches before it writes

- Status: Accepted
- Date: 2026-09-22

## Context

[Decision 0013](0013-sites-are-designed-not-templated.md) retired this
account's shared design language, Instrument Workshop, because uniform sites
for unrelated products told a visitor nothing any of them individually. An
unattended agent that designs many sites without looking closely at each one
risks the identical failure: it converges on its own default palette and
layout, which is Instrument Workshop again with one more author and no name for
it.

The maintainer's view, and the one this decision adopts, is that this is not a
reason to keep site design manual. A designer that genuinely researches the
specific repository and product first — what it does, who it is for, what its
own voice already sounds like — before choosing a colour can produce work made
for that project, the same way a good human designer does. The risk is real but
is a property of skipping research, not a property of using an agent at all.

## Decision

Publish two packages instead of one. `packages/frontend-designer` is a writer:
it reads the repository and the product before it designs anything, is
instructed explicitly to notice and avoid repeating a look it has already
produced, writes the site into the working tree, and never commits or opens a
pull request itself — the operator reviews a generated site exactly as they
would review a colleague's draft. `packages/site-content-reviewer` is a
read-only reviewer that checks only what the standard can decide as fact
(`W01`-`W04`, `W07`, `W08`, and `W09`'s three enumerated Fail cases) and
explicitly does not comment on design taste, holding the same boundary `W09`'s
own text draws.

Splitting them keeps the judgement-free check separate from the creative one:
a reviewer that also tried to judge taste would either invent a standard nobody
agreed to or rubber-stamp whatever the designer produced.

## Consequences

- A repository can get from nothing to a standard-compliant, project-specific
  site with one agent run and one review pass, instead of the site being the
  reason a repository stays out of compliance.
- The designer's output still needs a human look before it is trusted: the
  package's own README says so, and nothing in `site-content-reviewer` checks
  whether the result is actually good, only whether it clears the standard's
  floor.
- If sites produced this way start to look alike despite the instruction not
  to, that is evidence the research step is not being followed and the package
  needs sharper instructions, not evidence that design should go back to being
  unassisted.
