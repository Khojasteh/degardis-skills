"""Generate narrative release notes for a dated snapshot of bundled skills."""

from __future__ import annotations

import argparse
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

import changelog
import repo_git
from template_engine import render_template


TAG_DATE = re.compile(r"^skills-(\d{4}-\d{2}-\d{2})(?:\.\d+)?$")

NEVER_RELEASED = "Never released"
HELD = "Held"
NEW = "New"
UPDATED = "Updated"
PUBLISHED = "Published"


@dataclass(frozen=True)
class Skill:
    directory: Path
    title: str
    name: str
    version: str
    description: str
    short_description: str
    history: changelog.Changelog | None


@dataclass(frozen=True)
class Classified:
    skill: Skill
    status: str
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


def snapshot_date(release_tag: str) -> str:
    match = TAG_DATE.match(release_tag)
    if not match:
        raise ValueError(
            f"Tag must be skills-YYYY-MM-DD or skills-YYYY-MM-DD.N: {release_tag}"
        )
    return match.group(1)


def skill_title(data: dict[str, Any], path: Path) -> str:
    """The name a release note shows.

    `interface.display_name` is the one human-readable name a manifest declares,
    and Degardis requires it, so a source that reaches a release always has one.
    """
    interface = data.get("interface")
    value = interface.get("display_name") if isinstance(interface, dict) else None
    if isinstance(value, str) and value.strip():
        return value.strip()
    raise ValueError(f"{path}: needs an interface.display_name")


def load_skill(manifest: Path) -> Skill:
    data = load_mapping(manifest)
    interface = data.get("interface")
    short_description = ""
    if isinstance(interface, dict):
        value = interface.get("short_description")
        if isinstance(value, str):
            short_description = value.strip()

    return Skill(
        directory=manifest.parent,
        title=skill_title(data, manifest),
        name=required_text(data, "name", manifest),
        version=required_text(data, "version", manifest),
        description=required_text(data, "description", manifest),
        short_description=short_description,
        history=changelog.load(manifest.with_name("CHANGELOG.md")),
    )


def classify_skill(
    repository_root: Path,
    skill: Skill,
    release_tag: str,
    held: set[str],
) -> Classified:
    """Decide a skill's part in this snapshot from its changelog and its diff."""
    if skill.history is None:
        return Classified(skill, NEVER_RELEASED, "")

    latest = skill.history.latest
    if latest is None:
        raise ValueError(f"{skill.history.path}: contains no released version")

    expected_date = snapshot_date(release_tag)
    if latest.date > expected_date:
        raise ValueError(
            f"{skill.name}: the changelog already records version {latest.version} "
            f"on {latest.date}, which is later than the {expected_date} snapshot "
            "being released"
        )

    if latest.date == expected_date:
        if latest.version != skill.version:
            raise ValueError(
                f"{skill.name}: skill.yaml declares version {skill.version}, but "
                f"the section dated for this snapshot is {latest.version}"
            )
        if latest.tag != release_tag:
            raise ValueError(
                f"{skill.name}: the changelog links version {latest.version} to "
                f"tag {latest.tag}, but this snapshot is {release_tag}"
            )
        summary = latest.summary or skill.short_description or skill.description
        first_release = len(skill.history.releases) == 1
        return Classified(skill, NEW if first_release else UPDATED, summary)

    # Released earlier. It carries forward unchanged unless its source moved on,
    # in which case holding it back has to be said out loud.
    changed = repo_git.source_changed(repository_root, skill.name, latest.tag)
    if changed and skill.name not in held:
        raise ValueError(
            f"{skill.name}: bundle content has changed since {latest.tag}, but this "
            "snapshot neither releases it nor holds it back. Add a changelog "
            f"section dated {expected_date}, or pass --hold {skill.name}."
        )
    return Classified(skill, HELD if changed else PUBLISHED, "")


def render_skill_section(
    skill: Skill,
    summary: str,
    repository: str,
    release_tag: str,
    template: str,
    template_path: Path,
) -> str:
    return render_template(
        template,
        {
            "title": skill.title,
            "skill_name": skill.name,
            "version": skill.version,
            "description": skill.description,
            "summary": summary,
            "repository": repository,
            "release_tag": release_tag,
        },
        template_path,
    ).rstrip()


