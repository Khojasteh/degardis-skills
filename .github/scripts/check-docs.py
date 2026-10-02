"""Check that handwritten documentation agrees with what has been released."""

from __future__ import annotations

import fnmatch
import os
import re
from dataclasses import dataclass
from pathlib import Path

import yaml

import changelog
import repo_git


CATALOG_ROW = re.compile(
    r"^\|\s*\[[^\]]+\]\(skills/([a-z0-9-]+)/\)\s*\|\s*`([^`]+)`\s*\|",
    re.MULTILINE,
)
VERSION_LINE = re.compile(r"^\*\*Version:\*\*\s*`([^`]+)`", re.MULTILINE)
RELEASE_LINK = re.compile(r"(?:\.\./)*releases/[^\s)\]]+")
LATEST_ASSET = re.compile(r"^(?:\.\./)+releases/latest/download/([a-z0-9-]+\.zip)$")
INLINE_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
REFERENCE_LINK = re.compile(r"^\[[^\]]+\]:\s*(\S+)\s*$", re.MULTILINE)
LINK_TEXT = re.compile(r"\[([^\]]*)\]\([^)]*\)")
HEADING = re.compile(r"^#{1,6}[ \t]+(.+?)[ \t]*#*$", re.MULTILINE)
NOT_IN_ANCHOR = re.compile(r"[^a-z0-9 \-_]")
SNAPSHOT_TAG = re.compile(r"^skills-(\d{4}-\d{2}-\d{2})(?:\.\d+)?$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
QUEUE_SECTION = re.compile(r"^##[ \t]+(.+?)[ \t]*#*$", re.MULTILINE)
QUEUE_ITEM = re.compile(r"^-[ \t]+\S", re.MULTILINE)
PENDING_STATES = frozenset({"Open", "Needs a decision", "Blocked"})


@dataclass(frozen=True)
class Skill:
    directory: Path
    name: str
    readme: Path
    manifest: dict
    changelog: changelog.Changelog | None

    @property
    def released(self) -> changelog.Release | None:
        return self.changelog.latest if self.changelog else None

    @property
    def version(self) -> str:
        return str(self.manifest.get("version", "")).strip()


def discover_skills(root: Path) -> list[Path]:
    """Find skill directories using Degardis's stop-at-skill discovery rule."""
    directories: list[Path] = []

    for directory, child_directories, filenames in os.walk(root):
        child_directories.sort()
        if "skill.yaml" in filenames:
            directories.append(Path(directory))
            child_directories.clear()

    return directories


def load_skills(skills_root: Path, problems: list[str]) -> list[Skill]:
    skills: list[Skill] = []
    for directory in discover_skills(skills_root):
        try:
            history = changelog.load(directory / "CHANGELOG.md")
        except ValueError as error:
            problems.append(str(error))
            history = None
        manifest = yaml.safe_load(
            (directory / "skill.yaml").read_text(encoding="utf-8")
        ) or {}
        skills.append(
            Skill(
                directory=directory,
                name=directory.name,
                readme=directory / "README.md",
                manifest=manifest,
                changelog=history,
            )
        )
    return skills


def check_layout(skills_root: Path, skills: list[Skill], problems: list[str]) -> None:
    if (skills_root / "skill.yaml").is_file():
        problems.append(f"{skills_root}: holds a manifest; skills go in skills/<skill-name>/")

    # One reader-facing page per skill and no other: a category or collection
    # README under skills/ has no catalog row, no version, and no reader.
    for readme in sorted(skills_root.rglob("README.md")):
        if readme.parent.parent != skills_root:
            problems.append(
                f"{readme}: only skills/<skill-name>/README.md is a reader-facing page"
            )

    for skill in skills:
        parent = skill.directory.parent
        while parent != skills_root and parent != parent.parent:
            if (parent / "skill.yaml").is_file():
                problems.append(
                    f"{parent}: holds a manifest above the skill in {skill.directory}"
                )
                break
            parent = parent.parent

        content = skill.manifest.get("content")
        if not isinstance(content, dict):
            continue
        for kind, patterns in content.items():
            for pattern in patterns or []:
                for page in repo_git.NOT_BUNDLE_CONTENT:
                    if fnmatch.fnmatch(page, str(pattern)):
                        problems.append(
                            f"{skill.directory}/skill.yaml: content.{kind} pattern "
                            f"{pattern!r} matches {page}, which never ships in a bundle"
                        )


def parse_version(value: str) -> tuple[int, ...]:
    return tuple(int(part) for part in value.split("."))


def check_versions(
    repository_root: Path,
    skill: Skill,
    problems: list[str],
    *,
    git_available: bool,
) -> None:
    if not SEMVER.match(skill.version):
        problems.append(
            f"{skill.directory}/skill.yaml: version {skill.version!r} is not X.Y.Z"
        )
        return

    released = skill.released
    if released is None:
        return

    declared = parse_version(skill.version)
    published = parse_version(released.version)
    if declared < published:
        problems.append(
            f"{skill.directory}/skill.yaml: version {skill.version} is behind the "
            f"released {released.version}"
        )
        return

    if not git_available:
        return
    if not repo_git.git(
        repository_root, "rev-parse", "--verify", f"{released.tag}^{{commit}}", check=False
    ).stdout.strip():
        return

    changed = repo_git.source_changed(repository_root, skill.name, released.tag)
    if changed and declared == published:
        problems.append(
            f"{skill.directory}: bundle content changed since {released.tag} but "
            f"skill.yaml still declares the released version {skill.version}. "
            "Raise it in the commit that changed the source."
        )
    elif not changed and declared != published:
        problems.append(
            f"{skill.directory}/skill.yaml: declares {skill.version} but no bundle "
            f"content has changed since {released.version} was released"
        )


def check_changelog(skill: Skill, problems: list[str]) -> None:
    if skill.changelog is None:
        return

    for release in skill.changelog.releases:
        where = f"{skill.changelog.path}: version {release.version}"
        tag = SNAPSHOT_TAG.match(release.tag)
        if not tag:
            problems.append(
                f"{where} links to tag {release.tag!r}, which is not a "
                "skills-YYYY-MM-DD snapshot tag"
            )
        elif tag.group(1) != release.date:
            problems.append(
                f"{where} is dated {release.date} but links to tag "
                f"{release.tag}, whose date is {tag.group(1)}"
            )
        if release.asset != f"{skill.name}.zip":
            problems.append(
                f"{where} links to asset {release.asset!r} instead of "
                f"{skill.name}.zip"
            )


def check_readme_version(skill: Skill, text: str, problems: list[str]) -> None:
    shown = VERSION_LINE.search(text)
    released = skill.released

    if released is None:
        if shown:
            problems.append(
                f"{skill.readme}: shows version {shown.group(1)} but the skill has "
                "never been released"
            )
        return

    if not shown:
        problems.append(
            f"{skill.readme}: has no '**Version:** `X.Y.Z`' line, but the skill is "
            f"released at {released.version}"
        )
    elif shown.group(1) != released.version:
        problems.append(
            f"{skill.readme}: shows version {shown.group(1)}, but the newest "
            f"released changelog version is {released.version}"
        )


def check_release_links(
    path: Path,
    text: str,
    released_names: set[str],
    problems: list[str],
) -> None:
    for link in RELEASE_LINK.findall(text):
        asset = LATEST_ASSET.match(link)
        if asset:
            name = asset.group(1).removesuffix(".zip")
            if name not in released_names:
                problems.append(
                    f"{path}: links to {asset.group(1)}, but {name} has no released "
                    "version to download"
                )
            continue
        problems.append(
            f"{path}: release link {link!r} must point at "
            "'releases/latest/download/<skill-name>.zip'"
        )


def retired_link(candidate: Path, retired_directories: set[Path]) -> bool:
    """A link landing in a skill directory a pending retirement has deleted."""
    landing = candidate.resolve()
    return any(
        landing == directory or directory in landing.parents
        for directory in retired_directories
    )


def anchor_slug(heading: str) -> str:
    """The fragment GitHub gives a Markdown heading."""
    plain = LINK_TEXT.sub(r"", heading)
    plain = plain.replace("`", "").replace("*", "").replace("~", "").replace("_", "")
    return NOT_IN_ANCHOR.sub("", plain.lower()).strip().replace(" ", "-")


def anchors(path: Path, cache: dict[Path, set[str]] = {}) -> set[str]:
    """Every heading fragment a Markdown page offers, read once per page."""
    key = path.resolve()
    if key not in cache:
        try:
            body = path.read_text(encoding="utf-8")
        except OSError:
            cache[key] = set()
        else:
            cache[key] = {anchor_slug(heading) for heading in HEADING.findall(body)}
    return cache[key]


def check_relative_links(
    path: Path,
    text: str,
    problems: list[str],
    retired_directories: set[Path] = frozenset(),
) -> None:
    targets = INLINE_LINK.findall(text) + REFERENCE_LINK.findall(text)
    for target in targets:
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        if RELEASE_LINK.fullmatch(target):
            continue
        location, _, fragment = target.partition("#")
        candidate = (path.parent / location) if location else path
        # A link landing in a skill directory a pending retirement has deleted.
        if retired_link(candidate, retired_directories):
            continue
        if not candidate.exists():
            problems.append(f"{path}: link target {target!r} does not exist")
            continue
        # A heading that moved to another page leaves a link that resolves and
        # lands nowhere, which is the failure a split into guides invites.
        if fragment and candidate.is_file() and candidate.suffix == ".md":
            if anchor_slug(fragment) not in anchors(candidate):
                problems.append(
                    f"{path}: link {target!r} points at no heading in {candidate.name}"
                )


def check_catalog(
    root_readme: Path,
    text: str,
    skills: list[Skill],
    retiring: set[str],
    problems: list[str],
) -> None:
    rows = CATALOG_ROW.findall(text)
    listed: dict[str, list[str]] = {}
    for name, version in rows:
        listed.setdefault(name, []).append(version)

    known = {skill.name for skill in skills}
    for name in listed:
        # A retired skill keeps its row until the release drops it, the same
        # release that adds a row for a skill published for the first time.
        if name not in known and name not in retiring:
            problems.append(
                f"{root_readme}: catalog lists {name}, which is not a skill"
            )

    for skill in skills:
        versions = listed.get(skill.name, [])
        released = skill.released

        if released is None:
            if versions:
                problems.append(
                    f"{root_readme}: catalog lists {skill.name}, which has never "
                    "been released"
                )
            continue

        if not versions:
            problems.append(
                f"{root_readme}: catalog is missing {skill.name}, released at "
                f"{released.version}"
            )
        elif len(versions) > 1:
            problems.append(
                f"{root_readme}: catalog lists {skill.name} {len(versions)} times"
            )
        elif versions[0] != released.version:
            problems.append(
                f"{root_readme}: catalog shows {skill.name} {versions[0]}, but its "
                f"newest released changelog version is {released.version}"
            )


def describe_retirements(retirements: list[repo_git.Retirement]) -> str:
    """One line naming what the next release still has to announce and drop."""
    if not retirements:
        return ""

    unexplained = sorted(entry.name for entry in retirements if not entry.reason)
    named = ", ".join(sorted(entry.name for entry in retirements))
    line = (
        f"{len(retirements)} retired skill(s) await the release that announces them "
        f"and drops their catalog rows: {named}."
    )
    if unexplained:
        line += (
            " The deleting commit has an empty body for "
            f"{', '.join(unexplained)}, so the release will refuse to announce "
            "them until that body is fixed."
        )
    return line


def check_pending_queue(page: Path, problems: list[str]) -> None:
    """A queue holds open questions under their state, and nothing settled."""
    text = page.read_text(encoding="utf-8")

    # A settled question is deleted rather than kept under a heading of its
    # own: a standing verdict here goes stale the moment the skill changes.
    for heading in QUEUE_SECTION.findall(text):
        if heading not in PENDING_STATES:
            problems.append(
                f"{page}: section '{heading}' is not one of "
                f"{', '.join(sorted(PENDING_STATES))}; a settled question is "
                "deleted, not filed"
            )

    if not QUEUE_ITEM.search(text):
        problems.append(
            f"{page}: holds no question; delete the directory when the queue empties"
        )


def check_trials(
    trials: Path,
    skills: list[Skill],
    problems: list[str],
    retired_directories: set[Path] = frozenset(),
) -> None:
    if not trials.is_dir():
        return

    # AGENTS.md holds the rules; this is the page a visitor opens instead.
    if not (trials / "README.md").is_file():
        problems.append(f"{trials}: has no README.md describing what it holds")

    known = {skill.name for skill in skills}
    fixtures = trials / "fixtures"
    if fixtures.is_dir():
        for collection in sorted(fixtures.iterdir()):
            if collection.name == "README.md":
                continue
            if not collection.is_dir():
                problems.append(f"{collection}: fixtures live in fixtures/<skill-name>/")
                continue
            if collection.name not in known:
                problems.append(
                    f"{collection}: fixture collection has no matching skill; a "
                    "retirement deletes its fixtures"
                )
            # The collection README is the one page describing these fixtures:
            # what each is, what it carries, and which situations it fits.
            if not (collection / "README.md").is_file():
                problems.append(
                    f"{collection}: fixture collection has no README.md describing "
                    "what it holds"
                )

            # A session working in this repository reads an AGENTS.md it walks
            # into as instructions for itself, and nothing under a fixture
            # collection is that. A check needing the evaluator's root to carry
            # one writes it there; the rules live in trials/AGENTS.md.
            for name in ("AGENTS.md", "CLAUDE.md"):
                for instructions in sorted(collection.rglob(name)):
                    problems.append(
                        f"{instructions}: trial fixtures carry no {name}; the rules "
                        "are in trials/AGENTS.md and a check that needs one writes "
                        "it into the prepared root"
                    )

    # A pending directory is optional — a skill with an empty queue has none —
    # but one that exists names a real skill and holds its questions.
    pending = trials / "pending"
    if pending.is_dir():
        if not (pending / "README.md").is_file():
            problems.append(f"{pending}: has no README.md describing what it holds")

        for queue in sorted(pending.iterdir()):
            if queue.name == "README.md":
                continue
            if not queue.is_dir():
                problems.append(f"{queue}: pending questions live in pending/<skill-name>/")
                continue
            if queue.name not in known:
                problems.append(
                    f"{queue}: pending queue has no matching skill; a retirement "
                    "deletes its queue"
                )
            page = queue / "README.md"
            if not page.is_file():
                problems.append(
                    f"{queue}: has no README.md holding its queue; delete the "
                    "directory when that queue empties"
                )
            else:
                check_pending_queue(page, problems)

    for path in sorted(trials.rglob("*.md")):
        check_relative_links(
            path, path.read_text(encoding="utf-8"), problems, retired_directories
        )


def check_guides(
    docs: Path,
    downloadable: set[str],
    problems: list[str],
    retired_directories: set[Path] = frozenset(),
) -> None:
    """The shared guides the READMEs hand readers off to, and their conventions."""
    if not docs.is_dir():
        problems.append(f"{docs}: the READMEs hand readers off to guides that are missing")
        return

    if not (docs / "README.md").is_file():
        problems.append(f"{docs}: has no README.md index")

    # AGENTS.md here is not a guide — it is how the guides are written — but its
    # links are checked with theirs by the sweep below.
    if not (docs / "AGENTS.md").is_file():
        problems.append(f"{docs}: has no AGENTS.md holding the reader-page conventions")

    for path in sorted(docs.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        check_release_links(path, text, downloadable, problems)
        check_relative_links(path, text, problems, retired_directories)


def main() -> None:
    repository_root = Path(__file__).resolve().parents[2]
    skills_root = repository_root / "skills"
    root_readme = repository_root / "README.md"

    problems: list[str] = []
    skills = load_skills(skills_root, problems)
    released_names = {skill.name for skill in skills if skill.released}

    # Skills the last snapshot published whose directories are now gone. Their
    # catalog rows, download links, and sibling links stand until the release
    # removes them, so every check below treats those as pending, not broken.
    snapshot_tag = repo_git.latest_snapshot_tag(repository_root)
    git_available = snapshot_tag is not None
    retirements = (
        repo_git.detect_retirements(
            repository_root, snapshot_tag, present={skill.name for skill in skills}
        )
        if git_available
        else []
    )
    retiring = {entry.name for entry in retirements}
    retired_directories = {(skills_root / name).resolve() for name in retiring}
    downloadable = released_names | retiring

    root_text = root_readme.read_text(encoding="utf-8")
    check_layout(skills_root, skills, problems)
    check_catalog(root_readme, root_text, skills, retiring, problems)
    check_release_links(root_readme, root_text, downloadable, problems)
    check_relative_links(root_readme, root_text, problems, retired_directories)

    for skill in skills:
        check_changelog(skill, problems)
        check_versions(repository_root, skill, problems, git_available=git_available)
        if not skill.readme.is_file():
            problems.append(f"{skill.directory}: has no README.md")
            continue
        text = skill.readme.read_text(encoding="utf-8")
        check_readme_version(skill, text, problems)
        check_release_links(skill.readme, text, downloadable, problems)
        check_relative_links(skill.readme, text, problems, retired_directories)

    check_guides(
        repository_root / "docs", downloadable, problems, retired_directories
    )
    check_trials(repository_root / "trials", skills, problems, retired_directories)

    # The maintainer pages cross-link each other and the reader pages, and
    # nothing else here would notice a link that stopped resolving.
    for path in sorted((repository_root / ".github").glob("*.md")):
        check_relative_links(
            path, path.read_text(encoding="utf-8"), problems, retired_directories
        )

    if problems:
        print("Documentation is inconsistent:")
        for problem in sorted(problems):
            print(f"- {problem}")
        raise SystemExit(1)

    print(f"Documentation is consistent for {len(skills)} skills.")
    outstanding = describe_retirements(retirements)
    if outstanding:
        print(outstanding)


if __name__ == "__main__":
    main()
