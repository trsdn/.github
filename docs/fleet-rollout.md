# Bringing every repository to the standard

How agents raise all of an account's repositories to the current standard without
the maintainer deciding each one. It is a procedure for a coordinating agent and
the worker agents it starts, one repository at a time. Nothing here changes what a
criterion requires: [the standard](repository-quality-standard.md) decides that,
and [the guides](guides/README.md) say how.

## Where the account stands

Read on 2026-09-21 from the 156 active, non-fork repositories:

| | Public | Private |
|---|---|---|
| Repositories | 75 | 81 |
| With a conformance record | 16, at nine different versions | none |
| With the `trsdn-standard` topic | 14 | none |
| With an `AGENTS.md` | 33 | 20 |

Thirty-nine repositories have not been pushed to in six months. The numbers come
from `gh repo list` and `gh api`; re-read them instead of trusting this table.

## The unit of work

One repository, worked from a fresh shallow clone in a scratch directory, never from
a working checkout, because another session may have it on a branch of its own.

1. **Claim.** Skip the repository, and report it, when a pull request from another
   session is open on the files this work would touch, or when its default branch
   changed in the last day. A branch named `standard/<version>` marks a repository
   as being worked on; create it first, and stop if it exists.
2. **Read.** The repository's own `AGENTS.md` first: its rules win over a template,
   and a conflict is reported, not overridden. Then run
   [`scripts/assess.py`](assessing.md) for the facts it can read, and the
   [account's capabilities](account-capabilities.md) for a private repository.
3. **Plan.** Decide the profiles, then every criterion with the
   [deciding rules](repository-quality-standard.md#deciding-without-the-maintainer).
   The gaps that remain are the work. A gap with a reason from the closed list is
   recorded and left.
4. **Fix.** Take the kit for the repository's language family from
   [the templates](../templates/) and change only what a gap needs. Prefer the
   reusable workflows to copies. In a private repository add no workflow that needs
   minutes: the [local gate](../templates/local-gate/README.md) and the documented
   validation command take their place.
5. **Verify.** Run the repository's documented validation command. For a public
   repository the pull request's checks must be green, and a change to a workflow
   is not verified until it has run. For a private one the local result goes into
   the pull request description.
6. **Merge.** Squash, when the checks are green or, in a private repository, when
   the local verification passed. Never force a merge past a red check, and never
   rewrite history.
7. **Assess and record.** Write `.github/conformance.yml`, the badge and the
   per-criterion evidence, with every result decided. Merge that as its own pull
   request, so the fixes and the claim about them stay separable.

A repository needs at most three pull requests: the safety net (secrets, security
settings, `AGENTS.md`), the pipeline (CI, lint, release gate), and the record. If it
needs more, stop and report.

## Order

| Wave | Repositories | Why first |
|---|---|---|
| 0, pilot | Three: a public Swift app, a public Python or Node project, a private repository | The procedure and the kits get their defects found on three, not on a hundred and fifty |
| 1 | The 16 with a record | Reassessing is quick, and it shows how stale results are |
| 2 | Active public repositories without a record, one language family at a time | The kits fit best here, and CI is free |
| 3 | Active private repositories | Local commands only, and many are documents or notes with little to do |
| 4 | The 39 not pushed in six months | Decide each with `Overall State`; archiving is the maintainer's action, so list candidates and do not archive |

Do not start a wave until the one before it has been read: a defect found in a kit
in wave 0 is fixed in the kit, then the wave is rerun.

## Who does what

A **coordinator**, the session the maintainer talks to, keeps the queue, starts up to
four **workers** at a time, and collects what they return. Four, because more only
queue on the repositories' own checks and press on the GitHub API. Each worker gets
one repository, this document, the standard, the capabilities statement, and a time
limit of about half an hour. It returns a report and stops.

A worker's report is fixed so the coordinator can read forty at a time: repository,
profiles, state before and after, the pull requests with their outcome, each
criterion that is not a `Pass` with its reason, anything it skipped and why, and
anything it needs a person for.

There is no ledger to keep in step. The state of the fleet is read from the
repositories: the record's version and date, the open `standard/*` branches and
pull requests. Resuming after an interruption is running the survey again.

## What an agent may not do

- Change a repository setting beyond the ones the maintainer has authorised: the
  public security settings, and the `trsdn-standard` topic. Branch protection,
  visibility, archiving, deleting and transferring are the maintainer's.
- Rotate or revoke a credential. When the scan finds a secret in a repository or its
  history, stop work on that repository and report the credential, where it is, and
  what it unlocks. Removing the commit does not undo the exposure, and revoking is
  the one thing only the owner of the account can do.
- Force-push, rewrite history, or delete a branch that is not its own.
- Add Dependabot, or any workflow that needs minutes, to a private repository.
- Trigger a macOS-heavy workflow more than once per pull request in a repository
  that pays for it.
- Merge over a red check, or touch a repository whose own rules forbid it.
- Put private repository content in a public place: a pull request to a private
  repository stays there, and the fleet report is not published.

## When a person is needed

Only four things reach the maintainer, and they arrive in the fleet report, not as
questions: a secret to revoke, a result the maintainer disputes with an issue, an
archive or visibility decision, and a failure the worker could not resolve after one
retry. Everything else is decided by the assessor and recorded with its reason.

## Done

A repository is done when its record names the current version, its state follows
from its results, no criterion is `unknown`, the pull requests are merged, and the
worker's report is filed. A repository that cannot be finished is reported with why,
not left half changed: an unmerged pull request states what is missing.

## What is still to build

A `scripts/fleet.py` that prints the survey table above and the next repositories in
order, a worker prompt kept in the repository beside the kits, and the pilot's three
repositories. None of it is needed for the procedure above to be followed by hand.