def render_retired_section(
    entry: repo_git.Retirement,
    template: str,
    template_path: Path,
) -> str:
    return render_template(
        template,
        {
            "title": entry.title,
            "skill_name": entry.name,
            "last_version": entry.last_version,
            "reason": entry.reason,
        },
        template_path,
    ).rstrip()


def render_notes(
    classified: list[Classified],
    retirements: list[repo_git.Retirement],
    repository: str,
    release_tag: str,
    templates: dict[str, tuple[str, Path]],
) -> str:
    grouped: dict[str, list[str]] = {NEW: [], UPDATED: []}
    for entry in classified:
        if entry.status in grouped:
            template, path = templates[entry.status]
            grouped[entry.status].append(
                render_skill_section(
                    entry.skill, entry.summary, repository, release_tag, template, path
                )
            )

    sections: list[str] = []
    if retirements:
        template, path = templates["retired"]
        body = "\n\n".join(
            render_retired_section(entry, template, path)
            for entry in sorted(retirements, key=lambda item: item.title.casefold())
        )
        sections.append(f"### Retirements\n\n{body}")
    if grouped[NEW]:
        sections.append("### New skills\n\n" + "\n\n".join(grouped[NEW]))
    if grouped[UPDATED]:
        sections.append("### Improvements\n\n" + "\n\n".join(grouped[UPDATED]))

    template, path = templates["notes"]
    return render_template(
        template,
        {
            "snapshot_date": snapshot_date(release_tag),
            "sections": "\n\n".join(sections),
        },
        path,
    )


def write_names(path: Path, names: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(f"{name}\n" for name in names),
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skills", type=Path, default=Path("skills"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--hold",
        action="append",
        default=[],
        metavar="SKILL",
        help=(
            "Skill whose changed source this snapshot deliberately does not "
            "publish. Repeatable."
        ),
    )
    parser.add_argument(
        "--released-skills",
        type=Path,
        help="Optional file listing the skills to build, one name per line.",
    )
    parser.add_argument(
        "--published-skills",
        type=Path,
        help=(
            "Optional file listing every skill that must have a bundle attached, "
            "one name per line."
        ),
    )
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
    templates = {
        key: ((templates_root / filename).read_text(encoding="utf-8"), templates_root / filename)
        for key, filename in (
            ("notes", "release-notes.md"),
            (NEW, "release-note-new-skill.md"),
            (UPDATED, "release-note-updated-skill.md"),
            ("retired", "release-note-retired-skill.md"),
        )
    }

    skills = sorted(
        (load_skill(manifest) for manifest in discover_skills(skills_root)),
        key=lambda skill: skill.title.casefold(),
    )
    names = [skill.name for skill in skills]
    if len(names) != len(set(names)):
        raise ValueError("Skill names must be unique")

    held = set(arguments.hold)
    unknown = held - set(names)
    if unknown:
        raise ValueError(f"--hold names no such skill: {', '.join(sorted(unknown))}")

    classified = [
        classify_skill(repository_root, skill, arguments.tag, held) for skill in skills
    ]

    previous_ref = arguments.previous_ref or repo_git.latest_snapshot_tag(
        repository_root, exclude=arguments.tag
    )
    retirements: list[repo_git.Retirement] = []
    if previous_ref:
        retirements = repo_git.detect_retirements(
            repository_root, previous_ref, present=set(names)
        )
    missing = [entry.name for entry in retirements if not entry.reason]
    if missing:
        raise ValueError(
            "These retirements have no reason to announce: "
            f"{', '.join(missing)}. Users are told why a skill was withdrawn and "
            "what replaces it, and that reason is the body of the commit that "
            "deleted it. Ask the maintainer for the reason — never infer one — "
            "and put it in that commit."
        )

    released = sorted(
        entry.skill.name for entry in classified if entry.status in (NEW, UPDATED)
    )
    if not released and not retirements:
        raise ValueError(
            f"No skill declares a release dated {snapshot_date(arguments.tag)} and "
            "nothing was retired. Date a changelog section for at least one skill "
            "before releasing."
        )

    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        render_notes(classified, retirements, arguments.repository, arguments.tag, templates),
        encoding="utf-8",
        newline="\n",
    )

    if arguments.released_skills:
        write_names(arguments.released_skills, released)

    if arguments.published_skills:
        write_names(
            arguments.published_skills,
            sorted(
                entry.skill.name
                for entry in classified
                if entry.skill.history and entry.skill.history.releases
            ),
        )


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        raise SystemExit(f"error: {error}")
