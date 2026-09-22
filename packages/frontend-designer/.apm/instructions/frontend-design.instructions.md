---
applyTo: "docs/**,site/**"
---

<!-- markdownlint-disable MD041 -->

# Designing a site for this project

These rules exist so the result meets the Repository Quality Standard's `W01`,
`W02`, `W03`, `W04`, `W07`, `W08`, and `W09` — read as constraints on a design,
not as the design itself.

## Research before design

Do not open an editor before you can answer, in your own words and specific to
this product: what does it do, who is it for, and what is one true thing about
it that a generic project page would not say? If you cannot answer that third
question yet, keep reading the repository until you can — it is the thing that
makes the site belong to this project.

## The seven required items (W04)

Every one needs real content, not a placeholder:

1. Name and a one-sentence statement of what the project is — written from
   what you read, not copied verbatim from the README's own first line unless
   that line is already good.
2. Status (maintained, experimental, archived) and which release the page
   describes, or a link to the latest one.
3. What it does: a real screenshot if the product has a visual surface, a real
   usage example if it is a tool or library, or the shortest honest sentence if
   it has no visual or textual output at all.
4. How to get it or read it: the actual install command, download link, or
   entry point.
5. The privacy disclosure `Y01` requires. If the product collects or sends
   nothing, say exactly that in one sentence.
6. Links to the repository, the licence, the security policy, and how to get
   support.
7. The date the page was written or last reviewed.

## The landing order (W03)

Before any content but navigation: what the project is, who it is for, and its
status. In that order, in the page's source order — not merely visible, in the
markup, so `W03`'s test (reading the source) finds it.

## Design constraints, not a template

- No third-party resources: self-host fonts, images, and any script (`W07`).
  No analytics, no cookies.
- One page, unless there is a real reason for more.
- Colour, type, and layout must differ from an unmodified framework or
  component-library default in at least one deliberate way — and should differ
  in several, because one override that reads as an afterthought is a weak
  `Pass` at best. Explain the choice, even briefly, so it is visibly a decision
  and not a default nobody looked at.
- Never carry over another repository's site as a starting point unchanged.
  Looking at one for reference is fine; shipping its palette or layout
  unmodified is exactly what `W09` fails.

## What belongs in the repository, not the site (W08)

Contribution instructions, architecture writeups, decision records, the full
changelog, anything addressed to a contributor rather than a reader. If you
find yourself writing one of these into the site, stop and link to the
repository instead.

## Accessibility, in full

The site is a shipped interface, so the standard's `X01`-`X05` apply to it,
which in practice for a static page means: real contrast (not merely "looks
readable" — check actual colour values against text size), visible keyboard
focus on any interactive element, a legible type scale that works down to a
phone width, and no meaning conveyed by colour alone.
