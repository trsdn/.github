---
name: "privacy-disclosure"
description: "Finds what a product talks to, stores, and reports — outbound hosts, telemetry and crash SDKs, AI providers, local storage — and helps write the disclosure the Data Protection criteria ask for. Covers Y01 to Y06 of the trsdn Repository Quality Standard. Use when an app, CLI, or service handles user data or contacts a network service, or when a privacy note needs writing or checking."
---

<!-- markdownlint-disable MD041 -->

## What this is for

The Data Protection criteria ask a product to say what it does with data,
including when the answer is *nothing*. That answer is easy to write and hard to
trust, because the person writing it is the person least likely to remember the
one endpoint added eighteen months ago.

So this starts from the source rather than from memory: the scan lists every
outbound host, telemetry SDK, AI provider and storage location it can find, with
file and line, and you write the disclosure from that list.

## How to use it

```sh
python3 scripts/network-scan.py --path /path/to/checkout
```

`--json` gives machine-readable output. It is read-only.

The scan separates what it finds by where it found it, because the same string
means different things in different files:

- **code and configuration** — candidates for `Y02`, things the product may
  contact when it runs.
- **build, schema or platform hosts** — `github.com`, a plist doctype, a package
  registry. Usually not product destinations. Usually.
- **README, site or docs only** — not `Y02` at all, but a site that *loads* them
  is what `W07` asks about, so they are worth seeing.

Telemetry, provider and storage matches come only from code and configuration.
A Markdown file naming Sentry is usually a sentence saying Sentry is *not* used,
and matching there produces precisely the wrong finding.

## Writing the disclosure

**`Y01` is the load-bearing one.** One paragraph in the README or a privacy note,
saying what the product collects, stores, and transmits. The explicit "none" case
counts and is often the true one: *"OpenExample stores your documents in
Application Support and sends nothing anywhere."* A product that says nothing at
all fails, however little it does.

**`Y02` every destination and why.** Take the hosts from the code section and
write one line each: the host, and what it is for. A destination you cannot
explain is the finding — either it should not be there, or nobody remembers what
it does, and both are worth knowing.

**`Y03` telemetry off by default.** If the scan finds an SDK, the criterion wants
it off by default or opt-in, *and* disclosed. If the scan finds none, say the
source was reviewed and none is present; that is the evidence the criterion asks
for.

**`Y04` and `Y06` storage, retention and deletion.** The storage section shows
where the product writes. Document the locations a user would care about, and say
how they find, export, or delete their data — for most small apps that is one
sentence naming a folder they can open in Finder. Where data does not outlive a
session, say so, and `Y06` is answered.

**`Y05` third parties receiving user content.** Name them. An AI provider that
sees a document the user wrote is exactly what this criterion exists for, and
"we use AI features" is not naming it.

## Rules

- **The scan finds candidates, not answers.** A host in source may be dead code,
  a comment, or a test fixture. Confirm before disclosing it, and never disclose
  a destination you have not confirmed — a wrong privacy note is worse than a
  missing one.
- **Write it where a user will look.** The README or a linked privacy note, not
  a comment in the source.
- **Never claim "none" on the strength of the scan alone.** It reads text; it
  cannot see a URL assembled at run time from parts. Say what you checked.
- **Never commit.** Leave the disclosure in the working tree for review.
