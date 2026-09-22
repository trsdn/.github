# Repository Quality Standard

- Version: 1.27.1
- Last reviewed: 2026-09-21
- Review cadence: every six months, even when nothing changes

This document is the public source of truth for repository quality across
projects maintained by `trsdn`. It defines outcomes and evidence, not a mandatory
technology stack.

A machine-readable catalog of every criterion in this document is published as
[`standard.yml`](../standard.yml). The two are kept in sync by a required check;
neither is allowed to drift from the other.

## Purpose

A maintainable repository lets a new contributor answer five questions without
private context:

1. What is this repository for, and who is it for?
2. How do I install, configure, run, validate, and release it?
3. What protects changes from regressions and leaked secrets?
4. How are contributions, support requests, and security reports handled?
5. What is the current release and maintenance status?

Every assessment must point to durable evidence: a repository file, GitHub
setting, release artifact, or successful workflow run.

## Versioning And Compatibility

This standard is versioned so that an assessment result stays reproducible. A
result is always recorded against the exact version it was produced with.

**The impact is decided by what the change can do to a result already recorded
against an earlier version.** That is the property; the table below lists the
changes that meet each case at the time of writing, and a change not listed is
decided by the property rather than left undecided.

- **Major**, where a recorded result could now be weaker than it was — a `Pass`
  becoming a `Partial` or a `Fail` — or where a record cites an identifier that
  no longer means what it did. Both invalidate a past assessment, which is the
  only thing this policy is protecting.
- **Minor**, where no recorded result can weaken, and some could strengthen,
  become `Not applicable`, or newly need assessing. A repository is never made
  wrong by such a change; it is due for reassessment.
- **Patch**, where no recorded result can change at all.

| Change | Version impact |
|---|---|
| A criterion is removed, renumbered, or its meaning narrows so that a recorded `Pass` could become a `Fail` | Major |
| Applicability narrows, so that a recorded `Fail` could become `Not applicable`, whether by a profile, a section, or a criterion's own text | Minor |
| A criterion's meaning widens, so that a recorded `Fail` could become a `Pass` | Minor |
| A criterion, profile, or section is added | Minor |
| Wording, examples, formatting, or typos change without altering meaning | Patch |

Adding criteria is a minor change because a recorded result stays valid for the
version it names. A repository does not silently regress when this document
grows; it is simply due for reassessment.

Narrowing applicability is minor for the same reason in reverse. No recorded
`Pass` can turn into a `Fail`, so no past assessment is invalidated; the change
can only excuse a repository from criteria it was previously measured against,
and only at its next assessment. Widening is minor on the same test: a repository
that recorded a `Fail` may now be able to record a `Pass`, and one that recorded
a `Pass` is unaffected.

