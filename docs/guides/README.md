# Guides

The [standard](../repository-quality-standard.md) says what must be true. These
guides and the [templates](../../templates/) say how to make it true, with worked
examples taken from repositories that already meet the criteria. A guide never
replaces the criterion: where they disagree, the criterion decides, and a copied
file is not evidence until the repository has it and it works there.

## By criterion

Every criterion has something here. Some rows name a skill or a kit; others say
that the answer is a convention, or that the account already supplies it and
there is nothing to do. "No tooling" is a complete answer and is written as one,
because a criterion with no row reads as an oversight even when it is not.

| Criteria | Read |
|---|---|
| The Baseline: [`B01`](../repository-quality-standard.md#b01)-[`B04`](../repository-quality-standard.md#b04), [`B06`](../repository-quality-standard.md#b06)-[`B10`](../repository-quality-standard.md#b10), and [`P01`](../repository-quality-standard.md#p01), [`P02`](../repository-quality-standard.md#p02), [`P04`](../repository-quality-standard.md#p04)-[`P07`](../repository-quality-standard.md#p07) | [The repo-setup skill](../../skills/repo-setup/SKILL.md), which audits them and applies the mechanical ones |
| [`P03`](../repository-quality-standard.md#p03), [`P12`](../repository-quality-standard.md#p12), [`S05`](../repository-quality-standard.md#s05), [`B16`](../repository-quality-standard.md#b16), [`S09`](../repository-quality-standard.md#s09) | [Repository security settings](repository-security-settings.md) |
| [`P13`](../repository-quality-standard.md#p13) | [CodeQL](codeql.md) |
| [`I01`](../repository-quality-standard.md#i01)-[`I06`](../repository-quality-standard.md#i06) | [The product-identity skill](../../skills/product-identity/SKILL.md), which reads what the artifact embeds and where it comes from |
| [`Y01`](../repository-quality-standard.md#y01)-[`Y06`](../repository-quality-standard.md#y06) | [The privacy-disclosure skill](../../skills/privacy-disclosure/SKILL.md), which finds what the product contacts and stores |
| [`L01`](../repository-quality-standard.md#l01)-[`L07`](../repository-quality-standard.md#l07) | [The localization skill](../../skills/localization/SKILL.md), whose catalog check is the command `L04` asks for |
| [`S01`](../repository-quality-standard.md#s01), [`S06`](../repository-quality-standard.md#s06), [`S07`](../repository-quality-standard.md#s07), [`S10`](../repository-quality-standard.md#s10), [`X04`](../repository-quality-standard.md#x04) | [The software-practices skill](../../skills/software-practices/SKILL.md), which reads setup, configuration, logs, architecture and terminal output |
| [`R01`](../repository-quality-standard.md#r01), [`R02`](../repository-quality-standard.md#r02), [`R06`](../repository-quality-standard.md#r06) | [The release-hygiene skill](../../skills/release-hygiene/SKILL.md), which compares the manifest with the repository and reads the latest release |
| [`D01`](../repository-quality-standard.md#d01)-[`D06`](../repository-quality-standard.md#d06) | [The deployment-runbook skill](../../skills/deployment-runbook/SKILL.md), for anything that runs without being started |
| [`G04`](../repository-quality-standard.md#g04) | [The agent-instructions skill](../../skills/agent-instructions/SKILL.md), which finds where a tool file has drifted from `AGENTS.md` |
| [`A01`](../repository-quality-standard.md#a01)-[`A04`](../repository-quality-standard.md#a04) | [The archive-safely skill](../../skills/archive-safely/SKILL.md), which checks nothing is still loaded before you archive |
| [`P10`](../repository-quality-standard.md#p10), [`P11`](../repository-quality-standard.md#p11) | Nothing to build: a public repository with no forms of its own inherits [the account's issue forms](../../.github/ISSUE_TEMPLATE/) and [pull-request template](../../.github/pull_request_template.md), whose fields are the ones these two name. Ship your own only where this repository needs different ones |
| [`T02`](../repository-quality-standard.md#t02) | The [documentation kit](../../templates/docs/README.md) ships the link and Markdown checks; copy them rather than writing one |
| [`T04`](../repository-quality-standard.md#t04) | Convention, not tooling: a generated file carries a header naming the script that writes it and saying not to edit it by hand, as [`standard.yml`](../../standard.yml) does |
| [`X02`](../repository-quality-standard.md#x02), [`X03`](../repository-quality-standard.md#x03) | [The Apple HIG review package](../../packages/apple-hig-review/README.md) for a macOS or iOS interface. For a terminal program, [`X04`](../repository-quality-standard.md#x04) is in the [software-practices skill](../../skills/software-practices/SKILL.md) |
| [`X01`](../repository-quality-standard.md#x01), [`X05`](../repository-quality-standard.md#x05) | [The Apple HIG review package](../../packages/apple-hig-review/README.md). `X05` needs no tooling: state the limitations you know about, and "none known" is a valid statement |
| [`B05`](../repository-quality-standard.md#b05), [`G05`](../repository-quality-standard.md#g05) | One documented command that validates the repository. Every starter kit in [templates](../../templates/) ships one; `G05` is that same command named in `AGENTS.md` |
| [`G01`](../repository-quality-standard.md#g01)-[`G03`](../repository-quality-standard.md#g03), [`G06`](../repository-quality-standard.md#g06), [`G07`](../repository-quality-standard.md#g07) | [The `AGENTS.md` template](../../templates/AGENTS.md), which has a section for each. `G07` is a habit rather than a file: agent-authored commits carry a `Co-authored-by` trailer |
| [`B12`](../repository-quality-standard.md#b12) | No tooling: add the `trsdn-standard` topic when a repository is assessed. That topic is what makes the set countable |
| [`B14`](../repository-quality-standard.md#b14) | No tooling: one paragraph naming who revokes an exposed credential, where, and what else has to change. [`SECURITY.md`](../../SECURITY.md) is inherited and does not answer this for your repository |
| [`P08`](../repository-quality-standard.md#p08), [`P09`](../repository-quality-standard.md#p09) | [The statistics card](../repo-stats.md) and its [README snippet](../../templates/repo-stats/README-snippet.md). `P08` needs no tooling: the badge block follows the order the criterion gives |
| [`S04`](../repository-quality-standard.md#s04), [`R04`](../repository-quality-standard.md#r04) | The [macOS](../../templates/macos-app/README.md), [Python](../../templates/python/README.md), [Node](../../templates/node/README.md) and [.NET](../../templates/dotnet/README.md) kits: their CI matrices cover `S04`, and their release workflows derive the tag, version and title from one source for `R04` |
| [`S14`](../repository-quality-standard.md#s14), [`REC-01`](../repository-quality-standard.md#recommendations) | Retired as a criterion at 1.28.0 and kept as a recommendation, so nothing here is assessed. [The performance-review package](../../packages/performance-review/README.md) is one way to run the review it suggests |
| [`T01`](../repository-quality-standard.md#t01), [`T03`](../repository-quality-standard.md#t03) | [`README.template.md`](../../templates/docs/README.template.md) in the documentation kit, which carries both as headings to fill in |
| Any private repository, and [`R09`](../repository-quality-standard.md#r09) | [Private repositories](private-repositories.md), the [account's capabilities](../account-capabilities.md), and the [local gate](../../templates/local-gate/README.md) |
| A public application's site: [`W01`](../repository-quality-standard.md#w01)-[`W09`](../repository-quality-standard.md#w09) | [Site design](site-design.md) |
| [`S08`](../repository-quality-standard.md#s08), [`P12`](../repository-quality-standard.md#p12) | [Dependabot version updates](dependabot.md) |
| [`S05`](../repository-quality-standard.md#s05) | [Secret scanning](secret-scanning.md) |
| [`S11`](../repository-quality-standard.md#s11), [`S12`](../repository-quality-standard.md#s12), [`S13`](../repository-quality-standard.md#s13) | [Workflow permissions and pinning](workflow-permissions-and-pinning.md) |
| [`S02`](../repository-quality-standard.md#s02), [`S03`](../repository-quality-standard.md#s03) | [Tests and lint](tests-and-lint.md) |
| [`B11`](../repository-quality-standard.md#b11) | [The first conformance record](../../templates/conformance-first-record.md) |
| Any workflow that several repositories share | [Reusable workflows](reusable-workflows.md) |
| A macOS application: `R03`, `R05`, `R07`, `R08`, `R09`, `I01`-`I06`, `B15`, `G08`, `S03`, including a private app with no minutes | [Bringing a macOS app to the standard](macos-app.md) |

## Starter kits

Copy the kit for the repository's language family, edit the `TODO(...)` markers,
and read its README first. Each kit says which criteria its files serve.

| Kit | For |
|---|---|
| [`templates/macos-app/`](../../templates/macos-app/README.md) | A Swift package or Xcode macOS application, with the Apple Human Interface Guidelines review agent |
| [`templates/python/`](../../templates/python/README.md) | A Python project |
| [`templates/node/`](../../templates/node/README.md) | A Node or TypeScript project |
| [`templates/dotnet/`](../../templates/dotnet/README.md) | A .NET project, including CodeQL for C# |
| [`templates/docs/`](../../templates/docs/README.md) | A repository of documentation or content |
| [`templates/local-gate/`](../../templates/local-gate/README.md) | The release gate for a repository without automation |

Versioned agent packages are under [`packages/`](../../packages/apple-hig-review/README.md),
run locally and pinned to a tag: the Apple HIG review agent for a macOS app, a
[performance reviewer](../../packages/performance-review/README.md) for any
language, a [documentation staleness reviewer](../../packages/doc-staleness-reviewer/README.md)
for `T05`/`B13`, a [frontend designer](../../packages/frontend-designer/README.md)
and a [site content reviewer](../../packages/site-content-reviewer/README.md) for
`W01`-`W09` (see the [site design guide](site-design.md)), a
[kit customizer](../../packages/kit-customizer/README.md) that resolves a
freshly copied starter kit's markers against the real code, and [the
repository assessor](../../packages/repo-assessor/README.md), which files a
remediation issue per gap and needs the operator's own `gh` write access to do
it.

Older single-purpose templates remain:
[`templates/AGENTS.md`](../../templates/AGENTS.md),
[`templates/release-notes/`](../../templates/release-notes/), and
[`templates/repo-stats/`](../../templates/repo-stats/).

## Bringing many repositories up

[Bringing every repository to the standard](../fleet-rollout.md) is the procedure
for agents that raise a whole account, one repository at a time.

## Shared workflows

These are referenced from another repository in the account instead of copied, as
`trsdn/.github/.github/workflows/NAME.yml@main`. [The guide](reusable-workflows.md)
lists them, their inputs, and how to change one without breaking its callers.
