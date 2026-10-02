# Install a skill

Installing a skill usually means putting its folder where your agent already looks for skills. If your AI chat app accepts skill ZIPs, you can upload the archive instead by following the app's own guide. A released skill is already built, so there's nothing to compile or configure. This guide helps you choose the right place and confirm the skill is ready to use.

> [!WARNING]
> Before you install any third-party AI agent skill, read its instructions and executable scripts and make sure you trust the source. Those instructions guide what your agent does.

## Get the package

Choose a skill from the [catalog](../README.md#available-skills), then download its ZIP.

The archive is named after the skill. Throughout this page, `<skill-name>` means that name without `.zip`. For example, `my-skill.zip` becomes the folder name `my-skill`.

If you'd rather use the current source than the latest release, or you maintain changes of your own, you can [build the skill from source](building-from-source.md). The result is the same kind of folder, so the rest of this guide still applies.

## Filesystem-based agents

Most agents read skills from folders on disk, and each agent's documentation lists the folders it reads. Agents update those locations over time, so check the page for yours:

- [Claude Code](https://code.claude.com/docs/en/skills)
- [Codex](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)
- [GitHub Copilot](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)
- [Cursor](https://cursor.com/docs/skills)
- [Roo Code](https://roocodeinc.github.io/Roo-Code/features/skills)

Most agents offer two kinds of location. A folder inside a workspace makes the skill available in that workspace only, and it travels with the workspace. A folder in your home directory makes it available wherever you work.

### Put the skill in place

In the skills folder you chose, create a folder named `<skill-name>` and extract the ZIP into it. Then check that `SKILL.md` sits directly inside that folder, not in a second folder below it. This quick check catches most installations that seem to do nothing.

If you built the skill yourself, copy the built `<skill-name>/` folder into the skills folder instead.

Before you rely on the skill, confirm that it shows up in your agent's skill list or picker. If it doesn't, or it shows up but never seems to be used, the [troubleshooting guide](troubleshooting.md) walks through the usual causes.

### Upgrade an installed skill

To see which version you have, open the installed `SKILL.md` and look for the `version:` line near the top. It's worth including when you report a problem.

To upgrade, empty the skill's folder and extract the new ZIP into it. Emptying it first means no file from the old version is left behind. It also deletes any changes you made to your copy, so back those up before you start.

If a skill's page says it replaces other skills, remove their folders too. A skill left installed beside its replacement competes for the same requests, and the agent may pick the old one.

## Share one copy across agents and environments

If your agents read different folders, you don't have to install the same skill several times. Keep one copy and link to it from each agent's skills folder with a symbolic link. Updates and local changes then happen in one place.

The same works across Windows and WSL. Keep the copy somewhere both can reach, then link each environment's skills folder to it. That's handy when you open the same workspaces from either side.

Check your agent's documentation to see whether it follows linked folders, and confirm the skill shows up through the link before you depend on it.

## Where to next

- [Get good results](using-skills.md): how to phrase a request now that the skill is in place.
- [Build a skill from source](building-from-source.md): when you want the current source, or to modify a skill.
