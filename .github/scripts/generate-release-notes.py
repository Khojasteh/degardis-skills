"""Generate release notes for a complete snapshot of bundled skills."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import yaml


def discover_skills(root: Path) -> list[Path]:
    """Find skill directories using Degardis's stop-at-skill discovery rule."""
    manifests: list[Path] = []

    for directory, child_directories, filenames in os.walk(root):
        child_directories.sort()
        if "skill.yaml" in filenames:
            manifests.append(Path(directory) / "skill.yaml")
            child_directories.clear()

    return manifests


def load_skill(manifest: Path) -> tuple[str, str, str]:
    data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    try:
        return str(data["title"]), str(data["name"]), str(data["version"])
    except (KeyError, TypeError) as error:
        raise ValueError(f"{manifest} is missing title, name, or version") from error


def render_notes(skills_root: Path) -> str:
    skills = sorted(
        (load_skill(manifest) for manifest in discover_skills(skills_root)),
        key=lambda skill: skill[0].casefold(),
    )

    names = [name for _, name, _ in skills]
    if len(names) != len(set(names)):
        raise ValueError("Skill names must be unique")

    lines = [
        "Ready-to-install ZIP archives for every skill in this repository.",
        "",
        "Each archive contains all profiles available for that skill.",
        "",
        "| Skill | Version | Asset |",
        "| --- | --- | --- |",
    ]
    lines.extend(
        f"| {title} | `{version}` | `{name}.zip` |"
        for title, name, version in skills
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skills", type=Path, default=Path("skills"))
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()

    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        render_notes(arguments.skills),
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
