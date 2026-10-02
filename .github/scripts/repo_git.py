"""Git queries shared by the documentation check, the harvest, and the generator.

One definition of "this skill's bundle content changed", used everywhere, so the
documentation check, the harvest, and the release gate cannot disagree.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


SNAPSHOT_GLOB = "skills-*"

# A skill's handwritten pages are not bundle content: they describe the released
# bundle and are rewritten at release, so changing one is not a source change.
NOT_BUNDLE_CONTENT = ("README.md", "CHANGELOG.md")


@dataclass(frozen=True)
class Commit:
    sha: str
    date: str
    subject: str
    body: str


@dataclass(frozen=True)
class Retirement:
    name: str
    title: str
    last_version: str
    reason: str


# Matches the root catalog in every format it has had: the linked skill's title,
# its name, and the version cell that follows.
CATALOG_ROW = re.compile(
    r"^\|\s*\[([^\]]+)\]\(skills/([a-z0-9-]+)/\)\s*\|\s*`([^`]+)`\s*\|",
    re.MULTILINE,
)


def git(root: Path, *arguments: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", *arguments],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if check and result.returncode:
        detail = (result.stderr or result.stdout).strip()
        raise ValueError(f"git {' '.join(arguments)} failed: {detail}")
    return result


def latest_snapshot_tag(root: Path, *, exclude: str | None = None) -> str | None:
    """Newest snapshot tag reachable from HEAD, or None when there is none."""
    result = git(
        root,
        "tag",
        "--merged",
        "HEAD",
        "--list",
        SNAPSHOT_GLOB,
        "--sort=-version:refname",
        check=False,
    )
    for tag in result.stdout.splitlines():
        tag = tag.strip()
        if tag and tag != exclude:
            return tag
    return None


def show(root: Path, ref: str, path: str) -> str | None:
    """File content at a ref, or None when the file is absent there."""
    result = git(root, "show", f"{ref}:{path}", check=False)
    return result.stdout if result.returncode == 0 else None


def skill_names_at(root: Path, ref: str, skills_root: str = "skills") -> set[str]:
    result = git(root, "ls-tree", "--name-only", "-d", f"{ref}:{skills_root}", check=False)
    if result.returncode:
        return set()
    return {line.strip().rstrip("/") for line in result.stdout.splitlines() if line.strip()}


def source_changed(root: Path, name: str, ref: str, skills_root: str = "skills") -> bool:
    """Whether a skill's bundle content differs from that ref."""
    directory = f"{skills_root}/{name}"
    if not git(root, "ls-tree", "-d", "--name-only", ref, "--", directory).stdout.strip():
        return True

    excludes = [f":!:{directory}/{name_}" for name_ in NOT_BUNDLE_CONTENT]
    comparison = git(root, "diff", "--quiet", ref, "--", directory, *excludes, check=False)
    if comparison.returncode in (0, 1):
        return comparison.returncode == 1
    detail = (comparison.stderr or comparison.stdout).strip()
    raise ValueError(f"Could not compare {name}: {detail}")


def commits_for(root: Path, ref: str, path: str) -> list[Commit]:
    """Commits touching a path since a ref, newest first."""
    separator = "\x1e"
    field = "\x1f"
    result = git(
        root,
        "log",
        f"--format=%H{field}%ad{field}%s{field}%b{separator}",
        "--date=short",
        f"{ref}..HEAD",
        "--",
        path,
    )
    commits: list[Commit] = []
    for record in result.stdout.split(separator):
        record = record.strip("\n")
        if not record.strip():
            continue
        sha, date, subject, body = record.split(field, 3)
        commits.append(Commit(sha=sha, date=date, subject=subject, body=body.strip()))
    return commits


def deleting_commit(root: Path, ref: str, path: str) -> Commit | None:
    commits = git(
        root,
        "log",
        "--diff-filter=D",
        "--format=%H",
        f"{ref}..HEAD",
        "--",
        path,
        check=False,
    ).stdout.split()
    if not commits:
        return None
    sha = commits[0]
    detail = git(root, "show", "-s", "--format=%ad\x1f%s\x1f%b", "--date=short", sha).stdout
    date, subject, body = detail.split("\x1f", 2)
    return Commit(sha=sha, date=date, subject=subject.strip(), body=body.strip())


def detect_retirements(
    root: Path,
    ref: str,
    present: set[str],
    skills_root: str = "skills",
) -> list[Retirement]:
    """Skills the snapshot at `ref` published whose directory is now gone.

    The root catalog at that ref is the record of what it published — changelogs
    were introduced later, so they cannot answer this for early snapshots.
    """
    import yaml

    catalog_text = show(root, ref, "README.md") or ""
    published = {
        name: (title.strip(), version)
        for title, name, version in CATALOG_ROW.findall(catalog_text)
    }

    retirements: list[Retirement] = []
    for name in sorted(set(published) - present):
        catalog_title, last_version = published[name]
        # The catalog row is what that snapshot called the skill, so it names it
        # even where the snapshot's own manifest can no longer be read. The
        # manifest is the fallback, and `interface.display_name` is the one
        # human-readable name it declares.
        manifest = yaml.safe_load(show(root, ref, f"{skills_root}/{name}/skill.yaml") or "") or {}
        interface = manifest.get("interface") or {}
        title = str(catalog_title or interface.get("display_name") or name)

        commit = deleting_commit(root, ref, f"{skills_root}/{name}/skill.yaml")
        reason = commit.body if commit else ""
        retirements.append(
            Retirement(
                name=name,
                title=title,
                last_version=last_version,
                reason=reason.strip(),
            )
        )
    return retirements