The mechanism does not decide the impact. Applicability has narrowed by profile,
and in 1.9.0 and 1.11.0 it narrowed by a section — [Automation
Availability](#automation-availability) overriding results for criteria inside
other profiles — and in 1.11.0 by a criterion's own text, when `R08`'s escape
hatch was corrected. All three are minor, because a recorded `Pass` survives each
of them.

### Criterion Identifiers Are Permanent

Criterion identifiers are append-only.

- An identifier is never reused, renumbered, or reassigned to different content.
- A criterion that no longer applies is marked retired in place, keeping its
  identifier and gaining a note that states when and why it was retired.
- New criteria take the next free number in their section.

This rule exists because identifiers are cited from other repositories, from
remediation issues, and from conformance records. An identifier that changes
meaning silently invalidates every citation pointing at it.

### Prefix Register

Section prefixes are assigned here and nowhere else. Adding a section requires
claiming its prefix in this table in the same change.

| Prefix | Section |
|---|---|
| A | Archived |
| B | Baseline |
| D | Deployable |
| G | Agent Readiness |
| I | Product Identity |
| L | Language And Localization |
| P | Public |
| R | Package And Release |
| S | Software |
| T | Documentation |
| W | Published Site |
| X | Accessibility |
| Y | Data Protection And Privacy |

Retired prefixes are never reused. Any letter not listed above is free.

### Citing This Standard

Cite the pinned form. Never cite the default branch: it changes underneath the
citation and destroys the evidence trail.

```text
https://github.com/trsdn/.github/blob/v1.2.0/docs/repository-quality-standard.md#s05
```

Every criterion carries an anchor matching its identifier in lower case, so a
single criterion can be linked directly. Assessments, conformance records, and
remediation issues must use this form.

## Profiles

Apply the baseline to every active repository, then add every matching profile.

| Profile | Applies when |
|---|---|
| Public | The repository is publicly visible |
| Software | It builds or executes application, library, CLI, script, or service code |
| Deployable | The maintainer operates a standing deployment of it: a service on a server, container, or cloud environment, or an installation on a workstation that runs or is scheduled without the maintainer starting it. Software that users download or build and install, and a script or tool run by hand, is not Deployable. [Deployable Repositories](#deployable-repositories) decides the cases |
| Package | It publishes a package, binary, image, or release artifact |
| Documentation | Its primary product is documentation, research, content, or templates |
| Published Site | It publishes a website, or it is public and ships an application, tool, or game that a non-developer audience installs or runs |
| Archived | Development has intentionally ended and GitHub marks it archived |

## Private Repositories

Visibility changes what GitHub offers a repository, not what the repository has to
be. A private repository is assessed against the Baseline and every matching
profile except Public. What differs is what the platform provides, and that
depends on the account's plan, so the assessor reads the platform's capabilities
before deciding anything, and an account states them once, in a document each
private repository's record links to. This account's statement is
[Account capabilities](account-capabilities.md).

| Capability | Where it is missing, the effect |
|---|---|
| Hosted Actions minutes | The repository is *without automation*, as [Automation Availability](#automation-availability) defines it |
| GitHub secret scanning and push protection | `S05` is met by a scan the repository runs itself |
| CodeQL and other code scanning | Nothing asks for it: `P13` applies to public repositories only, and static checks belong to `S03` |
| Rulesets and branch protection | `B16` is `Not applicable` with the sentence that criterion requires, and so is `S09` |
| Dependabot alerts and security updates | Where they consume the minutes the account does not have, they stay off, and `S08` is met by a documented process |

A capability that is absent is recorded once per repository, in one sentence naming
the absence and pointing at the account's statement. Without the sentence the
assessor records the ordinary result.

What applies to a private repository:

| Criteria | Private repository |
|---|---|
| `B01`-`B15` | Apply as written. `B06` counts the alert sources that exist and a source that is not offered contributes none |
| `B16` | `Not applicable` where no ruleset or protection is offered |
| `P01`-`P13` | `Not applicable`: the Public profile does not apply |
| `S01`, `S06`, `S07`, `S10` | Apply |
| `S02`, `S03` | Apply. Without automation the check runs as a documented command, and a dated record of a successful run stands in for the workflow run |
| `S04`, `S09` | `Not applicable` without automation, and `S09` also where no ruleset is offered |
| `S05` | Applies. Where GitHub does not offer secret scanning, a documented scan command with a recorded run is `Pass` |
| `S08` | Applies. A documented owner and process is `Pass`, and the process may be the audit that `R09` runs at each release |
| `S11`, `S12`, `S13` | Apply to the workflows the repository has, and are `Not applicable` with none |
| `D01`-`D06`, `R01`-`R08`, `I01`-`I06`, `T01`-`T05`, `W01`-`W09`, `G01`-`G08`, `L01`-`L07`, `X01`-`X05`, `Y01`-`Y06`, `A01`-`A04` | Decided by the profile and the criterion's own text, exactly as for a public repository |
| `R09` | Applies to a repository that publishes releases, by a local step where there is no automation |

Some things a private repository can still do for itself without minutes: run the
[local gate](../templates/local-gate/README.md) before a release, which scans for
secrets and audits dependencies with tools that need no GitHub feature, and run
the repository's own tests and lint by the same documented command. Which tools
fit which language, what code scanning is possible without GitHub's, and what a
self-hosted runner would change are in
[the private repositories guide](guides/private-repositories.md).

## Baseline

| ID | Requirement | Expected evidence |
|---|---|---|
| <a id="b01"></a>B01 | Name and description state the purpose | GitHub metadata |
| <a id="b02"></a>B02 | README explains purpose, audience, status, setup or usage, and key links | `README.md` |
| <a id="b03"></a>B03 | Licensing intent is explicit | `LICENSE` or a clear internal-use statement |
| <a id="b04"></a>B04 | Secrets, local state, and generated output are ignored while maintained source is tracked | `.gitignore` and repository contents |
| <a id="b05"></a>B05 | A reproducible validation command is documented | README, contributing guide, or agent instructions, plus a successful run or a green run on the default branch |
| <a id="b06"></a>B06 | The default branch has a stated merge policy and no open critical alerts | GitHub settings, repository text, and the alert APIs described below |
| <a id="b07"></a>B07 | Dependencies and supported runtime versions are declared where applicable | Manifest, lockfile, or README |
| <a id="b08"></a>B08 | User-facing or operational changes have durable history | Changelog, releases, ADRs, or linked issues |
| <a id="b09"></a>B09 | Visibility, topics, homepage, and archive state are set and agree with the README | GitHub metadata and `README.md` |
| <a id="b10"></a>B10 | Ownership and maintenance status are stated | `CODEOWNERS`, contributing guide, or README |
| <a id="b11"></a>B11 | The repository records which version of this standard it was assessed against, and when | Conformance record described in [Conformance Records](#conformance-records) |
| <a id="b12"></a>B12 | Assessed repositories are discoverable as a set | The `trsdn-standard` GitHub topic |
| <a id="b13"></a>B13 | Each fact has one home, and other documents link to it rather than restating it | [Content Boundaries](#content-boundaries) |
| <a id="b14"></a>B14 | A repository that holds or references a credential states how an exposed one is revoked and replaced | Security policy, runbook, or agent instructions naming each class of credential and who replaces it |
| <a id="b15"></a>B15 | A repository that redistributes third-party code states how the obligations of those licences are met | Notice file, generated attribution list, or a recorded statement that nothing is redistributed |
| <a id="b16"></a>B16 | The default branch cannot be force-pushed over or deleted | Branch ruleset or protection settings |

The parts of these criteria that the default results in
[Deciding Without The Maintainer](#deciding-without-the-maintainer) do not decide
are stated here. `Default` means the default results apply as written.

| ID | Pass | Partial | Fail | Not applicable |
|---|---|---|---|---|
| `B01` | The description is not empty and says what the repository is or does in words beyond its name | The description only restates the name or is generic, such as "my repo" | The description is empty | Default |
| `B02` | All five parts are present. "Key links" means at least one link to documentation, the issue tracker, or the licence | The README exists and at least one, but not all, of the five parts is present | There is no README, or it contains none of the five | Default |
| `B03` | A licence file with explicit terms, including one GitHub reports as unrecognised, or an internal-use or all-rights-reserved statement in a private or unlicensed repository | A file or statement is present but cannot be read as granting or withholding permission | Neither is present | Default |
| `B04` | No secret, local-state file, or generated output is tracked, and `.gitignore` covers what the ecosystem in use usually produces | Local state or generated output is tracked, or the ecosystem's usual output is not ignored | A secret or credential file is tracked in the current tree | Default |
| `B05` | A command is documented, runs from a clean checkout using only documented setup, and exits successfully | The command is documented but the run failed, needs setup that is not documented, or could not be made and no green run exists | No command is documented | The repository holds no executable code, configuration, or build, only prose or static assets |
| `B07` | Every applicable part is declared: third-party dependencies and the runtime versions supported | One applicable part is declared and another is not | No applicable part is declared | Neither a third-party dependency nor a runtime exists |
| `B08` | The latest release, or where none exists the latest user-facing or operational change, has an entry in a changelog, release notes, a decision record, or a linked issue or pull request | History exists but stops before the latest release or change | Releases or such changes exist and none is recorded | The repository has never been released and has no user-facing or operational change |
| `B09` | Visibility, topics, homepage, and archive state are each set and agree with the README, as described below | At least one is set or agrees and at least one is not | None is set or agrees | Default |
| `B10` | A maintenance statement and an owner are both present | Only one is present | Neither is present | Default |
| `B11` | The record is present and `assessed_on` is within the review cadence on the cover | The record is present and older than the cadence | No record is present | Default |

`B02` and `B10` share the status statement. One sentence in the README satisfies
both, and neither restates it. For `B10`, the owner is the account that owns the
repository unless the repository is owned by an organization, in which case a
`CODEOWNERS` entry or a named person or team is needed. A commit to the default
branch within the review cadence also meets the maintenance-status part.

`B04` reads the current tracked files, `.gitignore`, and the file names
`git ls-files` lists. A secret is a file of credential values, such as a private
key or an `.env` with values, or a token in a recognisable format; a placeholder
such as `.env.example` is not one. Generated output the repository documents as
committed, with the command that regenerates it, is maintained source. `S05`
owns secret scanning on commits and pull requests, and `B04` does not require it.

`B05` counts the command as run when the assessor runs it and it exits
successfully, or when the latest run of that command on the default branch is
green and the evidence links it. Where the assessor cannot install the toolchain
or reach the network and there is no green run, the result is `Partial`, with the
reason recorded; the assessor does not leave the criterion open. A Markdown lint
or link check counts as a command for a repository of prose. Where no runner is
available, [Automation Availability](#automation-availability) states what a
recorded run of this command decides for `S02`, `S03`, and `L04`.

`B06` has two parts, and the default results apply to them.

- *Merge policy* is met when the repository shows a choice: at least one of
  squash, merge commit, and rebase merge is disabled, a ruleset or protection
  on the default branch requires a pull request, or the README, contributing
  guide, or agent instructions name the merge method used. All three methods
  enabled with nothing stated is met only where the repository has a single
  maintainer and no ruleset, because the default is then the maintainer's choice.
- *Alerts* is met when no alert is open in these three sources, read with
  `gh api 'repos/OWNER/REPO/dependabot/alerts?state=open&severity=critical'`,
  `gh api 'repos/OWNER/REPO/code-scanning/alerts?state=open&severity=critical'`,
  and `gh api 'repos/OWNER/REPO/secret-scanning/alerts?state=open'`. Secret
  scanning alerts carry no severity and count as critical. An alert dismissed with
  a recorded reason, such as revoked or a false positive, is not open. A source that is disabled contributes no
  alerts, and one the token cannot read is named in the linked evidence and the
  result follows the sources that could be read.

`B16` owns blocking a force push and a deletion, and `S09` owns required checks.
`B06` asks for neither.

`B09` reads `gh repo view --json visibility,repositoryTopics,homepageUrl,isArchived`
and the README. Visibility agrees when a repository the README or licence presents
as open source is public, and one it presents as internal is private. Topics are
owned by `B12` and `P07` and are not assessed here. The homepage agrees when it is set and the README
names it, or is empty and the README names no site or documentation address. The
archive state agrees when the flag matches a README that says maintenance has
ended. An archived repository is assessed under
[Archived Repositories](#archived-repositories).

`B13` is assessed on three kinds of fact in the README, `AGENTS.md`, the
contributing guide, and `docs/`, and on nothing else. A restatement that has gone
stale, so that it no longer agrees with its home, is a copy that disagrees. The
three kinds are: a command, a version or
supported runtime, and a policy such as reporting, contribution, or licence
terms. A mention that links to the fact's home is not a restatement. `Pass` is no
hand-maintained restatement of any of the three. `Partial` is one that agrees
with its home. `Fail` is copies that disagree. Generated restatement does not
count, as [Content Boundaries](#content-boundaries) states.

`B12` marks a repository as *governed by this standard*. It makes no claim about
the outcome; the outcome lives only in the conformance record required by `B11`.
Every repository assessed against this standard carries the topic, whatever its
profile, and a repository with the topic is `Pass`, archived or not. An archived
repository may drop it, and a repository recorded as out of scope does not carry
it; either without the topic is `Not applicable`, with the rationale recorded. A
repository is out of scope when its README or description states that it is
outside this standard and gives a reason. Any other repository without the topic
is `Fail`.

The inventory of assessed repositories is produced with:

```sh
gh search repos --owner trsdn --topic trsdn-standard --limit 100 \
  --json fullName,isArchived
```

The difference between that list and the full account list is the outstanding
assessment backlog.

`B14` applies to a repository that holds a credential or names one it expects to
exist, including a workflow secret, a deployment token, or a registry
credential. `GITHUB_TOKEN` alone does not bring a repository into scope, because
it is issued and revoked per run and there is nothing for a maintainer to
replace. A repository in scope that states nothing is a `Fail`; one that names
some of its credentials is a `Partial`; a repository holding none is
`Not applicable`.

The bar is a few sentences, not an incident-response programme. Naming the
credential, where it lives, and who replaces it is a complete answer. The
criterion asks what happens when one is exposed, and deliberately does not ask
for rotation on a schedule, a drill, or evidence of having rehearsed one. Where
the answer is the same across repositories, link to the shared policy; `B13`
requires that anyway.

`B15` applies to a repository that ships somebody else's code inside something
it publishes — a bundled dependency, a vendored directory, a container layer, or
a compiled artifact that statically links one. A repository whose dependencies
are resolved by the consumer's package manager at install time redistributes
nothing, and one sentence saying so is a `Pass`. A repository with no
dependencies at all is `Not applicable`. A repository that redistributes and
states nothing is a `Fail`, and one that states its approach for some of the code
it ships but not all of it is a `Partial`.

Stating the approach is the requirement. Producing a per-dependency inventory,
running a licence scanner, or adjudicating compatibility between licences is
not, and a criterion that needed any of them would require evidence a single
maintainer cannot produce.

`B16` protects the branch itself, where `S09` gates what enters it. `S09` asks
whether the checks a repository already has are required before a merge, and
[Automation Availability](#automation-availability) records it as
`Not applicable` where no runner can produce such a check. Blocking a force push
and a deletion needs no runner, so `B16` is assessed on its ordinary terms in
every repository, including one with no automation at all.

The evidence is two settings on the default branch, read from the repository's
settings page or with:

```sh
gh api repos/OWNER/REPO/branches/BRANCH/protection \
  --jq '{force: .allow_force_pushes.enabled, deletion: .allow_deletions.enabled}'
```

A branch ruleset targeting the default branch and classic branch protection on
it are equally acceptable. The criterion asks what the settings do, not which
mechanism does it.

| The default branch | Result |
|---|---|
| Is in a repository offered no ruleset or branch protection mechanism at all, and the record says so | `Not applicable` |
| Otherwise, has both force pushes and deletion blocked | `Pass` |
| Otherwise, has one of the two blocked and the other permitted | `Partial` |
| Otherwise, has neither blocked, including where no ruleset or protection covers it | `Fail` |

The first row is narrow and has to be recorded before it can be used. GitHub
offers neither rulesets nor branch protection to a private repository on a plan
without them, so there is no setting to make and nothing to assess. A repository
in that state says so in the evidence its conformance record links to, in one
sentence naming the absence and the reason, on the same terms as
[Automation Availability](#automation-availability) requires for a missing
runner; without that sentence the assessor reads on to the rows below. Every
other repository has the settings available and reaches one of the three
ordinary results.

Whether the repository's own administrators may bypass the setting is not part
of this criterion, and a repository that lets them is not thereby a `Partial`.
The person who can lift the protection is the person who set it, so requiring
enforcement against them would test intent rather than configuration. The
setting still binds every other contributor and every workflow token, which is
what the criterion is for.

## Public Repositories

| ID | Requirement | Expected evidence |
|---|---|---|
| <a id="p01"></a>P01 | An OSI-approved license is present | Root `LICENSE` or `LICENSE.md`, with the SPDX identifier GitHub detects |
| <a id="p02"></a>P02 | Contribution and conduct expectations are documented | `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`, in the repository or inherited from the account |
| <a id="p03"></a>P03 | Security reporting is private and documented | `SECURITY.md`, in the repository or inherited, and a private reporting route |
| <a id="p04"></a>P04 | Issue and pull-request intake is structured | Issue templates or forms and a pull-request template, in the repository or inherited |
| <a id="p05"></a>P05 | README covers install, configuration, examples, compatibility, security, and support status | `README.md`, one sentence or a link per topic |
| <a id="p06"></a>P06 | Community health files are recognized by GitHub | Community profile lists the README, license, contributing guide, and code of conduct |
| <a id="p07"></a>P07 | Metadata supports discovery | Description, at least one topic, and a homepage that resolves where the repository has a site |
| <a id="p08"></a>P08 | README status badges follow the badge convention | [Status Badges](#status-badges) |
| <a id="p09"></a>P09 | Repository activity is shown from a self-hosted, generated source rather than a third-party image service | [Repository Statistics](#repository-statistics) |
| <a id="p10"></a>P10 | Issue intake collects what triage needs, not only a free-text box | Issue templates or forms, in the repository or inherited, whose fields cover the problem, the expected and actual result, how to reproduce it, and the version or environment it occurred in |
| <a id="p11"></a>P11 | Pull-request intake collects what review needs | Pull-request template, in the repository or inherited, covering what the change does, how it was validated, what it risks, and what it relates to |
| <a id="p12"></a>P12 | Dependency vulnerability alerts and Dependabot security updates are enabled | The two repository settings, read with `gh api repos/OWNER/REPO/vulnerability-alerts` and `gh api repos/OWNER/REPO/automated-security-fixes` |
| <a id="p13"></a>P13 | Code scanning covers the repository's languages where CodeQL supports one | CodeQL default setup or a CodeQL or equivalent scanner workflow, read with `gh api repos/OWNER/REPO/code-scanning/default-setup` |

`P01` passes when GitHub reports an SPDX identifier on the
[OSI approved list](https://opensource.org/licenses). Where GitHub reports
`NOASSERTION` or another non-listed identifier, the assessor reads the text and
passes it when it is an unmodified OSI-approved license, and otherwise it is a
`Fail`, as is a missing license.

`P02` and `P03` count files inherited from the account's default community health
files, because what is assessed is what a visitor is shown. Each is a two-part
criterion under the default results: `P02` is `Pass` with both files, `Partial`
with one. `P03` is `Pass` with a security policy and a private reporting route,
where a private route is GitHub private vulnerability reporting or a private
contact address the policy names. It is `Partial` with one of the two. Where the
private-reporting setting cannot be read, the policy file alone decides the
result, so a policy naming a private contact is a `Pass` and one that does not is
a `Partial`, with the unreadable setting recorded.

`P05` is met per topic by one sentence or by a link to where the repository
states it, including a link to a policy or support file. The six topics are
install, configuration, examples, compatibility, security, and support status.
Install, configuration, examples, and compatibility are each `Not applicable`
where the repository has nothing to install, configure, run, or depend on, as a
documentation or templates repository does not. Security and support status
always apply. Every applicable topic covered is `Pass`, some is `Partial`, and
none is `Fail`.

`P06` asks something the other criteria do not: whether GitHub recognizes the
files by name and location, which is what puts them on the Community Standards
page and in the sidebar. `P01` to `P04` ask whether the content is right. It
counts four files, the README, the license, the contributing guide, and the code
of conduct. The security policy and the templates are left to `P03` and `P04` so
that a gap is not counted twice. All four recognized is `Pass`, some is
`Partial`, none is `Fail`. Where the profile cannot be read, the assessor checks
the four files against the locations GitHub recognizes: the root, `docs/`,
`.github/`, and the account's default files.

`P07` is decided on three parts: a non-empty description, at least one topic, and
a homepage. The homepage is required only where the repository has a website or
documentation site, and then it must resolve at assessment time. A repository
without one is assessed on the other two. Whether the description states a
purpose is `B01`, and the `trsdn-standard` topic is `B12`, so neither is repeated
here.

`P12` is the platform half of dependency safety and `S08` the process half:
`S08` asks who triages the alerts, `P12` asks that GitHub raises them and offers
fixes at all. Both settings are free for a public repository and independent of
whether the repository has dependencies, so `P12` has no `Not applicable`. Both
enabled is `Pass`, one is `Partial`, neither is `Fail`. Dependabot version updates
through a `dependabot.yml` are not part of `P12`. A setting the token cannot read
is decided by the default rule for unreadable evidence.

`P13` asks that a scanner looks at the code without the maintainer starting it.
The default setup, a CodeQL workflow, or an equivalent scanner workflow on the
default branch is `Pass`. A configured scanner whose latest run failed is a
`Partial`. Where CodeQL supports a language the repository contains and no
scanning is configured, the result is `Fail`. It is `Not applicable` where none of
the repository's languages is supported, as for a repository of prose, data, or
configuration, and where no runner is available, recorded with the languages
looked for. `B06` decides what an open alert means, and `P13` only that scanning
exists. GitHub's default setup and a CodeQL workflow of the repository's own are
mutually exclusive: while the default setup is enabled, the workflow's results are
rejected. A repository with its own CodeQL workflow is therefore assessed on that
workflow, and the default setup must stay off for it. A compiled language whose
default autobuild fails, such as a Swift package, needs the workflow with a manual
build. See [the CodeQL guide](guides/codeql.md).

`P08` applies to every public repository. Its platform or runtime badge is `Not
applicable` where the repository has no runtime or platform requirement to
report, and the CI and release badges are conditional as
[Status Badges](#status-badges) states.

`P09` applies to every public repository that has a runner, and to none that
does not, as [Automation Availability](#automation-availability) records, except
that a repository with no runner which commits a card and presents it as
generated is a `Fail`. A
repository with a runner that shows no generated card, or one fetched from a
third-party image service, is a `Fail`: the criterion asks for the card, and
having no card is not the same as having nothing to show. The card does not have
to be a commit to the default branch. A workflow that generates it on a schedule
and publishes it to a dedicated branch, such as `stats`, with the README
referencing the file there, satisfies the criterion, because the card is still in
the repository and produced by a workflow. So does committing it to the default
branch by pull request. The default branch and its ruleset are then unaffected,
so `S09` and the pull-request rule of a repository are met, and the write
permission the job needs is one the work requires, so `S11` is met.

`P04` asks whether intake is structured at all. It counts an issue template
whether it is a form (`.yml`) or a Markdown file (`.md`), and a pull-request
template, each in the repository or inherited. A `config.yml` alone is not a
template. Both present is `Pass`, one is `Partial`, neither is `Fail`. Where
issues are disabled, the issue part is `Not applicable` and the pull-request
template decides the result. `P10` and `P11` ask whether the
structure collects enough to act on, because a form with one box labelled
"Description" is structured and still leaves every report to be triaged by
conversation.

Both are assessed on outcomes, not on headings. A template that gathers the
listed information under different names, in a different order, or merged into
fewer fields passes; wording is the repository's business. A template that
gathers some of the listed information but not all of it is a `Partial`, whether
it omits one item or several, and one that collects none of them is a `Fail`. So
is the absence of any template at all, in either case.

A template inherited from the account's default community health files counts,
because what is assessed is what a reporter is actually shown. A repository that
needs different fields from the inherited ones defines its own, which then
replaces the inherited set entirely rather than adding to it.

Fields may be optional where the repository knows they will often not apply, and
a template that lets a reporter say a field does not apply is preferred to one
that forces an answer. What `P10` and `P11` reject is a template that never asks.

A repository whose issues are disabled is `Not applicable` for `P10` and for the
issue part of `P04`, and so is
one that takes intake through a route GitHub forms cannot serve, provided the
route is documented and collects the same information. Neither result is
available for `P11`: every repository that accepts pull requests can carry a
template, and a repository that accepts none is not public in the sense this
section describes.

## Software Repositories

`S02`, `S03`, `S04`, and `S09` name a workflow run as their evidence. Where no
runner is available to the repository,
[Automation Availability](#automation-availability) states what is recorded
instead.

| ID | Requirement | Expected evidence |
|---|---|---|
| <a id="s01"></a>S01 | Setup is reproducible from a clean checkout | Lockfile or declared dependency versions, plus documented commands |
| <a id="s02"></a>S02 | Automated tests cover important behavior and failure paths | Test suite, and a successful run in CI or of the `B05` command |
| <a id="s03"></a>S03 | Formatting, linting, type, and static checks run automatically where supported | Tool configuration, run by a CI workflow or the `B05` command |
| <a id="s04"></a>S04 | CI covers every materially supported runtime or platform | CI jobs or matrix covering each version or platform the README or manifest claims |
| <a id="s05"></a>S05 | Secret scanning runs on commits and pull requests | GitHub secret scanning, Gitleaks, or equivalent |
| <a id="s06"></a>S06 | Configuration is environment-driven and defaults do not expose private data | Example configuration and a read of the source |
| <a id="s07"></a>S07 | Errors and logs are actionable without leaking credentials or personal data | Tests, documented logging behavior, or a read of the source |
| <a id="s08"></a>S08 | Dependency updates and vulnerability triage have an owner and process | Dependabot or Renovate configuration, or a documented owner and process |
| <a id="s09"></a>S09 | Existing required checks protect the default branch | Branch ruleset or protection settings requiring an existing check |
| <a id="s10"></a>S10 | Architecture and non-obvious constraints are documented | README, `docs/`, or ADRs |
| <a id="s11"></a>S11 | Workflow token permissions are declared and no broader than the work requires | A `permissions` block on every workflow or on each of its jobs |
| <a id="s12"></a>S12 | An executable reference in a workflow cannot change underneath the repository | Action and reusable-workflow references |
| <a id="s13"></a>S13 | A workflow triggered by an untrusted contribution cannot read repository secrets | Workflow triggers and secret usage, or an explicit not-applicable result |
| <a id="s14"></a>S14 | A repository with a performance-sensitive path states which path and how it is reviewed or measured | README, `AGENTS.md`, `docs/`, or an ADR naming the path and the practice |

`S01` is decided by reading the lockfile or manifest and the documented commands;
running them is not required. A library that declares dependency ranges in its
manifest instead of a lockfile meets the pinning part. A repository with no
third-party dependencies and no setup step is `Not applicable`.

`S02` passes when a suite exists, it has been run, and at least one test asserts
an error or failure path, such as rejected input, a raised error, or a non-zero
exit. That is the minimum reading of "important behavior and failure paths" under
[Judgement words](#deciding-without-the-maintainer): the main entry point is
exercised and one failure path is. The main entry point is the command, function
or action the README names as what the software does. For a graphical
application it is the logic behind that action, reached without its views, and a
suite that exercises only a supporting part of it is a `Partial`. Tests with no failure path are a `Partial`; no
tests are a `Fail`. That the run is green is read as evidence and decided by
`B05` and `S09`, not here. The run is read from the workflow history or, where
the repository is recorded as without automation, from the `B05` command as
[Automation Availability](#automation-availability) states.

`S03` counts four kinds of check: format, lint, type, and static analysis. A kind
counts only where the language's standard toolchain or a widely used tool for it
provides one, and compiling counts as the type check for a compiled language. The
minimum reading of "where supported" is a format or lint check that runs
automatically, plus a type check where the toolchain provides one. Running the
minimum is `Pass`: kinds beyond it are welcome, and their absence lowers nothing.
Running only part of the minimum, a lint check where a type check is also
supported or the reverse, is `Partial`, and none is `Fail`. In a repository
without automation the same checks run as a documented command, as
[Automation Availability](#automation-availability) states. A
repository whose language has no such tool is `Not applicable`.

`S04` compares CI with the runtimes and platforms the README or manifest claims.
One job per claimed version or platform is enough, and a repository claiming one
runtime passes with one job. A claim stated as a range, such as "macOS 14 or
later", is covered by a job on the newest version available to the runner, and a
job on the lower bound is welcome and not required. A claimed one missing from CI is a `Partial`, and
CI that exercises none of them is a `Fail`. A repository that claims no runtime
or platform is `Not applicable`.

`S05` passes with GitHub secret scanning enabled, or with a scanner workflow that
runs on both pushes and pull requests. A scanner on only one of the two, or only
on a schedule, is a `Partial`. Where the setting cannot be read and no workflow
scans, the result is `Partial` with the unreadable setting recorded. Where GitHub
does not offer secret scanning and the repository is without automation, a
documented scan command with a dated record of a successful run within the review
cadence is a `Pass`, as [Automation Availability](#automation-availability)
states. `S05` then needs a runner to run and none to check, so it moves to the
row of checks the repository owns.

`S06` is `Not applicable` where nothing in the repository reads configuration.
Otherwise a committed credential or personal data as a default, such as a token,
a personal email address, or a home-directory path, is a `Fail`. Configuration
read from the environment or from a file with a committed example and no such
default is `Pass`, and configuration partly hard-coded to one machine or host is
a `Partial`. The assessor finds these by searching the source for hosts, paths,
and credential-shaped strings.

`S07` is `Not applicable` where the code emits no logs or error messages. The
minimum reading of "actionable" is a message that names the failed operation and
its cause, not a bare "error" or a stack trace alone. The assessor reads the
source or the documented behavior and searches it for logging of environment
variables, tokens, passwords, or request headers and bodies. Actionable messages
and no such logging is `Pass`, one without the other is a `Partial`, and neither
is a `Fail`.

`S08` is `Not applicable` where the repository has no third-party dependencies
declared in a manifest or lockfile or vendored. Otherwise a Dependabot or Renovate
configuration, or a sentence in the README, contributing guide, or security policy
naming who updates dependencies and triages advisories and how, is a `Pass`; in a
single-maintainer repository the maintainer is the owner. Vulnerability alerts on
with no update process is a `Partial`, and neither is a `Fail`.

`S09` is `Not applicable` where the repository has no check to require, because
`S02` and `S03` fail first. Otherwise a ruleset or protection that requires an
existing check before merge is `Pass`, protection with no required check is
`Partial`, and none on the default branch is a `Fail`. Where the settings cannot
be read, the result is `Partial` with the unreadable setting recorded.

`S10` passes when the README, `docs/`, or an ADR names the main components and any
constraint a new contributor could break without knowing it, such as a required
ordering, an external service, a compatibility target, or a generated file.
Components without constraints, in a repository that has constraints, is a
`Partial`, and nothing documented is a `Fail`. Where the assessor reads the entry
points and workflows and finds no such constraint, and the repository is a single
component, one sentence describing it is a `Pass` and the constraints part is
`Not applicable`.

Automation is the part of a repository that runs with the most authority and is
read the least often. These three cover it.

`S11` is satisfied by a declared `permissions` block, at workflow or job level,
that grants only what the job uses. A repository whose workflows declare none
inherits the account default, which is frequently write-capable, so the omission
is a `Fail` rather than an oversight. Declaring it on some workflows and not
others is a `Partial`. A block of `write-all`, or a write scope no step of the
job uses, is not minimal and is a `Partial`.

`S12` treats a reference by a moving name as unpinned, on the same reasoning
[Citing This Standard](#citing-this-standard) applies to citations: a name that
resolves to different content later destroys the evidence trail, and here it
also changes what executes. The rule is graduated by who controls the target,
because that is where the risk actually differs.

| Reference | Required form |
|---|---|
| An action from an account outside the one being assessed, in a job that can read a secret or write to the repository | A commit SHA, or a recorded reason why a tag is acceptable |
| An action from an account outside the one being assessed, in a job with a read-only token and no secret | A major-version tag is sufficient; a SHA is permitted and not required |
| An action published by GitHub itself | A major-version tag is sufficient; a SHA is permitted and not required |
| A workflow or action from within the account being assessed | A branch is permitted, including the default branch |

The first two rows divide on what a moved tag could reach, because that is where
the risk actually differs. A hijacked action in a job with a read-only token and
no secret can waste a run and lie about a result, but cannot exfiltrate a
credential or change the repository. In a job that holds either, it can do both,
which is why only that case asks for a SHA. The job's own `permissions` block and
its secret usage are the evidence, and `S11` already requires the first.

The last row is a permission, not an obligation, and it is stated because the
alternative is worse: pinning a reusable workflow to a tag means re-tagging
every repository that calls it before any fix reaches them. An account that
publishes shared workflows accepts that it can break its own consumers, which is
a risk it can see and fix, unlike a third party it cannot.

A reason for a tag is recorded as a comment on the line of the reference or the
line above it. Where every reference in scope takes its required form the result
is `Pass`, where some do not it is a `Partial`, and where none does it is a
`Fail`.

A repository with no workflows is `Not applicable` for `S11` and `S12`.

`S13` is about triggers that run with the repository's own token or secrets on
content a contributor controls, of which `pull_request_target` and
`workflow_run` are the common ones. A repository using none of them is
`Not applicable`. One that uses them without exposing secrets to the untrusted
content passes, and it passes whether that is by design or by circumstance,
because the criterion is about what an attacker can reach and not about intent.
One that lets contributor-controlled content run in a job that can read a
repository secret fails. The result does not improve because the workflow is
guarded by a label, an approval, or a maintainer's attention. What the
workflow's own token may write is decided by `S11`, not here.

`S14` asks whether a practice exists, not whether performance is good: the
latter is a judgement no fixed line can decide consistently, which is why it is
not asked here. A path is *performance-sensitive* when at least one holds: it
runs on every frame, request, or keystroke; it sits in a startup or launch
sequence a user waits on; its cost scales with the size of user-supplied
content or input, with no fixed bound; or a past issue, benchmark, or profiling
note in the repository already treats it as one. A repository with no such
path is `Not applicable`, recorded with what was looked for.

Where such a path exists, naming it and stating the practice is a `Pass`: a
comment in the code, a line in `AGENTS.md` or the README, or an ADR, saying
which path and how it is reviewed or measured, whether that is a benchmark
suite, a profiling routine run before a release, or a documented review pass —
[a performance-review agent](../packages/performance-review/README.md) run
before merging a change to that path is one way to meet "reviewed," not the
only one. Naming the path without stating a practice, or stating a practice
without naming which path it covers, is a `Partial`. A performance-sensitive
path with neither is a `Fail`.

## Deployable Repositories

| ID | Requirement | Expected evidence |
|---|---|---|
| <a id="d01"></a>D01 | Target, prerequisites, configuration, and deployment command are documented | Deployment guide or runbook |
| <a id="d02"></a>D02 | Secrets are referenced, never committed, and their safe location is documented | Secret names and secret-store reference |
| <a id="d03"></a>D03 | Health verification is a command or a stated observable step, and the way back to the previous working state is documented | Health command or stated step, and runbook. A rollback that has been rehearsed is welcome and is not required |
| <a id="d04"></a>D04 | Runtime and infrastructure dependencies are constrained | Container, IaC, deployment, or runtime files |
| <a id="d05"></a>D05 | Operational changes update durable history and inventory where applicable | Changelog and inventory entry |
| <a id="d06"></a>D06 | Backup, migration, and destructive-operation risks are addressed when stateful | Runbook or explicit not-applicable result |

The profile turns on one property: a *standing deployment*, something the
maintainer puts in place and keeps running or scheduled, so that it has a target,
configuration, and possibly state to look after.

| The repository is | Deployable |
|---|---|
| A service, container, or cloud environment running on a server, host, or platform | Yes |
| An installation on a workstation that the repository installs and that runs without the maintainer starting it: a launch agent, scheduled job, daemon, or self-hosted service | Yes |
| An application or tool that users, the maintainer included, download or build and install from a release, such as a macOS app or a CLI | No: the Package profile decides it |
| A script or tool the maintainer runs by hand when needed, with no install step that keeps it running | No |
| A site served by GitHub Pages or an equivalent static host that builds or serves the repository's files, with no server the maintainer runs | No: the Published Site profile decides it |

A repository that is both, such as an app with a backend service, is Deployable for
the deployment only. Where the profile does not apply, `D01`-`D06` are recorded
`Not applicable` with the sentence "not a standing deployment", naming which row
above matched.

The default results in [Deciding Without The Maintainer](#deciding-without-the-maintainer)
apply. These are the boundaries they need here.

- `D01`: the deployment command is whatever puts the deployment in place, such as
  a compose command, a deploy script, `launchctl bootstrap`, or `make install`.
  Each of the four parts is a part for the default rule.
- `D02`: `Not applicable` where the deployment uses no secret, recorded with what
  was looked for (environment files, configuration templates, workflow secrets,
  documentation). Otherwise the parts are: no secret value in the current tree,
  and the safe location documented for each secret name. History is `B04`'s.
- `D03`: the parts are a health check that is a command or a stated observable
  step, and documented steps for returning to the previous working state, which
  may be as short as redeploying the previous tag or restoring a named backup.
  The assessor does not run either against the target.
- `D04`: *constrained* means no floating `latest` tag, no unbounded or absent
  version range, and no unstated runtime version. A tag, a digest, a lockfile, a
  bounded range, or a documented runtime version each constrain. The parts are the
  runtime and the infrastructure dependencies (base image, provider, service
  versions); all constrained is `Pass`, some is `Partial`, none is `Fail`.
- `D05`: an *inventory* is a list of deployments kept outside this repository that
  the repository names as one it maintains. Where none is named, only the
  durable-history part is assessed, the record says no inventory is named, and the
  result is `Pass` or `Fail` on it. The history part is met when the latest change
  to how the deployment is configured or operated appears in the changelog,
  a release, an ADR, or a linked issue.
- `D06`: a deployment is *stateful* when it holds data that cannot be recreated
  from this repository: a database, uploaded files, or configuration kept only on
  the host. A cache or a derived index is not state. A deployment that is not
  stateful is `Not applicable`. For a stateful one the parts are a stated backup
  and restore path, and a note on each migration or destructive operation the
  repository provides.

## Package And Release Repositories

| ID | Requirement | Expected evidence |
|---|---|---|
| <a id="r01"></a>R01 | Package metadata is complete and agrees with repository metadata, in the package manifest or, where the manifest format has no field for a property, in the artifact's own metadata | Package manifest, plus the artifact's metadata file for whatever the manifest cannot hold |
| <a id="r02"></a>R02 | Versioning and compatibility policy are documented | README, release guide, or a versioning statement at the head of the changelog |
| <a id="r03"></a>R03 | A tag identifies exactly what was built, and the artifacts come from a documented procedure: a workflow the tag triggers, a shared release pipeline run for that tag, or a documented manual release built from the tagged commit | Release workflow, the shared pipeline's documented run, or the documented manual steps, and the uploaded release assets |
| <a id="r04"></a>R04 | Tag, package version, and release title are consistent | The latest release's tag, manifest version at that tag, and release title; a release workflow check is one way to show it, not the only one |
| <a id="r05"></a>R05 | A smoke kit checks the published artifact as a consumer receives it, without anyone operating the product, and its result for the current build is recorded | A documented kit, and a workflow run or a dated record naming the version checked and the result |
| <a id="r06"></a>R06 | Release notes describe meaningful changes and upgrade concerns | The latest GitHub release or its changelog entry |
| <a id="r07"></a>R07 | The release notes a consumer receives are the changelog entry for the version being released, or link to it, and that entry exists and is not empty | A published release whose notes match or link to its changelog entry; where a gate exists, in this repository or in a shared release pipeline this repository documents, the gate too |
| <a id="r08"></a>R08 | A consumer can verify that a published artifact came from this repository or from the shared release pipeline that publishes its releases, or the repository states that they cannot, or that it does not offer that and what a consumer can check instead | Registry provenance, a build attestation, the shared pipeline's documented and verifiable record, or a recorded statement |
| <a id="r09"></a>R09 | Before a release is published, a secret scan and a dependency vulnerability check have passed for the release commit | A release workflow or checklist, and a dated result recorded with the release |

A repository that has published no release has nothing for `R03`-`R08` to assess:
they are `Not applicable`, and the record says no release exists. Per the default
rule, `R03`, `R04`, `R06`, `R07`, and `R08` are assessed on the latest published
release, and `R05` on the build method that release used.

`R01` is about where the metadata lives, not about whether it exists. Some
manifest formats have no field for a licence, a repository URL, or a description
(SwiftPM is one). Where that is so, the metadata belongs in the file the artifact
itself carries, such as an application's `Info.plist`, and the repository states
which properties live where. The properties are name, version, description,
licence, and repository URL. It is `Pass` when every property has a home and the
homes agree with each other and with the GitHub description, licence, and
homepage; `Partial` when every property has a home and one disagrees, or some
properties have no home; `Fail` when none is set anywhere the assessor can read.

`R02` is met by a statement that names the versioning scheme and says what a
consumer can rely on across versions. Naming SemVer is enough for both, because
SemVer defines what breaking means. Another scheme, such as calendar versions,
needs a sentence on what a new version may change. `Partial` where only the
scheme is named; `Fail` where nothing is stated.

`R04` compares three values for the latest release: the tag, the version the
manifest holds at the tagged commit (or, where R01 places the version in the
artifact's metadata, that value), and the release title. They agree when they name
the same version after ignoring a leading `v` and any product name in the title.
All three agreeing is `Pass`, two of three is `Partial`, and none is `Fail`.

`R03` asks that a tag identifies exactly what was built and that a reader can
tell how the artifact came to exist. It does not require automation and it does
not require the tag push itself to start the build. Three forms qualify:

- A workflow the tag triggers.
- A shared release pipeline that a maintainer starts for a specific tag, builds
  from that tag's pinned commit, and publishes to the release, when the
  repository documents the command that starts it.
- A manual release, when the repository documents the steps, the build is made
  from the commit the tag names, and the uploaded assets are the ones that build
  produced.

What does not qualify is an artifact nobody can trace to a tag: a build made from
a working tree that was never committed, or one whose steps are written down
nowhere. Automation is encouraged because it repeats without care, but a
single-maintainer repository is not failed for releasing by hand a way it can
describe.

For a manual release the assessor cannot see how the assets were made, so it
reads the documented steps and accepts them. It checks that the tag exists, that
it names a commit in the repository, and that the steps say the build is made
from that commit. It does not try to prove the assets match. The parts are the
tag and the documented procedure: both is `Pass`, one is `Partial`, and neither
is `Fail`.

`R06` and `R07` divide the work. `R06` is about content: notes a reader can act
on. `R07` is about provenance: the notes a consumer actually receives are the
maintained entry for that exact version, and not a second description written at
tag time.

`R06` is assessed on the latest release. Its parts are notes that name specific
changes a user can see (a feature, a fix, a removal, a changed behaviour), and,
where the release contains a breaking change or raises a minimum requirement,
notes that say so. `Pass` when both hold, and a release with nothing to warn about
needs no warning. `Partial` when the notes name specific changes but omit a
warning the release needed, or when they are generic, such as "bug fixes and
improvements" or "updates". `Fail` when the notes are empty or only the version.
`R07` is likewise assessed on the latest release. It is `Partial` when the
changelog entry for the version exists and is not empty and the notes describe
the version but neither match nor link to the entry, and `Fail` in the cases
named below. Releases made before a criterion existed are not assessed.
Where a shared pipeline holds the gate, the assessor reads the repository's
documentation of it and accepts it, and does not test the pipeline.

The gap `R07` closes is specific. A repository can keep an exemplary changelog
and still publish releases whose notes are fixed boilerplate, because nothing
connects the two. The entries then reach nobody — the changelog is read only by
someone who already knows to open it, and the release page, which is the surface
a consumer actually lands on, says nothing. `R06` on its own is satisfiable by a
changelog nobody consumes, which is why `R07` asks that the release page and the
changelog entry are connected.

The connection can be either of two things. The release notes can be the
changelog entry's text, or they can link to that entry. A link to a changelog
entry with meaningful content also satisfies `R06` for that release, so a
repository does not have to write the same notes twice. What fails is a release
whose notes say nothing about the version and point nowhere, and a version
released with no changelog entry, an empty one, or one still held in an unreleased
section the tagged version did not absorb.

A gate that fails the release automatically is the most reliable way to keep the
connection, and is recommended where a runner is available, not required. A
minimal gate extracts the section for the tag, exits non-zero when the result is
empty, and passes that same text to the release command as the notes body, so the
published notes and the maintained entry cannot disagree. A repository without
one keeps the same property by hand, and is assessed on the result: the published
release either connects to its entry or it does not.

A gate does not have to live in this repository. A repository whose releases
are built and published by a shared pipeline it does not own, such as a
notarization broker or an organisation-wide release service, may rely on that
pipeline refusing to publish without the changelog entry, when the repository
documents that it does. The repository's part is to keep the entry; the
pipeline's part is to refuse without it.

A reusable starting point is published as
[`templates/release-notes/`](../templates/release-notes/).

`R05` asks whether the artifact a consumer downloads can be checked
automatically, and whether it was. The repository supplies a smoke kit: a
documented command or script that takes the published file, installs or unpacks
it, starts it, and reports a result an agent can read, an exit code or a stated
output, without anyone operating the product. An agent runs the kit against the
published artifact and records the version, the date, and the result. A workflow
that runs it on every release is the strongest form and needs no further record.
The failure this guards against is a build that only works on the machine that
made it, which testing the *published* file rather than the local build catches.

What a kit covers depends on what the artifact is.

| The artifact is | A kit is, for example |
|---|---|
| A command-line tool or library | `--version`, or a self-test, run on the installed file |
| A signed application | The platform's signature and launch-policy check on the published file (on macOS `codesign --verify` and `spctl --assess`), plus a start that confirms the process runs where an unattended start is possible. Where it is not, the signature and launch-policy check alone is the kit |
| A container image | Pull, start, and a health command |
| An application that cannot be started or exercised without an operator | The checks the platform allows without one, such as its signature, and a stated limit |

Using the product's core function is welcome and is never required, because it is
the one part that cannot be automated for an interface that needs an operator.

An assessor that does not run downloaded software records the kit as present and
its own run as not performed. That is the `Partial` row below, unless a run of
the current build is already recorded by a workflow or a dated record, which is
the `Pass` row.

| Situation | Result |
|---|---|
| A kit exists, an agent ran it against the current published artifact, and the version, date and result are recorded | `Pass` |
| A kit exists, but its recorded run is for an earlier build method or is missing | `Partial` |
| A kit exists and its run fails | `Fail` |
| No kit exists, but a dated record names the version that was installed and launched by hand and what was exercised | `Pass` |
| No kit and no such record exist, and the artifact could be checked automatically | `Fail` |
| No kit exists because the artifact cannot be checked without an operator, and the record says so with the checks that remain and what they do not cover | `Pass` |
| Nothing installable is published | `Not applicable` |

A record stands for later releases until one changes how the artifact is built,
signed, or packaged; only that release needs a new run. A release that changes
only the code the artifact contains does not, because the build the run tested
has not changed. This is decided by comparing the build workflow or script, the
signing and packaging configuration, and the entitlements between the recorded
tag and the latest tag: if none of those files differ, the record is current.

**Where the record lives.** In the evidence the conformance record links for
`R05`: a workflow run, or a dated entry in a repository file such as the release
guide or a `smoke-tests` section of the conformance evidence. The entry names the
version checked, the date, the result, and who or what ran the kit. A run by the
assessing agent is recorded as such, so a later reader knows it was not made by
the maintainer.

**What the assessor does not have.** Some kits need a platform the assessor may
lack, such as macOS for `codesign` and `spctl`. An assessor without that platform
does not run the kit, does not record a result it did not observe, and records
what it could not run. Where a run by the maintainer or a workflow is recorded for
the current build, that record decides; where none is, the result is `Partial`
under the missing-run row above.

**What the kit may do.** The kit runs the artifact only in the way a consumer
would: it installs or unpacks it into a temporary location, starts it with the
documented start command, runs no elevated privileges, uses no credentials, and
removes what it installed. The assessor reads the kit before running it. A kit
that does more, or that runs a file the assessor did not download from the
release page, is not run by the assessor. It is recorded as not run, and the
result follows the missing-run row above.

`R08` covers the other half of what a consumer receives. `R03` establishes that
a tag identifies what was built, by a documented procedure, and `R05` that the artifact
works, but neither lets somebody who downloads it later establish where it came
from. A published name is not evidence of origin.

Where the ecosystem issues provenance from the workflow that built the artifact,
using it is the strongest answer and always a `Pass`: npm provenance, PyPI trusted publishing, and GitHub
artifact attestations all qualify, and all of them derive from the workflow
identity rather than from a key somebody has to look after. That is deliberate.
This criterion does not ask for artifact signing with maintainer-held keys,
because key custody is a heavier burden and a worse failure mode than the
absence it would replace, and it does not ask for a software bill of materials,
which is ecosystem-specific tooling that few consumers of these repositories
read.

Where a shared pipeline the repository documents builds and publishes its
releases, that pipeline's own verifiable record is sufficient evidence of origin.
A macOS app released through a notarization broker is the model case: the
Developer ID signature and Apple's notarization tie the artifact to the
publisher's identity and can be checked by anyone with `codesign` and `spctl`,
which is what the repository documents. The repository states what a consumer
can check and how, and what the record does not prove.

Where no such mechanism is used by this repository, a recorded statement of that
fact is a `Pass`. That covers an ecosystem that issues no provenance at all, a
repository with no runner, which cannot reach the mechanism its ecosystem does
offer because every qualifying mechanism derives from a workflow identity, and a
repository that does not use the mechanism, whatever the reason. All three are
recorded the same way, and the assessor may write the statement itself from what
it checked. It states the fact that the mechanism is not used, and does not claim
a decision by the maintainer: the assessor cannot know one, and a reason is quoted
only where the repository states it. This is an accepted path that costs nothing,
and the criterion asks a repository to have answered the question, not to have
adopted a mechanism. The assessor checks the fact by looking for an attestation,
a provenance record, or trusted-publishing configuration, and finding none.

The statement has to be true and has to say something a consumer can use. It
names the mechanism that is not used, or that none exists, and states what a
consumer can check instead, such as a published checksum, the release's tag, or
that nothing beyond the release page's own account of the source is offered. It
lives in the README, the release guide, or the linked evidence. A
statement that a mechanism is unavailable where it plainly is available is not a
statement of a fact that holds, and stays a `Fail`; a statement that it is
available and not used is a `Pass`. Where the repository claims a mechanism, the
assessor verifies the latest release's artifact with the ecosystem's own command
(for example `gh attestation verify`, or `codesign` and `spctl` on a Mac) when it
has the tool and records the outcome as evidence. The documented mechanism
decides the result, so a verification the assessor could not run, or that does
not reproduce, is recorded and does not by itself change it. Neither case is excused by
[Automation Availability](#automation-availability), which does not narrow this
criterion. A repository publishing a document, a site, or nothing installable is
`Not applicable`; `R01` and `R05` are already `Not applicable` in that case for
the same reason.

`R09` asks that a release does not go out with a leaked secret or a known serious
dependency vulnerability that nobody looked at. It does not care who or what runs
the checks: a workflow that gates the release, or a step of the release procedure
that the maintainer or an agent runs locally, with the result written where the
release's own record lives.

- The secret scan passes with GitHub secret scanning showing no open alert at the
  release, a scanner workflow whose run on the release commit succeeded, or a
  documented local scan command, such as a `gitleaks` run, whose result for the
  release commit is recorded.
- The dependency check passes when no critical or high advisory is open without a
  recorded reason. Read it from Dependabot alerts, or from a documented audit
  command such as `osv-scanner`, `npm audit` or `pip-audit`. A repository with no
  third-party dependency records that part as `Not applicable`.
- Both parts pass is `Pass`, one is `Partial`, and neither is `Fail`. A repository
  that has published no release is `Not applicable`.

The result is recorded in the release notes, in a release checklist file with the
date and the commit, or in the workflow run. A repository without automation
cannot run a workflow, and this criterion is why the local command exists: see
[Private Repositories](#private-repositories) and
[the local gate](../templates/local-gate/README.md).

## Product Identity

Apply these requirements to anything a user installs, runs, or downloads:
applications, installers, binaries, container images, published packages, and
hosted sites. They make a shipped artifact traceable back to its source without
guesswork.

These criteria are about the published artifact, not the source. The assessor
downloads the latest release asset, image, or package, or fetches the published
site, and reads its metadata without running it: for a macOS application it
unpacks the archive or mounts the disk image and reads `Info.plist`, and for an
image or package it reads the labels or manifest. A value that appears only in
source is not evidence that the artifact carries it. Where the artifact cannot be
fetched, the assessor records that and what it read instead, such as the build
configuration, and the result follows the readable evidence, as
[Deciding Without The Maintainer](#deciding-without-the-maintainer) describes.
A repository that ships nothing, meaning no release asset, image, package, or
site, has `I01`-`I06` as `Not applicable`. A multi-part criterion here follows the
default rule.

| ID | Requirement | Expected evidence |
|---|---|---|
| <a id="i01"></a>I01 | The built artifact embeds its product name and exact version | Bundle manifest, package manifest, image label, or binary metadata |
| <a id="i02"></a>I02 | The built artifact embeds its repository URL and issue tracker URL | Manifest, label, or metadata field resolved from the release build |
| <a id="i03"></a>I03 | The built artifact embeds its license identifier and copyright holder | Manifest, label, or metadata field, plus the bundled license text where required |
| <a id="i04"></a>I04 | The running product shows its version and links to the repository and issue tracker | About window, `--version` and `--help` output, site footer, or equivalent |
| <a id="i05"></a>I05 | A product icon is embedded in the artifact and reused across installer, store, and site surfaces | Icon asset in the built artifact and on published surfaces |
| <a id="i06"></a>I06 | Embedded identity metadata is produced by the build, not maintained by hand | Release workflow or build script deriving values from the tag and repository |

Example for a macOS application bundle: `CFBundleName`,
`CFBundleShortVersionString`, `NSHumanReadableCopyright`, and `CFBundleIconFile`
are set in `Info.plist`; repository and issue URLs are added as custom keys or
shown in the About window; the release workflow injects the version from the
tag. Equivalent fields exist for other ecosystems, such as `pyproject.toml`
project URLs, npm `repository` and `bugs`, and OCI image labels
`org.opencontainers.image.source` and `org.opencontainers.image.licenses`.

The boundaries the default rule needs:

- `I01`: the exact version is the release's version, not a placeholder such as
  `1.0`, `0.0.0`, or an unresolved build variable. A name with a version that
  differs from the release is `Partial`.
- `I02`: any key or bundled file the assessor can read without running the
  product, whose name says what it holds, is accepted. For a macOS bundle,
  custom `Info.plist` keys such as `RepositoryURL` and `IssueTrackerURL` are the
  suggested pair, and no particular names are required. The URLs are the
  repository's own.
- `I03`: the licence identifier is an SPDX identifier and the copyright holder is
  a name. The bundled text is *required* when the repository's own licence text
  says copies must carry it, which the assessor reads from the licence. It is met
  by a licence file in the artifact or by the text in a bundled acknowledgements
  or About resource. A licence that has no such term needs none.
- `I04`: for a command-line tool the assessor runs `--version` and `--help`, which
  is what a user does. For an interface it cannot operate, such as a graphical
  application, source that renders the version and both links is accepted, and
  the record says it read the source and did not operate the product. A server
  that a client drives and a person does not, such as one that speaks a protocol
  over standard input and output, shows its version when its handshake response
  reports it, which the assessor reads from the source or from the tests. A
  `--version` flag on such a server is welcome and not required. A site is read
  from its fetched footer.
- `I05`: only the surfaces the repository has are assessed, so a repository with
  no store listing or site is not failed for lacking one. The icon in the artifact
  is required, and each surface the repository has must show the same icon, meaning
  one source image. `Not applicable` where the artifact has no place for an icon:
  a command-line binary, a library package, or a container image.
- `I06`: a value is produced by the build when it is derived from the tag or the
  repository, or when it is set in one source-controlled place that the build
  writes into the artifact, such as an Xcode `MARKETING_VERSION` or a manifest
  version. A build script that a manual release runs counts as the build. A value
  typed separately into the artifact's metadata as well is maintained by hand.
  All values produced by the build is `Pass`, some is `Partial`, none is `Fail`.

## Documentation Repositories

| ID | Requirement | Expected evidence |
|---|---|---|
| <a id="t01"></a>T01 | Scope, audience, navigation, status, and freshness are visible | README or index and document metadata |
| <a id="t02"></a>T02 | Internal links and generated output are validated where practical | Link checker or documented review command |
| <a id="t03"></a>T03 | Sources and evidence are distinguishable from conclusions | Citations, references, or source notes |
| <a id="t04"></a>T04 | Generated artifacts identify their source and regeneration process | Build or export documentation |
| <a id="t05"></a>T05 | Stale or superseded material is archived or clearly marked | Status markers and archive structure |

Each criterion here is decided by the default results in
[Deciding Without The Maintainer](#deciding-without-the-maintainer), with the
readings below. The assessor states in the linked evidence which files it read.

- `T01`: the five things are five parts. *Visible* means stated in the README or
  the documentation index, or in a header or front matter block of the documents
  themselves, and reachable from the README or index. Freshness is a date or a
  version a reader can see; status is a word such as maintained, draft, or
  archived. A part met in the entry point and absent from the documents, or the
  reverse, is met.
- `T02`: *practical* means a command a single maintainer can run without a paid
  tool. `Pass` is a link checker or a documented review command that exists and
  runs clean on the current tree. A repository with no internal links has
  nothing to check on that part, and a repository that generates no output has
  nothing to check on the other; where both hold the result is `Not applicable`,
  and where one holds the criterion is judged on the other. A checker that
  exists and fails, or one that is not documented, is `Partial`. No check is
  `Fail`.
- `T03`: the rule applies to a sample of the README and the four most recently
  changed documents. A claim of fact that a reader could not confirm from the
  document itself carries a link, a citation, or a source note, and a conclusion
  is worded or placed so it is not mistaken for one. A document that makes no
  such claim, such as a procedure, a template, or a definition, is outside the
  sample; where the whole sample is outside it the result is `Not applicable`.
  Every sampled document meeting the rule is `Pass`, some is `Partial`, none is
  `Fail`.
- `T04`: a generated artifact is a file a tool writes rather than a person. It
  *identifies its source and regeneration process* when the file carries a header
  or comment naming the source and the command, or when a build or export
  document names both for it. Where the repository generates nothing the result
  is `Not applicable`.
- `T05`: material is *stale* when it has not changed for the review cadence
  of six months, carries no date or
  status saying it is still current, and describes something a newer document or
  the current tree has replaced. It is *marked* when it begins with a status line
  such as superseded, deprecated, or archived that links to its replacement, or
  when it sits in an archive directory. Where the assessor finds no stale or
  superseded material the result is `Not applicable`.

## Published Sites

A repository is read by contributors. A site is read by everyone else. The two
audiences want different things, and serving the second one from a README is why
READMEs grow until nobody reads them.

This profile applies when a repository publishes a website, or when it is public
and ships a product a non-developer installs or runs by name: a downloaded
application, a menu-bar or windowed app, a game, or a command-line tool a user
installs to run directly, whatever platform it targets. The test is whether a
reasonable audience wants the product and not the source, the same test the
Package profile does not ask: a repository can publish installable artifacts and
still have no such audience, for a library packaged for other code to depend on,
or a tool packaged for a pipeline to call.

It does not apply to a private repository shipping such a product, because nobody
outside the account could reach a site for it. `W01`-`W09` are `Not applicable`
there, with the reason.

It does not apply when every reader is working inside a repository or composing
it into other software. A library, an MCP server or agent tool that other
software or developers configure rather than install by name, an internal tool, a
template, and a specification are consumed *in* repositories or by tooling, by
people or programs already there — a page in front of them adds a surface to
maintain and answers nothing they were asking. This document is the example: it
is a definition that maintainers and agents apply to repositories, so it is
assessed as `Documentation` and not here. The repositories it is applied *to* are
a different matter, and many of them do ship a product with exactly this
audience.

A public repository matching the trigger that has not yet published a site
records `W01`-`W09` at their ordinary results, most of them `Fail` until the site
exists: the profile does not excuse a product from having one, and building it is
the remediation.

Record the rationale rather than leaving the profile unclaimed.

| ID | Requirement | Expected evidence |
|---|---|---|
| <a id="w01"></a>W01 | The site is published from the repository by a repeatable, documented process | Deployment workflow and committed site source |
| <a id="w02"></a>W02 | The repository and the site link to each other | Repository homepage field, and a repository link in the site's persistent navigation or footer |
| <a id="w03"></a>W03 | The landing view states what the project is, who it is for, and its current status before any scrolling | Site source |
| <a id="w04"></a>W04 | The site carries the content baseline | [Site Content Baseline](#site-content-baseline) |
| <a id="w05"></a>W05 | Retired 2026-09-17 (standard 1.12.0) — the shared-design-language mandate is replaced by `W09`; see [decision 0013](decisions/0013-sites-are-designed-not-templated.md) | None — retired |
| <a id="w06"></a>W06 | Retired 2026-09-17 (standard 1.12.0) — recording a vendored design-language version is no longer required; see [decision 0013](decisions/0013-sites-are-designed-not-templated.md) | None — retired |
| <a id="w07"></a>W07 | The site loads no third-party resources, sets no cookies, and carries no analytics | Site source and a documented network review |
| <a id="w08"></a>W08 | The site states each fact once and links to the repository for depth | [Content Boundaries](#content-boundaries) |
| <a id="w09"></a>W09 | The site's visual design is made for this project, not left at a framework or template default | [Site Design](#site-design) |

A site is a shipped user interface, so [Accessibility](#accessibility) applies to
it in full. Those criteria are not restated here.

`W05` and `W06` are retired and are not assessed: a conformance record still
lists each as `na` with the rationale "retired", because the record carries every
criterion in the catalog. The results below follow the
default results in
[Deciding Without The Maintainer](#deciding-without-the-maintainer), with these
readings.

- `W01`: two parts, a repeatable process and a sentence documenting it. The
  process is a deployment workflow, or the Pages source setting naming a branch
  and folder of committed source, or a build script; a repository with no runner
  and a static `docs/` or `site/` folder meets it through the Pages setting. The
  sentence is in the README, `AGENTS.md`, or `docs/` and says how the site is
  published. A site whose source lives in another repository is not published
  from this one, and the result here is `Not applicable`.
- `W02`: two parts, one per direction. The homepage field alone meets the
  repository half. The site half is a repository link that appears on every page,
  in the header, the navigation, or the footer; a single-page site meets it with
  the link anywhere on the page. One direction present is `Partial`.
- `W03`: the three statements, what the project is, who it is for, and its status
  as a word such as maintained, experimental, or archived, appear in the first
  visible content in source order, with nothing but navigation ahead of them.
  Reading the source is sufficient evidence. Where the page is rendered, the
  reference viewport is 1280 by 800 pixels.
- `W07`: three parts, no third-party resources, no cookies, and no analytics. The
  *network review* is a list of the hosts the landing page requests. The
  assessor produces it by searching the site source for `src`, `href`,
  `@import`, `url(`, and `<script>` values that point to another host, and for
  cookie writes and analytics code. A browser or a recorded request list is
  an equal alternative and is not required. A search that finds no other host, no
  cookie API use, and no analytics is a `Pass`. Links a visitor follows are not
  loaded resources, and neither is the host that serves the site itself; a badge
  image loaded from another host is a third-party resource. Where the assessor
  can see the source only, it says so in the linked evidence.
- `W08`: the test is [Content Boundaries](#content-boundaries). A contributor,
  architecture, or changelog section on the site is a `Fail`. A fact repeated on
  the site and in the README or `docs/` without a link to its home is `Partial`;
  a mention that links to the fact's home is not a repetition, as `B13` states.
  No repetition and no such section is a `Pass`.

`W07` is the same argument as `P09` and `Y02`. A font, script, or image loaded
from another host observes every visitor on a page the maintainer controls, and
adds an availability dependency on somebody else's free tier. Self-host it or do
without it.

### Site Content Baseline

`W04` is satisfied when the landing view carries all of these. Order is a
suggestion; presence is not. There are seven items: all seven is `Pass`, at least
one and fewer than seven is `Partial`, and none is `Fail`, as the default results
in [Deciding Without The Maintainer](#deciding-without-the-maintainer) state.
The `Y01` sentence, the links, and the date are found by searching the landing
source. An item that has nothing to show does not count against the page: a
product with no visual or textual output meets the third item with its shortest
honest statement alone, without a screenshot or sample.

- The name and a one-sentence statement of what the project is.
- Status and version: maintained, experimental, or archived, and which release
  the page describes. A page that says it describes the latest release, or links
  to it, names one.
- What it does, in the shortest honest form. A screenshot, an example, or a
  short sample where the product is visual or textual.
- How to get it, or how to read it: download, install, or the entry point to the
  content.
- The disclosure required by `Y01`, even when the answer is that nothing is
  collected. One sentence is a `Pass`.
- Links to the repository, the license, the security policy, and how to get
  support.
- The date the page was generated or last reviewed.

These belong in the repository and not on the site: contribution instructions,
architecture, decision records, the full changelog, and anything addressed to
contributors rather than to readers. A site that grows a contributor section has
started to duplicate the repository, which `W08` forbids.

A site may be a single page. Nothing in this section requires more than one, and
a single honest page beats a navigation tree over empty sections.

### Site Design

There is no shared design language every site is required to use, and no
default one to reach for. `W09` asks whether a visitor can tell the page was
built for what it describes, or whether it is unstyled HTML, a framework's
default theme, or another project's site reused unchanged. That test is
judgement, not a checklist, so what counts as evidence is a brief, honest look
at the page rather than a single artifact.

An assessor reads the stylesheet and the theme configuration and concludes only
what they show. `W09` is a `Fail` where the site has no stylesheet, or uses a
framework or template theme with no override of its colour, type, or layout, or
carries the stylesheet and assets of another project's site unchanged. It is a
`Pass` where the site's own stylesheet or theme configuration sets colour, type,
or layout values that differ from the theme's defaults and from any other site
the assessor can compare it to. Whether the design suits the subject, and whether
it is good, is taste and is outside what the criterion decides: a site that is
not one of the three `Fail` cases is a `Pass`, and the assessor does not mark it
down for looking plain. Rendering the page is not required. Where the assessor
can see only source, it says so in the linked evidence.

Colour, type, and layout are chosen for the project's own subject matter, and
the accessibility fundamentals that a shared system used to settle once —
contrast, visible keyboard focus, a legible type scale, sane behaviour down to
a phone width — are handled per site instead. `W07` still applies in full: a
distinctive site self-hosts its own fonts, images, and scripts rather than
reaching for a font CDN or an icon service.

This replaces the shared design language, **Instrument Workshop**, that earlier
versions of this standard required every site to vendor (`W05`, `W06`; both
retired — see [decision 0013](decisions/0013-sites-are-designed-not-templated.md)).
A site is not penalised for still using it: nothing here forbids vendoring it
where it genuinely fits, only the requirement that every site do so by default.

[The site design guide](guides/site-design.md) walks through building one, with
a designer agent that researches the specific product before writing anything
and a reviewer that checks the mechanical parts and holds the line that design
taste is out of scope here, the way this section does.

## Content Boundaries

`B13` and `W08` both point here. The rule is one sentence: **each fact has
exactly one home, and every other surface links to it.**

A fact stated in two places will be updated in one of them. The second copy then
becomes wrong while still looking authoritative, and readers have no way to tell
which one is current. This is the most common way a well-maintained repository
starts to mislead.

| Surface | Answers | Bounded by |
|---|---|---|
| Description and topics | What is this, in one line | One sentence |
| Site | What it is and why it is worth your time, for someone who will never read the code | The content baseline above |
| `README.md` | What, why, status, how to start, and where to go next | Links outward rather than expanding inward |
| `docs/` | Depth: architecture, guides, reference, runbooks | No limit |
| `docs/decisions/` | Why a choice was made, and what it cost | One decision per file |
| `CHANGELOG.md` | What changed, and when | One entry per release |
| `AGENTS.md` | How to work in this repository safely | Operating rules only |

The README is the surface that goes wrong most often, because everything looks
like it belongs there. The test is whether a paragraph answers *how do I start*
or *why should I care*. If it answers *how does it work internally*, it belongs
in `docs/`. If it answers *why was it built this way*, it belongs in a decision
record.

The same test resolves the site. If a paragraph is addressed to somebody who
might change the code, it does not belong on the site. A paragraph is addressed
to such a person when it describes how to build, test, or contribute, how the
code is organised internally, or what changed between versions.

`B13` is assessed on the repository's own surfaces and `W08` on the site against
them. A fact repeated between the site and the repository is recorded against
`W08`, and a fact repeated between two repository surfaces against `B13`, so one
repetition is not counted twice.

Duplication that a generator produces from a single source is not duplication.
The badge, the conformance record, and the statistics card all restate facts that
live elsewhere, and none of them can drift, because none of them is edited by
hand. That is the distinction: **generated restatement is fine, hand-maintained
restatement is not.**

## Agent Readiness

AI coding agents are primary contributors to these repositories. A repository
that cannot be worked in safely by an agent is not maintainable in practice,
even when a human can still navigate it.

The Baseline requires `G01` only. The Software, Deployable, and Package profiles
require the full section. Documentation repositories require `G01` and `G03`.

| ID | Requirement | Expected evidence |
|---|---|---|
| <a id="g01"></a>G01 | Agent-facing instructions exist at a discoverable, tool-neutral location | `AGENTS.md` in the repository root |
| <a id="g02"></a>G02 | Instructions state purpose, layout, and the authoritative build, run, and validation commands | `AGENTS.md` content plus a successful run of each command |
| <a id="g03"></a>G03 | Forbidden and high-risk operations are named explicitly | `AGENTS.md` section covering history rewriting, force pushes, secret handling, deployments, releases, and data-destructive commands |
| <a id="g04"></a>G04 | Tool-specific configuration does not diverge from the tool-neutral instructions | `.github/copilot-instructions.md` and equivalents reference `AGENTS.md` instead of restating it |
| <a id="g05"></a>G05 | An agent can validate its own change before proposing it | A single documented command that succeeds from a clean checkout |
| <a id="g06"></a>G06 | Generated, vendored, and machine-owned paths are marked so they are not hand-edited | `.gitignore`, `.gitattributes`, or an explicit statement in `AGENTS.md` |
| <a id="g07"></a>G07 | Agent-authored changes are attributable and reviewable | Commit trailers, pull-request labels, or a documented review expectation |
| <a id="g08"></a>G08 | Repository-scoped agent configuration is intentional where the platform supports it | `.github/github-app.yml` or a recorded not-applicable result |

`G04` is the criterion that decays first. Duplicated instructions drift apart,
and an agent then follows whichever copy it happens to read. A tool-specific file
should point at `AGENTS.md`, not paraphrase it.

The results follow the default results in
[Deciding Without The Maintainer](#deciding-without-the-maintainer), with these
readings.

- `G02`: three parts, purpose, layout, and commands. *Authoritative* means
  `AGENTS.md` names the command as the one to use, or links to the document that
  does. The assessor runs the validation command from a clean checkout and it
  must succeed, or a linked green run of it on the default branch counts as
  `B05` counts it. Build and run commands are required to be stated and are not
  required to be run, and a repository with nothing to build or run states
  none. A validation command that fails is `Partial`. A validation command that
  cannot run in the assessor's environment, because it needs a secret, a
  service, the network, or is destructive, is `Partial` with the reason recorded
  in the linked evidence.
- `G03`: the topics are history rewriting, force pushes, secret handling,
  deployments, releases, and data-destructive commands. A topic that concerns
  something the repository does not have, such as deployments in a repository
  that deploys nothing, need not be named, and the assessor records which topics
  it treated that way. *Covering* a topic means `AGENTS.md` says what an agent
  must not do or must ask before doing.
- `G04`: the tool-specific files are `.github/copilot-instructions.md`,
  `CLAUDE.md`, `GEMINI.md`, `.cursorrules`, `.cursor/rules/`, `.windsurfrules`,
  and `.clinerules`. A file that exists meets the rule when it links to or
  tells the agent to read `AGENTS.md` and does not contradict its instructions.
  Repeating an instruction that agrees is not divergence, and `B13` does not
  assess these files. Where none of these files exists, the result is `Pass`,
  because there is nothing to diverge.
- `G05`: it is met when the command `B05` requires is named in `AGENTS.md`, or
  `AGENTS.md` links to the document that names it, and the command succeeds from a
  clean checkout, or a linked green run of it counts as `B05` counts it. One
  documented sequence that the documentation calls the complete validation counts
  as the single command. `B05` decides whether a command is documented and `G05`
  whether the agent is pointed at it, so a repository with no `B05` command has
  no `G05` command either, and the result is `Fail` on both, except that `G05` is
  `Not applicable` where `B05` is. A command that cannot run in the assessor's
  environment is `Partial`, with the reason recorded.
- `G06`: the paths are those a tool writes, those copied in from elsewhere, and
  those a person must not edit, including lockfiles. A path is *marked* when
  `.gitignore` excludes it, `.gitattributes` flags it as `linguist-generated` or
  `linguist-vendored`, or `AGENTS.md` names the path or a pattern that matches it.
  Where the repository has no such path the result is `Not applicable`.
- `G07`: this is one test with three accepted forms. It is met when the
  repository documents a trailer rule, a pull-request label rule, or a review
  expectation, in `AGENTS.md`, `CONTRIBUTING.md`, or the README. A repository with
  no agent-authored commits is judged on the documentation alone, and commit
  history is not sampled. No such documentation is `Fail`.
- `G08`: `.github/github-app.yml` is the file the GitHub Copilot app reads for
  repository-scoped configuration: instructions, named scripts, and automation
  settings, as in [Recommended Shape](#recommended-shape). It is *intentional*
  when it is committed, is not empty, and its instructions point at `AGENTS.md`
  or do not contradict it. A file that is only a placeholder, or whose content
  contradicts `AGENTS.md`, is `Partial`. Where the platform does not offer the
  capability, meaning the repository is not hosted on GitHub or the account has
  no access to the app, the result is `Not applicable`, with what was checked
  recorded. An absent file where the platform does offer it is `Fail`.

A reusable starting point is published as [`templates/AGENTS.md`](../templates/AGENTS.md).

## Language And Localization

Repositories are published to an international audience. Language is therefore a
property of the repository, not a matter of personal habit.

Applies to the Software, Deployable, Package, Documentation, and Published Site
profiles. `L04` accepts a command or a CI check; where no runner is available,
[Automation Availability](#automation-availability) states which result the
command produces.

| ID | Requirement | Expected evidence |
|---|---|---|
| <a id="l01"></a>L01 | The primary user-facing language is declared and is English unless a documented exception applies | README statement |
| <a id="l02"></a>L02 | User-facing strings are not hardcoded in a language other than the declared primary language | Source review or a lint rule |
| <a id="l03"></a>L03 | Localization support is declared as either English-only or an explicit list of supported locales | README or locale manifest |
| <a id="l04"></a>L04 | Localized builds keep string catalogs complete, with missing and orphaned keys detected | Catalog files plus a validation command or CI check |
| <a id="l05"></a>L05 | Dates, numbers, currency, and sorting use platform locale APIs rather than manual formatting | Source review or tests |
| <a id="l06"></a>L06 | Translated strings are traceable to their source string and to their translation origin | Catalog metadata or translation notes |
| <a id="l07"></a>L07 | Repository and contributor surfaces are English | README, `docs/`, code comments, identifiers, commit messages, issues, pull requests, and release notes |

User-facing surfaces include interface labels, menus, notifications, onboarding,
error messages, `--help` and `--version` output, human-readable log messages,
store listings, install prompts, and website copy.

`L07` applies even to repositories that ship a non-English product. The product
language and the contributor language are separate decisions.

The results follow the default results in
[Deciding Without The Maintainer](#deciding-without-the-maintainer), with these
readings. A repository with no user-facing surface is `Not applicable` on `L01`
to `L06`, and `L07` still applies.

- `L01`: the README says the primary language in one sentence, for example
  "Primary language: English." Any exception follows the
  [German-Content Exception](#german-content-exception) form: the subject matter
  is inherently in that language, and the README says so in one sentence.
  Silence is a `Fail`.
- `L02`: the assessor samples the files that hold user-facing strings, meaning
  resource and template files and the source files that print or display text,
  and the `--help` output, up to twenty files. It looks for text in a language
  other than the declared primary one. Strings in a catalog for a locale that
  `L03` declares are not hardcoded strings. None found in the sample is `Pass`,
  and where the assessor cannot reliably tell a language it says which files it
  could not judge.
- `L03`: one sentence in the README saying "English only" or listing the locales,
  or a locale manifest such as a `locales/` directory, an i18n configuration, or a
  string catalog. One sentence may carry `L01` and `L03` together, and each is
  then recorded as met by it.
- `L04`: *localized builds* are those that ship more than one locale. Where the
  repository declares English only under `L03`, or ships one catalog or none, the
  result is `Not applicable`, and
  [Automation Availability](#automation-availability) is reached only where the
  criterion applies. Where it applies, `Pass` is a documented command or CI
  check that reports both missing and orphaned keys and runs clean, `Partial` is
  a check that reports only one of them, or fails, or is not documented, and no
  check is `Fail`.
- `L05`: manual formatting is building a displayed date, number, currency amount,
  or sorted text by hand instead of through a locale-aware API. Searches that
  find it include `strftime` and `%Y` patterns in displayed strings, `toFixed(`,
  a currency symbol concatenated to a number, and `sort()` on displayed text
  without a collator. Machine-readable output such as ISO dates in files and logs
  is not display formatting, and neither is sorting identifiers, keys or file
  names that a person does not read as text. Where nothing in the source formats these values for
  display the result is `Not applicable`.
- `L06`: where the repository ships no translations, the result is `Not
  applicable`. Otherwise a translation is *traceable* when the catalog or a
  translation note records the source string or its key beside it and says who or
  what produced it, such as a translator's name or "machine-translated" and the
  tool.
- `L07`: the assessor reads the current README, `docs/`, code comments, and
  identifiers, and samples the last twenty commit messages, issues, and pull
  requests opened by the maintainer or an agent, and the latest release notes. History
  older than the sample is not counted, and neither is text written by other
  people. A surface that has no items, such as a repository with no issues, is
  not counted.

### German-Content Exception

A repository whose subject matter is inherently German — genealogy, archival,
regional, or personal-record projects — declares German as its primary
user-facing language in its README, with one sentence of rationale. The
exception covers the product surface only. `L07` still applies.

Silence is not an exception. An undeclared language is a `Fail` on `L01`.

## Accessibility

Applies to the Deployable and Package profiles, and to any repository shipping a
user interface, including command-line tools and websites. Not applicable to
libraries with no user-facing surface; record the rationale.

These are single-maintainer projects. The target is the absence of obvious,
cheap-to-avoid barriers, not formal conformance certified by an audit. No
criterion here requires a paid tool or a specialist.

| ID | Requirement | Expected evidence |
|---|---|---|
| <a id="x01"></a>X01 | The product is fully operable by keyboard, including focus order and a visible focus indicator | An automated test, a review of the source by the assessing agent for focusable and keyboard-reachable controls, or a documented check |
| <a id="x02"></a>X02 | Interactive elements expose an accessible name and role to assistive technology | Platform accessibility labels in source, an inspector result, or source review by the assessing agent |
| <a id="x03"></a>X03 | Text contrast and text sizing respect platform settings, and meaning is never conveyed by colour alone | Design tokens, a review of the source by the assessing agent, or a documented check |
| <a id="x04"></a>X04 | Command-line and terminal output stays usable without colour and without Unicode decoration | A documented plain-output or no-colour mode |
| <a id="x05"></a>X05 | Known accessibility limitations are stated rather than left implicit | README or a dedicated accessibility note |

The assessing agent decides `X01` to `X03` by reading source, and records in the
linked evidence what it read and what it found. It does not need to run the
product.

- **`X01`.** For a website or web application, read for controls that are not
  reachable or operable by keyboard (click handlers on non-interactive elements
  with no `tabindex` and key handler, positive `tabindex` values that break
  order) and for a suppressed focus outline with no replacement. For a native
  application, read for gesture-only interactions with no keyboard or
  accessibility equivalent, and for custom controls that replace standard ones.
  Standard platform controls are keyboard operable and show focus by default.
  `Pass` where no control found in the reviewed source is unreachable by
  keyboard and no focus indicator is suppressed, or where a documented manual
  check or automated test says so. `Partial` where one or more named controls
  are affected but the main flow is operable. `Fail` where the main flow is not
  operable by keyboard. A command-line tool with no interactive full-screen
  interface is `Pass`, because the terminal is keyboard-operated; record that as
  the reason. Where a native application offers no source-level signal either
  way, record `Partial` and state that the assessment is limited to source.
- **`X02`.** An interactive element is a control a user activates or edits.
  Read for an accessible name on each: a text label, `aria-label`, `<label>`,
  `accessibilityLabel`, `accessibilityIdentifier`, or `AutomationProperties`
  equivalent, with icon-only controls the usual gap. `Pass` where every
  interactive element found has a name and a role, by explicit label or by
  using a standard control that supplies both. `Partial` where some
  interactive elements lack a name in source. `Fail` where none are labelled. A
  text-only command-line tool has no interactive elements and is `Pass` with
  that recorded. A native application with no source-level labels or
  identifiers to read and no inspector result is `Partial`, stating that only
  source was available.
- **`X03`.** Three properties are assessed together, and only evidence against a
  property counts against it: a property the source gives no evidence about is
  taken as holding. Contrast: where the design tokens or stylesheet let it be
  computed, body text is at least 4.5:1 and large text at least 3:1 against its
  background; platform semantic colours meet it by definition.
  Sizing: text sizes use relative units or platform text styles, not fixed
  pixel sizes for body text. Colour: no status or meaning depends on colour
  alone. `Pass` where all three hold in the reviewed source or a documented
  check. `Partial` where at least one holds and a named gap remains in another.
  `Fail` where none holds. A command-line tool is `Pass` here where it sets no
  colours or sizes of its own; its colour use is assessed under `X04`.
- **`X04`.** `Pass` where a plain or no-colour mode is documented, including
  documented support for `NO_COLOR`. `Partial` where a mode exists but is not
  documented. `Not applicable` where the product has no terminal output.
- **`X05`.** `Pass` where limitations are stated, or where the repository states
  explicitly that none are known. `Partial` where a statement exists but omits a
  limitation the assessor found under `X01` to `X03`. `Fail` where there is no
  statement at all.

`X05` is deliberate. Stating a known gap honestly is a `Pass`; leaving a reader
to discover it is not.

## Data Protection And Privacy

Existing criteria cover secrets in the repository. These cover the data the
product handles once it runs.

Applies to the Deployable and Package profiles, and to any repository that
processes user data or contacts a network service.

A repository whose only network contact is build, install, or CI tooling does
not contact a network service in the sense of this section. Where a repository
neither processes user data nor contacts a network service from the product
itself, record `Not applicable` with that rationale for `Y02` to `Y06`; `Y01` is
still answered, with the explicit "none" statement.

Most of these projects are local-first tools with no backend, so the honest
answer is usually that nothing is collected and nothing is sent. The purpose of
this section is to make that answer stated and checkable instead of assumed.

| ID | Requirement | Expected evidence |
|---|---|---|
| <a id="y01"></a>Y01 | The data the product collects, stores, or transmits is stated, including the explicit "none" case | README or privacy note |
| <a id="y02"></a>Y02 | Every outbound network destination and its purpose is documented | README, privacy note, or configuration |
| <a id="y03"></a>Y03 | Telemetry, analytics, and crash reporting are off by default or opt-in, and are disclosed | Source review plus a documented setting, or source review showing none is present |
| <a id="y04"></a>Y04 | Local storage locations for user data are documented, and the user can find, export, or delete them | README or runbook |
| <a id="y05"></a>Y05 | Third-party services and AI providers that receive user content are named | README or privacy note |
| <a id="y06"></a>Y06 | Retention and deletion behaviour is stated where data outlives a session | README, runbook, or an explicit not-applicable result |

`Y01` is load-bearing. A single sentence such as "this application stores all
data locally and contacts no network service" is a `Pass`.

The assessing agent decides these by reading the README or privacy note and
comparing it with source: network libraries and URLs (`fetch`, `requests`,
`URLSession`, and the like), analytics and crash-reporting dependencies, and the
paths the code writes to.

- **`Y01`.** There is no `Not applicable` result. `Pass` where the statement is
  present and source does not contradict it. `Partial` where the statement omits
  something the source shows. `Fail` where there is no statement, or where it
  says none and source collects or transmits.
- **`Y02`.** A destination counts when the product's own code contacts it at run
  time, including default update checks. Build and install tooling, and hosts the
  user supplies themselves, do not count, though a user-configurable endpoint is
  named as such. `Pass` where every destination found in source is documented
  with its purpose, or where the product contacts none and says so. `Partial`
  where the list omits a destination found or is a sample. `Fail` where none is
  documented and the code contacts one.
- **`Y03`.** Where no telemetry, analytics, or crash reporting is present in
  source or dependencies, that is `Pass`, and no setting need be documented.
  Where present, `Pass` when it is off by default or opt-in and disclosed
  (disclosure in the `Y01` or `Y02` text counts), `Partial` when it is off or
  opt-in but not disclosed, and `Fail` when it is on by default.
- **`Y04`.** Documenting where user data is stored is enough for `Pass`, where
  the location is an ordinary file or directory the user can reach. `Partial`
  where only some locations are documented. `Fail` where the product writes user
  data and no location is documented. `Not applicable` where the product writes
  no user data.
- **`Y05`.** `Pass` where every third party or AI provider found in source that
  receives user content is named, or where `Y01` and `Y02` state that none does.
  `Partial` where some are named and one found is missing. `Fail` where the code
  sends content to one and none is named.

These criteria describe disclosure, not legal process. They do not require a
record of processing, a data protection agreement, or legal review. They also do
not restate the secret-handling requirements in `S05`, `S06`, `S07`, and `D02`.

## Automation Availability

Several criteria name a workflow run as their evidence, and one required badge
reports one. A repository with no runner cannot produce any of it, and none of
those criteria say what an assessor records instead. This section says it once,
because a rule restated in every criterion drifts.

**The property is the runner, not the visibility.** A repository is *without
automation* when no runner is available to it: no self-hosted runner it can use,
and no hosted minutes it can spend. Private repositories are the common case,
because hosted minutes there are metered and billable rather than free, but
visibility does not decide it. A private repository with a self-hosted runner
has automation available. A public repository whose account has disabled Actions
does not.

**It has to be recorded before it can be used.** A repository in this state says
so in the evidence its conformance record links to, in one sentence naming the
absence and the reason for it. Without that sentence the assessor records the
ordinary result, because an unstated possibility is not evidence and cannot be
checked by anyone else. Recording it also keeps the answer honest as the
repository changes: the sentence has to be removed when a runner appears.

Where the state applies and is recorded, these results replace the ordinary
ones:

| Which criteria | Result when no runner is available |
|---|---|
| Those satisfied by a check the repository owns, which a runner only makes convenient. At this version `S02`, `S03`, `S05`, and `L04` | `Fail` where the check does not exist; otherwise `Pass` where the documented `B05` command, or for `S05` the documented scan command, runs the check and the evidence the conformance record links to records a successful run of that command, and `Partial` where it does not. A criterion's own boundaries still decide any further `Partial`, as `S02` and `S03` state |
| Those whose evidence can only be produced by a workflow run. At this version `S04`, `S09`, `P09`, and `P13` | `Not applicable` |

**Membership is decided by the property, not by the list.** Each list names the
criteria that match at the version on the cover, and is there so an assessor can
work without re-deriving it. A criterion added later is decided by the row it
matches, whether or not anyone remembered to extend the list — a list stops being
true the moment the document grows, and a property does not.

The split is between a capability and a gate. A test suite, a linter, and a
catalog check are things the repository owns; a runner only makes them
convenient, and `B05` already requires the command that runs them, so the
evidence exists without CI and `Pass` is the honest result. A matrix, a required
check, and a generated activity card are not properties of the
repository at all — they are things a runner does. Where there
is no runner, there is nothing to assess, which is what `Not applicable` means
everywhere else in this document.

`P09` needs its membership shown rather than asserted. It requires a card a
workflow reproduces and regenerates on a schedule, and states outright that a
committed SVG no workflow reproduces is a `Fail`, so a repository with no runner
has no reachable result but that one. The `Not applicable` covers the repository
that publishes no card. It does not licence one: a repository that commits a card
and presents it as generated remains a `Fail`, because that is a false claim
rather than an absence, and this section excuses what a repository cannot
produce, never what it misrepresents.

The first row turns on one property, whether the check exists, so every
repository lands on exactly one of its three results. A check that does not
exist is a `Fail`. A check that exists is a `Pass` only where both remaining
conditions hold together, and a `Partial` wherever either fails — so a check
that no documented command runs, a check whose documented command produces no
recorded successful run, and a check whose run fails are all `Partial` alike.
None of the three is excused by the absence of a runner, because none of them
is caused by it.

**`P08`.** The CI badge is position 3 of the required block. Where no runner is
available, that position is omitted and the remaining badges keep their order
and their numbering intent; nothing takes its place. Committing an image
asserting a CI status is not the alternative and remains a `Fail` under
[Status Badges](#status-badges), which already rejects a committed image of a
value that moves without a commit — and a badge reporting a result that was
never computed is worse than one that is merely stale.

**Everything else is assessed normally.** A repository with a runner available
that chooses not to use it is not in this state, and its ordinary results stand,
including `Fail`. So does every criterion matching neither row above, including
one whose evidence a workflow run *may* produce but need not: `I06` accepts a
build script, `R04` asks whether a tag, a version, and a title agree rather than
what compared them, `R08` accepts a recorded statement wherever no provenance
mechanism is available to the repository, which a repository with no runner can
write without one, `W01` asks for a repeatable documented process rather than a
workflow, and `S11`, `S12`, and `S13` are properties of a workflow file that
hold whether or not it ever runs. This section narrows the criteria its two rows
describe — eight at this version — and one badge position, and nothing else.

## Status Badges

Badges are the first thing a reader sees. They are held to the same rule as
built artifacts in `I06`: their values are produced from an authoritative source,
not maintained by hand.

Applies to the repositories `P08` applies to, which are the public repositories.

Required badge block, in this order:

1. license;
2. platform or runtime requirement, omitted where the repository states none, as
   a documentation or template repository does not; the omission is `Pass` and
   its reason is recorded;
3. CI status of the default branch, except where
   [Automation Availability](#automation-availability) omits it;
4. latest release, where the repository publishes releases;
5. conformance, where a conformance record exists.

Rules:

- A committed or static image of the conformance badge is a `Pass` where a
  check fails when it disagrees with the conformance record, and otherwise
  follows the drift rule below.
- Every badge links to what it reports: the license file, the manifest or
  documented requirement, the workflow, the release, the conformance record.
- Every badge value is derived from an authoritative source, or is covered by a
  check that fails when it drifts. A badge that a service computes from the
  repository when it is requested, such as a licence badge read from the
  repository's detected licence, is derived and is a `Pass`. A hardcoded value
  duplicating a manifest, such as a fixed platform version, is a `Partial` unless
  a check covers it.
- Badges outside the required and optional sets need a stated reason. A wall of
  badges carries less information than four accurate ones.
- A badge image may be committed to the repository only when a repository event
  regenerates it. License, platform, and conformance qualify, and committing
  them is permitted, never required. CI status and the latest release move
  without a commit, so a committed image of either is stale between
  regenerations. Bounded staleness is acceptable for the activity card in `P09`;
  it is not acceptable for a badge reporting current status.
- Where the authority for a value publishes its own image, use that image.
  GitHub serves a workflow status badge for a repository's own CI, so that badge
  is first-party and live at once. A third-party render of the same value is not
  a `Fail`, but it is the weaker option and reassessment should replace it.
- A live third-party image is a `Pass` for any value with no first-party image,
  whether or not that value would also qualify for committing. Serving a value
  late is worse than serving it from somebody else's host.

A hardcoded `Swift 5.9` badge beside a manifest that has moved to 6.0 is the
failure this section exists to prevent.

Badge hosting is not a privacy question on GitHub. Markdown rendered on
`github.com` loads every external image through GitHub's proxy, so the image host
observes the proxy and not the reader. The `Y02` argument applies where that
proxy does not: a published site fetches images directly into the visitor's
browser, which is why `W07` forbids them there. What remains for a README is an
availability and trust dependency on whoever renders the image.

## Repository Statistics

Badges report state. A statistics card reports activity: commit volume, when the
repository was last touched, the current release, contributor count, language
mix. A reader uses it to judge whether a project is alive before reading any
code.

Results in this section follow the general rules of this standard for a
criterion with several parts; the boundaries below cover only what those rules
leave open.

`P09` applies the same rule the badge section applies to values: the card is
generated from an authoritative source and committed to the repository. It is
not fetched from a third-party rendering service at read time.

The reason is not privacy. GitHub proxies the image, as
[Status Badges](#status-badges) explains. The reason is control: a card fetched
at read time renders whatever a third party decides to render, whenever that
party is available, and no diff ever showed it. A card committed as an SVG was
reviewed when it landed and cannot break because someone else's free tier
expired. On a published site the privacy argument does apply directly, and `W07`
covers it there.

Rules:

- The card is generated, never hand-edited. A committed SVG that no workflow
  reproduces is a `Fail`.
- Generation runs on a schedule, so the card cannot silently age past the
  repository it describes.
- Light and dark variants are published as separate files and selected with a
  `<picture>` element. A `prefers-color-scheme` query inside the SVG has no
  effect through GitHub's image proxy.
- The card embeds no external references: no remote fonts, no `<image href>` to
  another host. It is self-contained or it reintroduces the problem it solves.

- Where the card is committed is not fixed. The workflow may commit it to a
  branch other than the default, for example `stats`, and the README may
  reference it there. That satisfies the rule and is the route where the default
  branch is protected: the scheduled commit never reaches the default branch, so
  neither the pull-request rule nor `S09` applies to it. The card may instead
  reach the default branch through a pull request.
- A card generated from public data needs only the workflow's built-in token. A
  `STATS_TOKEN` secret is needed only to count private repositories and is never
  a requirement of `P09`. The assessing agent does not create it; a card that
  can be reproduced without it is what is assessed.

Results. `Pass` where a workflow generates the card on a schedule, in light and
dark variants, with no external references. `Partial` where the card is
generated but lacks a variant, a schedule, or self-containment. `Fail` where the
card is a third-party image, or a committed SVG no workflow reproduces. Where a
runner is available and no card is published, the result is `Fail`, because the
criterion asks that activity is shown from a generated source. Where no runner
is available, [Automation Availability](#automation-availability) gives
`Not applicable`.

The shared implementation is the reusable workflow described in
[Repository Stats](repo-stats.md). A repository may generate the card another
way; the criterion is about the property, not the tool.

Both of the first two rules need a runner. Where none is available,
[Automation Availability](#automation-availability) states what is recorded
instead.

## Conformance Records

`B11` requires a conformance record: the machine-readable result of assessing a
repository against a named version of this standard.

The record is the source of truth. The conformance badge renders it and can
never disagree with it, because no badge value is editable on its own.

| Field | Meaning |
|---|---|
| `standard_version` | The version assessed against, matching a published tag |
| `assessed_on` | The date the assessment was completed |
| `state` | One of the states defined in [Assessment](#assessment) |
| `criteria` | Every criterion in the catalog, each with a result |
| `evidence` | Link to the assessment output holding the per-criterion notes |

Every criterion in the catalog appears in the record. A criterion that does not
apply is recorded as `na` with its rationale in the linked assessment, so the
difference between "does not apply" and "was never looked at" stays visible.

Rules:

- The badge shows the states defined in this document. `Pass` stays a
  per-criterion result and is never used as a repository-level state, because one
  word with two meanings makes both useless.
- A record carries an assessment date, and a record older than the review cadence
  renders as stale rather than as its last known result. An assessment from two
  years ago is not evidence.
- Where no record exists, no badge is shown. A permanent "unknown" badge is
  worse than an absent one.
- No numeric score or percentage is derived from a record. State is assigned by
  impact, and a score would quietly replace that judgement.

The format and a worked example are documented in
[Conformance Record Format](conformance-record.md).

## Archived Repositories

Archived repositories do not need to satisfy the active baseline.

| ID | Requirement | Expected evidence |
|---|---|---|
| <a id="a01"></a>A01 | GitHub archive state is enabled | GitHub settings |
| <a id="a02"></a>A02 | README states why and when maintenance ended | `README.md` |
| <a id="a03"></a>A03 | A successor or migration destination is linked when one exists | `README.md` |
| <a id="a04"></a>A04 | No active deployment or undocumented dependency remains | Deployment records, Pages status, scheduled workflows, published packages, and dependents the README names |

The Archived profile applies once GitHub reports the repository as archived, so
`A01` is met by the fact that placed the repository here. The assessor still
reads the flag with `gh repo view --json isArchived` and records it, because the
flag can be lifted. `A01` is `Pass` when it is set and `Fail` when it is not.
A repository whose README says development has ended but which is not archived is
not in this profile. It is assessed against the baseline, its `B10` records the
status, and `A01`-`A04` are `Not applicable` with the rationale that it is not
archived. Archiving it is a maintainer action, and the linked evidence may note
that it is outstanding.

The baseline and the criteria of every other profile do not need to be satisfied
by an archived repository. Each is recorded `Not applicable` with the rationale
that the repository is archived, except `B11`, which keeps its ordinary result.

`A02` is `Pass` when the README says why maintenance ended and gives a date, in
the year or more precisely; `Partial` when it gives one and not the other; and
`Fail` when it says nothing.

`A03` is `Not applicable` when the assessor has read the README, the description,
and the homepage and finds no successor or migration destination named, and the
record says where it looked. It is `Pass` when one is named and linked in the
README, `Partial` when it is named without a link, and `Fail` when it is named
only outside the README.

`A04` reads what the repository exposes: `gh api repos/OWNER/REPO/deployments`,
`gh api repos/OWNER/REPO/pages`, `gh workflow list` for an enabled scheduled
workflow, the releases and packages it publishes, and the dependents its README
names. An active deployment is one of those still serving or running. An
undocumented dependency is a named dependent the README does not mention as
affected. What lives on an operator's own host cannot be seen, and the record
says it was not visible, then decides from what was. Neither found is `Pass`,
exactly one is `Partial`, and both is `Fail`.

## Assessment

An assessment is made by whoever reads the evidence, and that is normally an AI
agent working in the repository. A maintainer is not required to perform it or to
be present for it. What makes a record valid is the evidence it links and the
date it was made, not the identity of the assessor. The assessing agent uses
[Drafting A Conformance Record](assessing.md) and states in the linked evidence
what it read.

Use one result for every applicable criterion.

| Result | Meaning |
|---|---|
| Pass | Requirement is met and evidence is linked |
| Partial | Evidence exists, but a material part is missing |
| Fail | Requirement applies and is not met |
| N/A | Requirement does not apply and the rationale is recorded |

`unknown` is a draft marker in a generated record and is never a result. The
validation rejects a record that still contains one, because it stands for
evidence nobody has inspected.

### Deciding Without The Maintainer

The assessor reaches every result itself and does not leave a question for the
maintainer. `Unknown` is a draft state, not a result. Where the right result is
unclear, apply these in order and stop at the first that fits.

1. The requirement is met as written: `Pass`.
2. The property is met by other means than the evidence column names: `Pass`,
   with the means named in the linked evidence.
3. The repository cannot meet the requirement, or should not be asked to, for one
   of the reasons in the table below, and the assessor has checked that the
   reason holds: the result in the table, with the reason and the check recorded.
4. Otherwise the gap is real: `Partial` where a material part is missing, `Fail`
   where none of it is met.

**Default results.** These apply wherever a criterion does not state its own
boundaries, and a criterion that states them keeps them.

- A criterion with several parts, whether listed in the requirement, the evidence
  column, or joined by "and": every part met is `Pass`, at least one met and at
  least one missing is `Partial`, and none met is `Fail`. A criterion with a
  single part is `Pass` or `Fail`.
- `Not applicable` where the repository has nothing the criterion is about, such
  as no workflows for a workflow criterion, no user-facing strings for a
  localization criterion, or no interface for an accessibility criterion. Every
  `Not applicable` records one sentence naming the fact and what was looked for;
  the fixed sentences some sections give are instances of it. This differs from
  an intended deviation: the requirement does not reach the repository at all.
- A criterion applies to the current state of the repository and to its latest
  published release, not to every release that ever existed.

**Judgement words.** Where a criterion uses a word that needs a threshold, such
as important, actionable, non-obvious, where practical, covers, or intentional,
the assessor applies the reading a maintainer of a small project would accept,
states that reading in the linked evidence, and applies it the same way in every
repository it assesses. Stating a reading is not a defect. Leaving it unstated
is, because a later reader cannot check a result against a threshold they cannot
see.

A deviation is *intended* when the repository has a reason for it. These are the
reasons that make one intended. A reason that is not in the table is not one.

| Reason | What the assessor checks | Result |
|---|---|---|
| The platform does not offer the capability: no runner, no ruleset on the plan, no provenance in the ecosystem, no way to operate an interface without an operator | The absence is real, read from settings, plan, or ecosystem, and not merely asserted | The result the criterion or [Automation Availability](#automation-availability) states; otherwise `Not applicable` |
| The property is met by cheaper means than the criterion names, which suits a single-maintainer project | The other means exists and gives the consumer the same assurance | `Pass` |
| The criterion assumes a wider scope than the repository claims: one supported platform, one language, one audience | The repository claims only that scope and the criterion is met within it | `Pass` |
| The repository states the choice and its reason in its README, `AGENTS.md`, or the linked evidence, and the criterion's own text allows a stated choice | The statement is true and gives a reason from this table | `Pass` |

A choice the repository has stated but that the criterion's text does not allow
is a `Partial`, recorded as intended and with its reason. It stays visible so a
later reader can see it was decided, and it does not lower the state below,
because only a `Fail` does.

**Intent does not excuse the critical and high-priority criteria** named under
[Overall State](#overall-state): `B04`, `D01`-`D04`, `D06`, `B02`, `B03`, `P01`,
`B05`, `S02`, `B07`, `S08`, `S01`, `R03`, and `R04`. A repository may have a
reason for missing one of them, and the result is still the ordinary one.

Where evidence cannot be read at all, such as a setting the token cannot see, the
assessor records the result the readable evidence supports and states what it
could not read. It does not leave the criterion open for the maintainer.

A maintainer who disagrees with a result disputes it through an issue, as
[Changing This Standard](#changing-this-standard) describes. Nothing has to be
approved beforehand.

### Overall State

Assign the overall state by impact, not by percentage. The state follows from the
recorded results, so an assessor reaches it without a further judgement and two
assessors with the same results reach the same state.

| State | Rule |
|---|---|
| Healthy | No criterion is `Fail`. `Partial` and `N/A` results, including intended ones, do not lower the state |
| Needs work | At least one criterion is `Fail`, and none of the critical criteria below is |
| At risk | A critical criterion is `Fail` |
| Archive candidate | `B10` and `B02` are both `Fail`, and no other repository in the account references this one |
| Archived | The repository is archived and `A01`-`A04` are met |

The critical criteria are the ones whose failure means a committed secret, an
exposed write-capable service, missing recovery for irreplaceable state, or an
active deployment with no known source or configuration:

| Criterion | Why its failure is critical |
|---|---|
| `B04` | A secret is committed to the repository |
| `D01` | An active deployment has no documented target or command, so its source and configuration are unknown |
| `D02` | An active deployment's secrets are committed or have no documented safe location |
| `D03`, `D06` | An active deployment has no health check or way back, or risks irreplaceable state |
| `D04` | A deployment's runtime and infrastructure are unconstrained. No criterion measures an exposed write-capable service directly, and this is the nearest one |

The high-priority criteria, which are named so that intent cannot excuse them, are
the ones that stand for no README (`B02`), ambiguous licensing (`B03`, `P01`), no software
validation (`B05`, `S02`), unsupported dependencies (`B07`, `S08`), and
unreproducible releases (`S01`, `R03`, `R04`). Their failure gives `Needs work`
like any other, and
[Deciding Without The Maintainer](#deciding-without-the-maintainer) explains why
intent does not change it.

## Changing This Standard

A standard that can be cited but not contested puts every disagreement out of
reach of the person holding the evidence. This section states what to do with
one.

**A criterion that cannot be applied is a defect in the criterion.** If reaching
a result requires an intention the rule text does not state, the text is
unfinished. The assessor still records a result: the one the rule text supports
on its plain reading, with that reading stated in the linked evidence. It then
reports the defect as an issue against the repository publishing this document,
which is a report to the standard and not a question to the repository's
maintainer. See
[decision 0011](decisions/0011-criteria-are-decided-by-the-rule-text.md).

**Proposals and disputes both go in an issue against the repository publishing
this document.** A proposal names the criterion, what it fails to decide or
fails to catch, and a repository the change would score differently. A dispute
names the criterion, the recorded result, and the evidence the assessor did not
have. Neither needs a template; both need the criterion identifier, because that
is what makes the discussion locatable later.

**The maintainer decides.** There is no committee, review period, or vote, and
inventing one would describe a process nobody runs. What the decision owes is
durability: a change that alters how a criterion is applied gets a decision
record, so the reasoning survives the issue thread that produced it.

**A disputed result is resolved by reassessing, not by editing the record.** The
record follows the evidence. If the evidence was misread, the reassessment
produces a different result and the assessment date moves with it. If the
criterion was wrong, the criterion changes and every repository assessed against
the old version keeps its recorded result, because that result names the version
it was produced with.

**A repository records the result its evidence supports, with the reason.**
Where a criterion applies and the repository knowingly does not meet it,
[Deciding Without The Maintainer](#deciding-without-the-maintainer) says which
result that is. A stated reason never changes a result the evidence does not
support: it is recorded next to the result, not in place of it, and an `N/A` that
claims the criterion does not apply when it does is not available.

One structural note, because it is not obvious and invites an incorrect fix. The
issue forms in the publishing repository are inherited by every repository in
the account that does not define its own, so a form specific to this document
cannot be added there without it appearing in repositories that have nothing to
do with it. That is why proposals and disputes are ordinary issues.

## Remediation Issue Contract

Every remediation issue must be executable without private context. For every
scope item, include:

- the criterion ID and observed gap;
- required content or configuration, not only a file or setting name;
- expected evidence, such as a recognized community file, green workflow,
  release asset, or repository-setting result;
- concrete acceptance criteria under `Done when`; and
- explicit exclusions for working behavior that must be preserved.

For example, `add SECURITY.md` is insufficient. Require supported versions, a
private reporting path, response expectations, and guidance against public
disclosure. Likewise, `protect main` must name existing checks, require the
branch to be current before merge, and block force pushes and deletion. Never
require a check that does not exist.

## Recommended Shape

Use only files that serve the repository's profiles. Empty governance files are
not evidence of quality.

```text
AGENTS.md
README.md
LICENSE
SECURITY.md
CONTRIBUTING.md
CODE_OF_CONDUCT.md
CHANGELOG.md
.gitignore
.github/
  CODEOWNERS
  conformance.yml
  copilot-instructions.md
  dependabot.yml
  github-app.yml
  ISSUE_TEMPLATE/
  pull_request_template.md
  workflows/
    ci.yml
    release.yml
docs/
  decisions/
site/
  index.html
  assets/
tests/
```

Equivalent evidence is valid when it is durable, discoverable, and testable.

## Implementation Guides

The criteria say what must be true. This repository also publishes how to make it
true, so that neither a maintainer nor an agent has to work it out again in every
repository:

- [Guides](guides/README.md) map each criterion to a worked example.
- [Reusable workflows](../.github/workflows/) are referenced from another
  repository in the account as `trsdn/.github/.github/workflows/NAME.yml@main`,
  which `S12` permits, so a repository has no copy to drift.
- [Templates](../templates/) are starting points to copy where a file has
  per-repository content: a starter kit per language family and one for macOS
  applications.
- [Packages](../packages/) are versioned agent packages, such as a reviewer with
  its rules, that a repository installs with the Agent Package Manager and pins to
  a tag, so the agent runs locally and updating it is a version change.

Where a guide or a template disagrees with a criterion, the criterion decides. A
guide or template is never evidence that a criterion is met, only the repository's
own files are, so an assessor reads what the repository contains and not what it
was copied from.
