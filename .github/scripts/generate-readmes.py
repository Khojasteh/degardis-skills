"""Generate skill READMEs and the dynamic sections of the root README."""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from template_engine import render_repeated, render_template


README_KEYS = {
    "format_version",
    "purpose",
    "when_it_applies",
    "capabilities",
    "sample_prompts",
    "catalog",
}
CATALOG_KEYS = {"order", "category", "summary"}


@dataclass(frozen=True)
class Skill:
    directory: Path
    title: str
    name: str
    version: str
    license: str
    purpose: str
    when_it_applies: str
    capabilities: tuple[str, ...]
    sample_prompts: tuple[str, ...]
    catalog_order: int
    catalog_category: str
    catalog_summary: str


def discover_manifests(root: Path) -> list[Path]:
    """Find skill manifests using Degardis's stop-at-skill discovery rule."""
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


def required_text_list(
    data: dict[str, Any],
    key: str,
    path: Path,
) -> tuple[str, ...]:
    value = data.get(key)
    if not isinstance(value, list) or not value:
        raise ValueError(f"{path}: {key} must be a non-empty list")

    items: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            raise ValueError(
                f"{path}: {key}[{index}] must be a non-empty string"
            )
        if "\n" in item:
            raise ValueError(f"{path}: {key}[{index}] must be one line")
        items.append(item.strip())
    return tuple(items)


def reject_unknown_keys(
    data: dict[str, Any],
    allowed: set[str],
    path: Path,
) -> None:
    unknown = set(data) - allowed
    if unknown:
        raise ValueError(
            f"{path}: unknown fields: {', '.join(sorted(map(str, unknown)))}"
        )


def load_skill(manifest: Path, skills_root: Path) -> Skill:
    if manifest.parent.parent != skills_root:
        raise ValueError(
            f"{manifest} is nested; skills must be stored directly under "
            f"{skills_root}"
        )

    skill_data = load_mapping(manifest)
    title = required_text(skill_data, "title", manifest)
    name = required_text(skill_data, "name", manifest)
    version = required_text(skill_data, "version", manifest)
    license_name = required_text(skill_data, "license", manifest)
    if manifest.parent.name != name:
        raise ValueError(
            f"{manifest}: name must match its parent directory, "
            f"{manifest.parent.name!r}"
        )

    documentation_path = manifest.with_name("readme.yaml")
    if not documentation_path.is_file():
        raise ValueError(f"{manifest} has no readme.yaml")
    documentation = load_mapping(documentation_path)
    reject_unknown_keys(documentation, README_KEYS, documentation_path)
    if documentation.get("format_version") != 1:
        raise ValueError(f"{documentation_path}: format_version must be 1")

    catalog = documentation.get("catalog")
    if not isinstance(catalog, dict):
        raise ValueError(f"{documentation_path}: catalog must be a mapping")
    reject_unknown_keys(catalog, CATALOG_KEYS, documentation_path)
    catalog_order = catalog.get("order")
    if isinstance(catalog_order, bool) or not isinstance(catalog_order, int):
        raise ValueError(
            f"{documentation_path}: catalog.order must be an integer"
        )

    return Skill(
        directory=manifest.parent,
        title=title,
        name=name,
        version=version,
        license=license_name,
        purpose=required_text(documentation, "purpose", documentation_path),
        when_it_applies=required_text(
            documentation,
            "when_it_applies",
            documentation_path,
        ),
        capabilities=required_text_list(
            documentation,
            "capabilities",
            documentation_path,
        ),
        sample_prompts=required_text_list(
            documentation,
            "sample_prompts",
            documentation_path,
        ),
        catalog_order=catalog_order,
        catalog_category=required_text(
            catalog,
            "category",
            documentation_path,
        ),
        catalog_summary=required_text(
            catalog,
            "summary",
            documentation_path,
        ),
    )


def release_asset_link(
    repository_root: Path,
    readme: Path,
    skill_name: str,
) -> str:
    source_depth = len(readme.parent.relative_to(repository_root).parts)
    # GitHub renders a nested README below its `tree/<revision>/` URL.
    repository_route = "../" * (source_depth + 2)
    return f"{repository_route}releases/latest/download/{skill_name}.zip"


def render_skill_readme(
    repository_root: Path,
    skill: Skill,
    readme_template: str,
    readme_template_path: Path,
    changelog_link: str,
    capability_template: str,
    capability_template_path: Path,
    sample_prompt_template: str,
    sample_prompt_template_path: Path,
) -> str:
    readme_path = skill.directory / "README.md"
    return render_template(
        readme_template,
        {
            "title": skill.title,
            "skill_name": skill.name,
            "version": skill.version,
            "license": skill.license,
            "changelog_link": (
                changelog_link
                if (skill.directory / "CHANGELOG.md").is_file()
                else ""
            ),
            "purpose": skill.purpose,
            "when_it_applies": skill.when_it_applies,
            "capabilities": render_repeated(
                skill.capabilities,
                "capability",
                capability_template,
                capability_template_path,
            ),
            "sample_prompts": render_repeated(
                skill.sample_prompts,
                "sample_prompt",
                sample_prompt_template,
                sample_prompt_template_path,
            ),
            "release_asset_link": release_asset_link(
                repository_root,
                readme_path,
                skill.name,
            ),
        },
        readme_template_path,
    )


