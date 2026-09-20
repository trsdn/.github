# 0014 - Release and pinning criteria scale with what they protect

- Status: Accepted
- Date: 2026-09-20

## Context

Assessments across the account's application repositories kept landing on the
same criteria: `R03`, `R05`, `R06`, `R07`, `R08` and `S12`. Every one of those
repositories has a single maintainer, publishes open source, and welcomes
contributions, so the audience is not the problem and the `P` criteria stay as
they are. The recurring cost was process a single maintainer had to invent to
satisfy the wording, not a property a consumer or a contributor would notice.

Each criterion asked for a mechanism where the property it protects can be met
without one:

- `R03` required automation, so a release built by hand from a tagged commit and
  described in the repository failed. What a consumer needs from `R03` is that a
  tag identifies what was built, not that a machine did the building.
- `R07` required a gate that fails the release. The property is that the release
  page and the changelog entry are connected, which a link achieves.
  [0010](0010-release-notes-come-from-the-changelog.md) chose the gate as the
  mechanism; this keeps its reasoning about the gap and relaxes only how the
  connection must be kept.
- `R08` failed a repository that could use build provenance and had not, even
  where the maintainer had decided it was not worth adopting. The failure was
  about a decision, not about anything a consumer could be misled by.
- `R05` was read as due on every release. The risk it guards against is a
  published build that works only on the machine that made it, and that risk is
  unchanged when only the code inside the artifact changes.
- `S12` required a commit SHA for every third-party action, including in a job
  with a read-only token and no secret, where a moved tag cannot reach anything
  worth taking.

## Decision

Widen each criterion so the property is the requirement and the mechanism is a
recommendation. `R03` accepts a documented manual release built from the tagged
commit. `R07` accepts notes that are the changelog entry or link to it, and
recommends the gate. `R08` accepts a true statement that a mechanism is available
and not used, with what a consumer can check instead. `R05` states that a record
stands until a release changes how the artifact is built, signed, or packaged.
`S12` asks for a SHA only where the job can read a secret or write to the
repository.

`R03` and `R07` leave the runner-only list in Automation Availability, because a
criterion that can be met without a workflow run no longer matches that row. A
repository with no runner is now assessed on them and can pass.

`R06` is not changed. A link to a changelog entry with meaningful content
satisfies it for that release.

Every change widens a criterion, so no recorded `Pass` can weaken. The version
moves to 1.14.0 as a minor release. A repository with no runner that recorded
`R03` or `R07` as `Not applicable` is newly due for assessment on them, which is
the "newly need assessing" case the policy classes as minor.

## Consequences

- A repository is no longer required to run a release pipeline to pass `R03`,
  `R07`, or `R08`, and a hand-made release is honest instead of failing.
- The strongest answers are unchanged and still pass: a tag-triggered workflow,
  a gate, and registry provenance or an attestation.
- A statement under `R08` that a mechanism is unavailable where it plainly is
  available is still a `Fail`, so the criterion does not become an assertion
  anyone can make.
- The standard has less machinery to defend a claim of quality on releases. The
  trade is deliberate: a consumer of a single-maintainer application is served by
  a release page that says what changed and a tag that says what was built, and
  the criteria now ask for exactly that.
