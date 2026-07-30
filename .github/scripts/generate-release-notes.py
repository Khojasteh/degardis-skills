"""Generate release notes for a complete snapshot of bundled skills."""

from __future__ import annotations

import argparse
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from template_engine import render_template


@dataclass(frozen=True)
class Skill:
    directory: Path
    title: str
    name: str
    version: str
    summary: str


def discover_skills(root: Path) -> list[Path]:
    """Find skill directories using Degardis's stop-at-skill discovery rule."""
    manifests: list[Path] = []

    for directory, child_directories, filenames in os.walk(root):
        child_directories.sort()
        if "skill.yaml" in filenames:
            manifests.append(Path(directory) / "skill.yaml")
            child_directories.clear()

    return manifests


def load_mapping(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return data


def required_text(data: dict[str, Any], key: str, path: Path) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{path}: {key} must be a non-empty string")
    return value.strip()


def load_skill(manifest: Path) -> Skill:
    skill_data = load_mapping(manifest)
    documentation_path = manifest.with_name("readme.yaml")
    documentation = load_mapping(documentation_path)
    catalog = documentation.get("catalog")
    if not isinstance(catalog, dict):
        raise ValueError(f"{documentation_path}: catalog must be a mapping")

    return Skill(
        directory=manifest.parent,
        title=required_text(skill_data, "title", manifest),
        name=required_text(skill_data, "name", manifest),
        version=required_text(skill_data, "version", manifest),
        summary=required_text(catalog, "summary", documentation_path),
    )


def git(
    repository_root: Path,
    *arguments: str,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", *arguments],
        cwd=repository_root,
        check=False,
        capture_output=True,
        text=True,
    )
    if check and result.returncode:
        detail = result.stderr.strip() or result.stdout.strip()
        raise ValueError(f"git {' '.join(arguments)} failed: {detail}")
    return result


def resolve_previous_ref(
    repository_root: Path,
    release_tag: str,
    requested_ref: str | None,
) -> str | None:
    if requested_ref:
        result = git(
            repository_root,
            "rev-parse",
            "--verify",
            f"{requested_ref}^{{commit}}",
        )
        return result.stdout.strip()

    result = git(
        repository_root,
        "tag",
        "--merged",
        "HEAD",
        "--list",
        "skills-*",
        "--sort=-version:refname",
    )
    for tag in result.stdout.splitlines():
        if tag != release_tag:
            return git(
                repository_root,
                "rev-parse",
                "--verify",
                f"{tag}^{{commit}}",
            ).stdout.strip()
    return None


def skill_status(
    repository_root: Path,
    repository: str,
    release_tag: str,
    skill: Skill,
    previous_ref: str | None,
) -> str:
    if previous_ref is None:
        return "New"

    relative_directory = skill.directory.relative_to(repository_root)
    previous_tree = git(
        repository_root,
        "ls-tree",
        "-d",
        "--name-only",
        previous_ref,
        "--",
        relative_directory.as_posix(),
    )
    if not previous_tree.stdout.strip():
        return "New"

    comparison = git(
        repository_root,
        "diff",
        "--quiet",
        previous_ref,
        "HEAD",
        "--",
        relative_directory.as_posix(),
        check=False,
    )
    if comparison.returncode == 0:
        return "Unchanged"
    if comparison.returncode == 1:
        changelog_url = (
            f"https://github.com/{repository}/blob/{release_tag}/"
            f"{relative_directory.as_posix()}/CHANGELOG.md"
        )
        return f"[Revised]({changelog_url})"
    detail = comparison.stderr.strip() or comparison.stdout.strip()
    raise ValueError(f"Could not compare {skill.name}: {detail}")


def table_cell(value: str, field: str, skill: Skill) -> str:
    if "\n" in value or "|" in value:
        raise ValueError(
            f"{skill.directory}: {field} cannot contain newlines or "
            "vertical bars"
        )
    return value


def render_notes(
    repository_root: Path,
    skills_root: Path,
    repository: str,
    release_tag: str,
    previous_ref: str | None,
    notes_template: str,
    notes_template_path: Path,
    row_template: str,
    row_template_path: Path,
) -> str:
    skills = sorted(
        (load_skill(manifest) for manifest in discover_skills(skills_root)),
        key=lambda skill: skill.title.casefold(),
    )

    names = [skill.name for skill in skills]
    if len(names) != len(set(names)):
        raise ValueError("Skill names must be unique")

    rows = []
    for skill in skills:
        rows.append(
            render_template(
                row_template,
                {
                    "title": table_cell(skill.title, "title", skill),
                    "skill_name": skill.name,
                    "version": table_cell(skill.version, "version", skill),
                    "summary": table_cell(skill.summary, "summary", skill),
                    "status": skill_status(
                        repository_root,
                        repository,
                        release_tag,
                        skill,
                        previous_ref,
                    ),
                    "repository": repository,
                    "release_tag": release_tag,
                },
                row_template_path,
            ).rstrip()
        )

    return render_template(
        notes_template,
        {"release_rows": "\n".join(rows)},
        notes_template_path,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skills", type=Path, default=Path("skills"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--repository",
        default=os.environ.get("GITHUB_REPOSITORY"),
        help="GitHub owner/repository used in bundle links.",
    )
    parser.add_argument(
        "--tag",
        default=os.environ.get("RELEASE_TAG"),
        help="Tag for the release being generated.",
    )
    parser.add_argument(
        "--previous-ref",
        help="Git ref to compare with; defaults to the latest earlier snapshot.",
    )
    arguments = parser.parse_args()
    if not arguments.repository:
        parser.error("--repository is required outside GitHub Actions")
    if not arguments.tag:
        parser.error("--tag is required outside GitHub Actions")

    repository_root = Path(__file__).resolve().parents[2]
    skills_root = arguments.skills.resolve()
    templates_root = repository_root / ".github" / "templates"
    notes_template_path = templates_root / "release-notes.md"
    row_template_path = templates_root / "release-note-row.md"
    previous_ref = resolve_previous_ref(
        repository_root,
        arguments.tag,
        arguments.previous_ref,
    )

    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        render_notes(
            repository_root,
            skills_root,
            arguments.repository,
            arguments.tag,
            previous_ref,
            notes_template_path.read_text(encoding="utf-8"),
            notes_template_path,
            row_template_path.read_text(encoding="utf-8"),
            row_template_path,
        ),
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