def table_cell(value: str, field: str, skill: Skill) -> str:
    if "\n" in value or "|" in value:
        raise ValueError(
            f"{skill.directory / 'readme.yaml'}: {field} cannot contain "
            "newlines or vertical bars"
        )
    return value


def render_catalog(
    skills: list[Skill],
    catalog_template: str,
    catalog_template_path: Path,
    row_template: str,
    row_template_path: Path,
) -> str:
    rows: list[str] = []
    for skill in sorted(
        skills,
        key=lambda item: (item.catalog_order, item.title.casefold()),
    ):
        title = table_cell(skill.title, "title", skill)
        version = table_cell(skill.version, "version", skill)
        license_name = table_cell(skill.license, "license", skill)
        category = table_cell(
            skill.catalog_category,
            "catalog.category",
            skill,
        )
        summary = table_cell(skill.catalog_summary, "catalog.summary", skill)
        rows.append(
            render_template(
                row_template,
                {
                    "title": title,
                    "skill_name": skill.name,
                    "version": version,
                    "license": license_name,
                    "category": category,
                    "summary": summary,
                },
                row_template_path,
            ).rstrip()
        )
    return render_template(
        catalog_template,
        {"catalog_rows": "\n".join(rows)},
        catalog_template_path,
    )


def replace_generated_section(
    document: str,
    expected: str,
    begin_marker: str,
    end_marker: str,
    path: Path,
) -> str:
    if document.count(begin_marker) != 1 or document.count(end_marker) != 1:
        raise ValueError(
            f"{path} must contain exactly one {begin_marker!r} and "
            f"{end_marker!r}"
        )
    start = document.index(begin_marker)
    end = document.index(end_marker, start)
    end += len(end_marker)
    return document[:start] + expected.rstrip() + document[end:]


def replace_root_sections(
    readme: Path,
    catalog: str,
    installation: str,
) -> str:
    current = readme.read_text(encoding="utf-8")
    with_catalog = replace_generated_section(
        current,
        catalog,
        "<!-- BEGIN GENERATED: root catalog -->",
        "<!-- END GENERATED: root catalog -->",
        readme,
    )
    return replace_generated_section(
        with_catalog,
        installation,
        "<!-- BEGIN GENERATED: root installation -->",
        "<!-- END GENERATED: root installation -->",
        readme,
    )


def update_file(path: Path, expected: str, check: bool) -> bool:
    current = path.read_text(encoding="utf-8") if path.is_file() else ""
    if current == expected:
        return False
    if check:
        return True
    path.write_text(expected, encoding="utf-8", newline="\n")
    print(f"[UPDATED] {path}")
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail when generated README content is stale.",
    )
    arguments = parser.parse_args()

    repository_root = Path(__file__).resolve().parents[2]
    skills_root = repository_root / "skills"
    templates_root = repository_root / ".github" / "templates"
    readme_template_path = templates_root / "skill-readme.md"
    catalog_template_path = templates_root / "root-catalog.md"
    catalog_row_template_path = templates_root / "catalog-row.md"
    root_installation_template_path = (
        templates_root / "root-installation.md"
    )
    changelog_link_template_path = templates_root / "changelog-link.md"
    capability_template_path = templates_root / "capability.md"
    sample_prompt_template_path = templates_root / "sample-prompt.md"
    readme_template = readme_template_path.read_text(encoding="utf-8")
    catalog_template = catalog_template_path.read_text(encoding="utf-8")
    catalog_row_template = catalog_row_template_path.read_text(
        encoding="utf-8"
    )
    root_installation_template = root_installation_template_path.read_text(
        encoding="utf-8"
    )
    changelog_link = changelog_link_template_path.read_text(
        encoding="utf-8"
    ).rstrip("\r\n")
    capability_template = capability_template_path.read_text(encoding="utf-8")
    sample_prompt_template = sample_prompt_template_path.read_text(
        encoding="utf-8"
    )

    skills = [
        load_skill(manifest, skills_root)
        for manifest in discover_manifests(skills_root)
    ]
    names = [skill.name for skill in skills]
    if len(names) != len(set(names)):
        raise ValueError("Skill names must be unique")
    orders = [skill.catalog_order for skill in skills]
    if len(orders) != len(set(orders)):
        raise ValueError("Catalog order values must be unique")

    stale: list[Path] = []
    for skill in skills:
        readme = skill.directory / "README.md"
        expected = render_skill_readme(
            repository_root,
            skill,
            readme_template,
            readme_template_path,
            changelog_link,
            capability_template,
            capability_template_path,
            sample_prompt_template,
            sample_prompt_template_path,
        )
        if update_file(readme, expected, arguments.check):
            stale.append(readme)

    root_readme = repository_root / "README.md"
    expected_root = replace_root_sections(
        root_readme,
        render_catalog(
            skills,
            catalog_template,
            catalog_template_path,
            catalog_row_template,
            catalog_row_template_path,
        ),
        render_template(
            root_installation_template,
            {},
            root_installation_template_path,
        ),
    )
    if update_file(root_readme, expected_root, arguments.check):
        stale.append(root_readme)

    if arguments.check and stale:
        print("Generated README content is stale:")
        for path in stale:
            print(f"- {path.relative_to(repository_root)}")
        raise SystemExit(1)

    if arguments.check:
        print(f"README content is current for {len(skills)} skills.")


if __name__ == "__main__":
    main()
