# Degardis Skills

Give your AI coding agent a clearer way to work. These reusable skills are written in a source format that [Degardis](https://pypi.org/project/degardis/) validates and compiles, so you can inspect what your agent will receive before you install anything. Choose the skill that matches your goal, look through its contents, and put it where your agent looks for skills.

## Available skills

| Skill | Version | Category | Download | What it helps with |
| --- | --- | --- | --- | --- |
| [Degardis Authoring](skills/degardis-authoring/) | `2.0.0` | Authoring | [degardis-authoring.zip](../../releases/latest/download/degardis-authoring.zip) | Guides an agent to create, improve, evaluate, explain, and package Degardis skills with compiler-grounded evidence. |
| [Coder](skills/coder/) | `1.0.0` | Software development | [coder.zip](../../releases/latest/download/coder.zip) | Guides an agent through software work, from investigation and planning to implementation, review, documentation, and verification. |

Open a skill's name to see where it fits, where its limits are, and what a useful request looks like.

To understand the approach shared by the collection—and what still depends on the agent and the run—read [what the skills are designed to do](docs/design-principles.md).

## Getting started

Ready to try one? Download its ZIP from the table, then follow [Install a skill](docs/installation.md). The guide covers agent-specific locations, apps that accept a ZIP, safe upgrades, and sharing one installed copy between agents.

> [!WARNING]
> A skill is a set of instructions your agent may act on. Before installing any third-party skill, including these, inspect its instructions and executable files and make sure you trust the source.

## Documentation

| Guide | Where it helps |
| --- | --- |
| [Install a skill](docs/installation.md) | Put a downloaded or built skill where your agent can use it, upgrade it, or share one copy between agents. |
| [Build a skill from source](docs/building-from-source.md) | Build the current source when no release exists or you want changes newer than the latest release. |
| [Get good results](docs/using-skills.md) | Give an installed skill a clear outcome, useful context, and the right model capability. |
| [Troubleshoot a skill](docs/troubleshooting.md) | Fix a skill your agent cannot see, does not load, skips, or runs unexpectedly. |
| [Understand the design principles](docs/design-principles.md) | See what the published skills aim to do and where their guarantees end. |
| [Ask a question or report a problem](docs/feedback.md) | Share an experience, ask for help, or provide evidence of a reproducible defect. |

## Questions and feedback

Questions, experiences, ideas, and requests for new skills are welcome in [discussions](https://github.com/Khojasteh/degardis-skills/discussions). If you can reproduce a defect, open an [issue](https://github.com/Khojasteh/degardis-skills/issues).

You do not need a polished report. [Ask a question or report a problem](docs/feedback.md) explains which details make feedback useful and includes prompts your agent can use to draft it.

Licensed under the [MIT License](LICENSE).
