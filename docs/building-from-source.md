# Build a skill from source

Every skill here starts as source files, and the Degardis compiler turns them into the folder or ZIP you install. Building one yourself is useful when you want changes newer than the latest release, or when you have changes of your own to include.

## Get the source and the compiler

Clone this repository, or download it as a ZIP from GitHub and extract it:

```console
git clone https://github.com/Khojasteh/degardis-skills.git
```

The skills are built with Degardis 2. Its [project page](https://pypi.org/project/degardis/) lists what it needs and how to install it; with pip, that's:

```console
python -m pip install --upgrade "degardis>=2"
```

## Build the skill

From the repository root, build into a folder your agent doesn't read skills from, because a rebuild replaces what's already there:

```console
degardis build skills/<skill-name> --output .artifacts
```

`<skill-name>` is the name of a directory under [`skills/`](../skills/). The build creates `.artifacts/<skill-name>/`, which you install just like an extracted download. For an AI chat app that accepts skills as a ZIP, add `--zip` to get `.artifacts/<skill-name>.zip` instead.

For everything else the compiler can do, see the [Degardis documentation](https://github.com/Khojasteh/degardis/tree/main/docs) or run `degardis manual`.

## Where to next

- [Install a skill](installation.md): where the folder or archive you just built should go.
