# Conformance Record Format

A conformance record is the machine-readable result of assessing a repository
against a named version of the
[Repository Quality Standard](repository-quality-standard.md). It satisfies
criterion `B11` and is the only source the conformance badge renders.

## Location

```text
.github/conformance.yml
```

## Shape

```yaml
standard_version: "1.3.3"
assessed_on: "2026-08-22"
state: "Needs work"
evidence: "docs/self-assessment.md"

criteria:
  B01: pass
  B02: pass
  B03: na
  # ... every criterion in the catalog
```

| Field | Meaning |
|---|---|
| `standard_version` | The standard version assessed against. Must be a published tag. |
| `assessed_on` | ISO date the assessment was completed. |
| `state` | `Healthy`, `Needs work`, `At risk`, `Archive candidate`, or `Archived`. |
| `evidence` | Path or URL to the assessment output holding per-criterion notes. |
| `criteria` | Every criterion in `standard.yml`, mapped to a result. |

Results are `pass`, `partial`, `fail`, `na`, or `unknown`, as defined in the
standard.

## Rules the tooling enforces

`scripts/conformance.py --check` fails when any of these is violated:

- a required field is missing, or `state` is not a defined state;
- a criterion in the catalog is absent from the record;
- a criterion in the record is not in the catalog, which catches records left
  behind after a criterion was retired;
- a result is outside the defined vocabulary;
- `state` is `Healthy` while any criterion is `fail`;
- the committed badge does not match what the record renders to;
- the record has aged past the review cadence.

The last one cannot be cleared by regenerating the badge. Ageing means the
assessment is overdue, not that the badge is wrong, so only a fresh assessment
resolves it. The badge does render as stale in the meantime, so the public
signal stays honest while the check stays red.

## Completeness is the point

Every criterion appears, including the ones that do not apply. `na` with a
rationale in the linked assessment is a complete answer; an absent entry is not.
Without this rule, "does not apply" and "was never looked at" become
indistinguishable, and the record stops being evidence.

`unknown` is available and is meant to be used. A record that claims certainty it
does not have is worse than one that admits a gap.

## Ageing

A record older than the review cadence renders as stale rather than as its last
known result. Because the badge is committed to the repository, the check turns
red once the record ages past the cadence.

That is deliberate. A red check is the signal that reassessment is due. The fix
is to reassess and update the record, or to regenerate the badge so it publicly
renders as stale. What is not available is leaving a two-year-old green badge on
the front page.

## Relationship to the badge

The badge is generated from the record and committed alongside it. No badge
value is editable on its own, so the badge cannot claim something the record does
not say. Where no record exists, no badge is published.

## Starting a record

A record names every criterion in the catalog, so it is generated rather than
typed:

```sh
python3 scripts/conformance.py --init --repository /path/to/repository
```

It writes `.github/conformance.yml` with every criterion set to `unknown`, and
refuses to overwrite an existing record, because a record holds an assessment
that regenerating it cannot reproduce. The `assessed_on` field is a placeholder
that `--check` rejects until it is replaced, so a generated file cannot pass for
an assessment nobody made.

[`templates/conformance.yml`](../templates/conformance.yml) is the same output,
committed for repositories that would rather copy a file than run a script.

## Adoption

Repositories consume the reusable workflow published here:

```yaml
jobs:
  conformance:
    uses: trsdn/.github/.github/workflows/conformance.yml@main
```

The workflow validates the record against the catalog for the standard version
the record names, and fails when the badge has drifted.
