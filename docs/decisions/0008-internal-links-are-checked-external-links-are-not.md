# 0008 - Internal links are checked, external links are not

- Status: Accepted
- Date: 2026-08-29

## Context

`T02` asks that internal links and generated output be validated where
practical. Generated output was already covered: `scripts/standard.py` proves the
catalog matches the document, and `scripts/conformance.py` proves the badge
matches the record. Links were not covered at all.

The gap mattered more here than it would in most repositories. This repository
publishes a standard whose criteria are addressed as `#s05` and cited by pinned
URL from other repositories and from issues. Renaming a heading invalidates every
one of those citations, and nothing in the toolchain noticed. The documentation
set also cross-references heavily between the standard, the record format, the
decisions, and the templates.

## Decision

`scripts/links.py` validates relative link targets and anchors across every
Markdown file in the repository. Anchors come from both heading slugs and
explicit `<a id>` elements, because the standard's criteria are addressed by the
latter and no heading exists for them.

External links are deliberately out of scope.

Fenced code blocks are excluded. The documentation shows example Markdown whose
paths exist in the repository the example is written for, not in this one, and
treating those as links would make the check cry wolf.

## Consequences

Checking external links would need the network on every run. It would fail when
a third-party site is briefly down, rate-limits CI, blocks the runner, or moves a
page that still resolves for a human through a redirect chain. Those failures
would be indistinguishable from a real defect, and a check that fails for reasons
outside the repository is a check people learn to click past. Once a check is
routinely ignored, it is worse than absent, because it still renders green
authority when it happens to pass.

Internal links are fully decidable from the checkout. A failure is always a real
defect, so the check can be required without ever being a nuisance.

The cost is accepted: a link to a page that has moved on someone else's site will
rot undetected. That is a documentation-review problem, not a CI problem, and
`T02` says *where practical*.

The slug algorithm approximates GitHub's rather than reimplementing a Markdown
parser. It is close enough to catch renamed headings, which is the failure this
exists to prevent, and simple enough to reason about. A heading whose slug the
approximation gets wrong would produce a false positive, which is visible and
fixable, rather than a false negative, which is not.
