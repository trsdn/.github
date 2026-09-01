# Drafting a conformance record

`scripts/assess.py` reads a repository through the GitHub API and writes a draft
conformance record plus the notes behind it. It exists because the backlog is
arithmetic: `B12` makes the assessed set discoverable, and the difference
between that set and the account is the work outstanding. Transcribing a hundred
records by hand is what keeps that number from moving.

## What it will and will not decide

A script can prove that something is absent. It cannot judge whether a README
explains the purpose, whether tests cover failure paths, or whether an issue
form collects enough to triage on. So it decides only the criteria that a fact
settles, and leaves every other criterion `unknown`.

`unknown` is not a result. `scripts/conformance.py --check` rejects a record
containing one, and the draft keeps the `YYYY-MM-DD` placeholder in
`assessed_on`, which the same check also rejects. Both are deliberate. A record
is produced by a person looking at a repository, and a generated file must not
be able to pass for one. The script removes the transcription, not the
assessment.

| Criterion | Decided from |
|---|---|
| `B01` | The repository description, and only when it is empty |
| `B03`, `P01` | The licence GitHub detects, against the OSI-approved list |
| `B09` | The archived flag, and only when the repository is archived |
| `B11` | Whether `.github/conformance.yml` exists |
| `B12` | Whether the `trsdn-standard` topic is present |
| `P02`, `P06` | The community profile GitHub reports, which counts inherited files |
| `P03` | A security policy in the tree or recognised by GitHub, absence only |
| `P04`, `P10`, `P11` | Whether any intake template exists, absence only |
| `S05` | The secret scanning status, where the token can see it |
| `S09` | Required status checks on the default branch, where the token can see it |
| `S11` | A `permissions` block in every workflow |
| `S12` | Every `uses:` reference, against the graduated table in the standard |
| `S13` | Untrusted triggers and the secrets they can reach |
| `G01` | Whether `AGENTS.md` is at the root |

Everything else is left to a person, and the notes file lists it.

Two of these deserve their limits stated. `P10` and `P11` ask whether intake
collects enough to act on, which the standard assesses on the information
gathered rather than on headings; the script can only see that no template
exists at all, so that is the only result it records. And `P03` is recorded as a
failure only when no policy is found anywhere — the community profile API emits
no `security` key, so its absence proves nothing.

Where the repository is private, the Public profile does not apply, and the
script records `na` against every `P` criterion with that reason.

## Running it

```sh
python3 scripts/assess.py --repo owner/name
python3 scripts/assess.py --repo owner/name --out drafts/owner-name
```

With `--out` it writes `conformance.yml` and `assessment.md` into that
directory. Without it, the record goes to standard output.

Authentication comes from `GH_TOKEN`, then `GITHUB_TOKEN`, then `gh auth token`.
An unauthenticated run still works against a public repository, but the security
and branch-protection facts need a token that can read them, and criteria whose
evidence is not visible are left `unknown` rather than guessed at.

## Finishing the draft

1. Work through the criteria the notes list as left to a person.
2. Replace `assessed_on` with the date you did that.
3. Set `state` from the [Assessment](repository-quality-standard.md#assessment)
   rules, which assign it by impact rather than by percentage.
4. Rewrite `assessment.md` as the evidence the record's `evidence` field points
   at, and check the drafted results while you are there. They are derived from
   one fact each and are not immune to being wrong.
5. Run `python3 scripts/conformance.py --check` in the assessed repository.

## Offline and repeatable runs

Collection and decision are separate, so the decisions can be re-run without the
network:

```sh
python3 scripts/assess.py --repo owner/name --save-facts facts.json
python3 scripts/assess.py --facts facts.json
```

This is also how the tests exercise every rule, including the `S12` table, with
no network access and no fixture repository.
