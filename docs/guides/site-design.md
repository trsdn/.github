# Designing a published site

Since [1.21.0](../repository-quality-standard.md#published-sites), a public
repository shipping an application, game, or command-line tool a non-developer
installs by name must publish a site — [decision
0020](../decisions/0020-public-applications-need-a-site.md). This guide is how,
and it is deliberately not "run one tool and get a compliant site."

## Design is not automatable the way a licence notice is

[`readme-writer`](https://github.com/trsdn/.github/issues/82) and
[`notices-writer`](https://github.com/trsdn/.github/issues/84) (tracked, not yet
built) are candidates because their output is mostly facts arranged in a known
shape. A site's design is not that: [decision
0013](../decisions/0013-sites-are-designed-not-templated.md) retired this
account's own shared design language because nine unrelated products sharing
one look told a visitor nothing about any of them. A design tool that is not
told to look closely at the specific product it is building for reproduces that
exact failure — it just becomes a new, invisible default instead of the old
one.

So this account's site tooling is two agents with two different jobs, not one:

| Agent | Job | Package |
|---|---|---|
| **Designer** | Reads the repository and the product, then writes a site made for it | [`frontend-designer`](../../packages/frontend-designer/README.md) |
| **Reviewer** | Checks the mechanical parts against the standard, and holds the line that design taste is out of scope | [`site-content-reviewer`](../../packages/site-content-reviewer/README.md) |

Both are local, versioned Agent Package Manager packages, run on request, never
in CI.

## The process

1. **Research first.** Whether by hand or by asking `frontend-designer` to do
   it, the question to answer before writing any markup is: what is one true
   thing about this specific product that a generic project page would not
   say? If you cannot answer it, keep reading the repository — the README, the
   source, existing screenshots or icons, the product's own voice — until you
   can.
2. **Design deliberately.** Colour, type, and layout follow from what you read
   in step 1. If you are working interactively, a live-preview tool (this
   account's own `Artifact` capability, or an equivalent in your own agent
   runtime) is worth using to look at the page as you go, the way you would
   look at a page a colleague showed you rather than trust markup alone.
3. **Cover the required content.** The seven items in [Site Content
   Baseline](../repository-quality-standard.md#site-content-baseline), with
   real content, not placeholders.
4. **Self-host everything.** No font CDN, no icon service, no analytics
   (`W07`). Keep contributor-facing material — architecture, decisions, the
   full changelog — in the repository, not the site (`W08`).
5. **Check the mechanics.** Run `site-content-reviewer` (or check by hand)
   before publishing: `W01`-`W04`, `W07`, `W08`, and `W09`'s three enumerated
   Fail cases.
6. **Look at it yourself before committing.** A generated draft is a strong
   starting point, not a finished site. Check that the voice actually sounds
   like the product and that nothing reads as though it could describe any
   other project equally well.

## What "good enough" means here

`W09` itself states that whether a design is *good* is taste, and out of scope
for the standard: a page that is not one of the three enumerated Fail cases (no
stylesheet, an unmodified framework theme, another project's site copied) is a
`Pass`, plain or not. Use `frontend-designer` to aim higher than the floor —
that is the whole reason it researches the product first — but the standard
itself only asks for the floor.

## A site for a repository that does not have one yet

The fastest path from nothing to compliant: install and run
`frontend-designer` from a `trsdn/.github` checkout, look at what it produced,
adjust the parts that do not yet sound like the product, run
`site-content-reviewer`, then commit and set the repository's homepage field.
