# Degardis Skills

A collection of AI agent skills in the source format validated and compiled by
[Degardis](https://pypi.org/project/degardis/).

Browse the catalog to find a skill for the work you want an agent to perform,
then build that skill for your agent or upload it to ChatGPT.

<!-- BEGIN GENERATED: root catalog -->
## Available skills

| Skill | Version | License | Category | What it helps with |
| --- | --- | --- | --- | --- |
| [Degardis Authoring](skills/degardis-authoring/) | `1.0.0` | [MIT](LICENSE) | Authoring | Guide an agent in writing and reviewing AI agent skills in the Degardis source format, then use Degardis to compile them into installable AI agent skill bundles. |
| [Codebase Assessment](skills/codebase-assessment/) | `1.0.0` | [MIT](LICENSE) | Software engineering / Assessment | Assess repository health and produce a prioritized improvement roadmap. |
| [Code Review](skills/code-review/) | `1.0.0` | [MIT](LICENSE) | Software engineering / Assessment | Find actionable correctness, security, reliability, and regression risks. |
| [Feature Implementation](skills/feature-implementation/) | `1.0.0` | [MIT](LICENSE) | Software engineering / Development | Design, implement, and verify new software behavior. |
| [Bug Fixing](skills/bug-fixing/) | `1.0.0` | [MIT](LICENSE) | Software engineering / Development | Diagnose defects, implement causal fixes, and verify regressions. |
| [Refactoring](skills/code-refactoring/) | `1.0.0` | [MIT](LICENSE) | Software engineering / Quality | Improve code structure without changing observable behavior. |
| [Testing](skills/code-testing/) | `1.0.0` | [MIT](LICENSE) | Software engineering / Quality | Plan, write, improve, and diagnose software tests. |
| [Performance Optimization](skills/performance-optimization/) | `1.0.0` | [MIT](LICENSE) | Software engineering / Quality | Measure bottlenecks and verify performance improvements. |
| [Documentation](skills/code-documentation/) | `1.0.0` | [MIT](LICENSE) | Software engineering / Quality | Create and improve verified software documentation. |
| [Dependency Upgrade](skills/dependency-upgrade/) | `1.0.0` | [MIT](LICENSE) | Software engineering / Modernization | Upgrade dependencies while preserving supported behavior. |
| [Technology Migration](skills/technology-migration/) | `1.0.0` | [MIT](LICENSE) | Software engineering / Modernization | Replace technologies with target-native designs. |
<!-- END GENERATED: root catalog -->

<!-- BEGIN GENERATED: root installation -->
## Install skills

Each skill's README links to its latest packaged version in ZIP format and
provides instructions tailored to that skill.

### Use a packaged skill

> **General security warning:** Before installing any third-party AI agent
> skill, review its instructions and executable scripts, and confirm that
> you trust its source.

Choose a skill from the catalog, open its README, and download its latest
packaged version in ZIP format.

#### Filesystem-based agents

Choose where the skill should be available:

| Agent | Current project | All projects |
| --- | --- | --- |
| Claude | `.claude/skills/<skill-name>/` | `~/.claude/skills/<skill-name>/` |
| Codex | `.agents/skills/<skill-name>/` | `~/.agents/skills/<skill-name>/` |
| Copilot | `.github/skills/<skill-name>/` | `~/.copilot/skills/<skill-name>/` or `~/.agents/skills/<skill-name>/` |
| Cursor | `.cursor/skills/<skill-name>/` or `.agents/skills/<skill-name>/` | `~/.cursor/skills/<skill-name>/` or `~/.agents/skills/<skill-name>/` |
| Roo | `.roo/skills/<skill-name>/` or `.agents/skills/<skill-name>/` | `~/.roo/skills/<skill-name>/` or `~/.agents/skills/<skill-name>/` |

Paths under **Current project** are relative to the project's root
directory. Paths under **All projects** are personal locations.

On macOS, Linux, and other Unix-like systems, `~/` refers to the current user's
home directory and can be used as written. On Windows, replace a leading `~`
with `%USERPROFILE%` in Command Prompt or File Explorer, or with `$HOME` in
PowerShell. For example, `~/.agents/skills/<skill-name>/` becomes
`%USERPROFILE%\.agents\skills\<skill-name>\` or `$HOME/.agents/skills/<skill-name>/`.

Create one of the directories shown above, extract the ZIP contents directly
into it, and confirm that `SKILL.md` is immediately inside that directory.

When upgrading an installed skill, first empty its existing skill directory,
then extract the new ZIP into that directory. Back up any local modifications
before emptying it.

The cross-agent `.agents/skills` directory is recognized by Codex, Copilot,
Cursor, and Roo. Claude uses `.claude/skills`.

#### ChatGPT

Open [Skills in ChatGPT](https://chatgpt.com/skills), select the **+** button,
choose **Upload from your computer**, and upload the ZIP as-is.
Availability and workspace permissions can vary.
<!-- END GENERATED: root installation -->

### Build from source

To build the authored sources yourself, install Degardis with Python 3.10 or
later:

```console
python -m pip install degardis
```

#### Build for a filesystem-based agent

Choose a target agent and scope from the table above, then remove the final
`<skill-name>/` component to obtain the parent directory for `--output`. From
the repository root, select any source path from the catalog and build it
directly into that parent directory. This example installs
[Bug Fixing](skills/bug-fixing/) for agents
that use the project-level `.agents/skills` directory:

```console
degardis build skills/bug-fixing --output .agents/skills
```

Use the source path of whichever catalog skill you want to install.

To install the complete catalog in that directory:

```console
degardis build skills --output .agents/skills
```

Degardis creates one `<skill-name>/` child beneath the output directory.
Building directly into an agent directory replaces any existing folder or ZIP
with the same skill name. Other skills and unrelated entries remain unchanged.

#### Build for ChatGPT

Choose any source path from the catalog and build that skill as a ZIP archive.
This example packages
[Code Review](skills/code-review/):

```console
degardis build skills/code-review --zip --output .artifacts
```

Open [Skills in ChatGPT](https://chatgpt.com/skills), select the **+** button,
choose **Upload from your computer**, and upload
`.artifacts/code-review.zip` as-is. Availability and workspace permissions can
vary.

## Work with the Degardis source format

[Degardis Authoring](skills/degardis-authoring/) helps an agent work with the
Degardis representation of AI agent skills: `skill.yaml`, workflows, entries,
profiles, scripts, and assets. The agent authors and reviews those sources;
Degardis validates them and compiles them into installable AI agent skill
folders or ZIP archives. This skill is not a general-purpose skill-creation
guide.
