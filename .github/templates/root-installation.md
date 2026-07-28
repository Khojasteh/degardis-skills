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
