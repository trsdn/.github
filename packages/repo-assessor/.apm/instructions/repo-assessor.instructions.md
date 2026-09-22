---
applyTo: "**"
---

# Repository assessment and remediation issues

Every issue you file follows the Remediation Issue Contract from
`docs/repository-quality-standard.md` in the `trsdn/.github` checkout, verbatim.
Read it there; this restates only the shape so you do not have to look it up for
every issue.

## Issue shape

- **Title**: the criterion ID(s) and the gap in one line, for example "I02/I03:
  published v1.2.0 artifact is missing repository and licence metadata". A
  reader searching by criterion ID must find it.
- **Criterion**: link each criterion ID to its anchor in the standard, in the
  pinned form the standard requires — `https://github.com/trsdn/.github/blob/v<assessed
  version>/docs/repository-quality-standard.md#i02`, naming the version you
  assessed against. A relative path resolves to nothing in another repository's
  issue, and a link to the default branch changes underneath the citation. State
  the observed gap in
  concrete terms: what you read, in which file or setting, and how it disagrees
  with the requirement. Quote the actual content where that is the clearest
  evidence, not a paraphrase of the rule.
- **Required content**: what has to exist or change, specific enough that
  whoever picks up the issue does not have to re-derive it from the criterion
  text. Name the file, the setting, or the command, not only "add security
  documentation."
- **Expected evidence**: what a reader (or the next assessment) checks to
  confirm the gap is closed: a file, a green workflow run, a release asset, a
  repository setting read a specific way.
- **Done when**: concrete acceptance criteria, phrased so a yes/no answer is
  possible without asking the maintainer anything further.
- **Exclusions**: what must not change. Name the working code or configuration
  the fix must leave alone, especially where your assessment already confirmed
  it is correct — this stops a fix from touching something that was never
  broken.

## Deciding without the maintainer

Apply the standard's own rule, in the order it gives:

1. The requirement is met as written: record `Pass`, file nothing.
2. The property is met by other means than the evidence column names: `Pass`,
   with the means noted for your own report; file nothing.
3. A reason from the standard's closed list of intended-deviation reasons
   applies, and you checked that the reason holds: record the result the
   standard's table gives for that reason. A `Partial` recorded this way still
   gets an issue if the standard's own text does not excuse it — read the
   "Deciding Without The Maintainer" section for which is which.
4. Otherwise the gap is real: `Partial` where part of it is met, `Fail` where
   none of it is. File the issue.

Never invent a reason not in the standard's list, and never soften a `Fail` to a
`Partial` because fixing it looks like a lot of work — the result follows the
evidence, not the size of the fix.

## Multi-part and default results

A criterion the standard does not give its own boundary for follows the default
rule in "Deciding Without The Maintainer": every part met is `Pass`, some is
`Partial`, none is `Fail`; `Not applicable` where the repository has nothing the
criterion is about, recorded with what you looked for.

## De-duplication

Before filing, search: `gh issue list --repo OWNER/NAME --search "<criterion ID>
in:title,body" --state all --limit 20`. Every `gh` command carries
`--repo OWNER/NAME`, because you are running from the `trsdn/.github` checkout
and an unscoped command would act on that repository instead. An open issue
citing the same criterion ID is not
duplicated — read it, and comment only if your assessment found something the
issue does not already say. A closed issue citing the criterion ID that the
current assessment still finds failing is neither reopened nor refiled: a
maintainer closed it, and reversing that is their decision, not yours. Record it
and give the operator the number.

## What stays out of an issue

Data the operator has not shared publicly: credentials, internal URLs, personal
information, anything from a private repository's content beyond what the issue
needs to describe the gap. If the repository is private, the issue can still be
private (filed on that repository), but never copy private content into a public
one.
