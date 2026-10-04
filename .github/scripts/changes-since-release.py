"""Collect what has changed since the last snapshot, as input to release notes.

There is no `Unreleased` section to read. This report says where to look, not
what is true: a commit body records what a session meant to do, and the change
may have landed differently or been reversed since. The shipped source is the
authority for every claim a release section or README makes.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import yaml

import changelog
import repo_git


def discover_skills(root: Path) -> list[Path]:
    directories: list[Path] = []
    for directory, child_directories, filenames in os.walk(root):
        child_directories.sort()
        if "skill.yaml" in filenames:
            directories.append(Path(directory))
            child_directories.clear()
    return directories


def construct_files(repository_root: Path, name: str, ref: str) -> list[str]:
    directory = f"skills/{name}"
    excludes = [f":!:{directory}/{page}" for page in repo_git.NOT_BUNDLE_CONTENT]
    output = repo_git.git(
        repository_root, "diff", "--stat", ref, "--", directory, *excludes
    ).stdout
    return [line for line in output.splitlines() if line.strip()]


def last_published(
    repository_root: Path, history: changelog.Changelog | None
) -> changelog.Release | None:
    """Newest release whose snapshot tag exists.

    While a snapshot is being prepared, the changelog already holds its section,
    but its tag is created only when it is published.
    """
    for release in history.releases if history else ():
        if repo_git.git(
            repository_root, "rev-parse", "--verify", "--quiet",
            f"{release.tag}^{{commit}}", check=False,
        ).returncode == 0:
            return release
    return None


def report_skill(
    repository_root: Path, directory: Path, ref: str, *, explicit: bool
) -> None:
    name = directory.name
    manifest = yaml.safe_load((directory / "skill.yaml").read_text(encoding="utf-8")) or {}
    released = last_published(repository_root, changelog.load(directory / "CHANGELOG.md"))
    since = released.tag if released and not explicit else ref

    if not repo_git.source_changed(repository_root, name, since):
        return

    print(f"\n{'=' * 78}\n{name}  —  manifest {manifest.get('version', '?')}", end="")
    if released:
        print(f", released {released.version} at {released.tag}")
    else:
        print(", never released")
    print("=" * 78)

    stat = construct_files(repository_root, name, since)
    if stat:
        print("\nChanged bundle content:")
        for line in stat:
            print(f"  {line.strip()}")

    commits = repo_git.commits_for(repository_root, since, f"skills/{name}")
    print(f"\nCommits since {since}: {len(commits)}")
    bodyless = 0
    for commit in commits:
        print(f"\n  {commit.sha[:9]}  {commit.date}  {commit.subject}")
        if commit.body:
            for line in commit.body.splitlines():
                if line.strip().startswith("Co-Authored-By:"):
                    continue
                print(f"      {line}")
        else:
            bodyless += 1
            print("      (no body — this change is recorded nowhere but its diff)")

    if bodyless:
        print(
            f"\n  {bodyless} of {len(commits)} commits carry no body. Read the diff "
            "for those; do not guess what they were for."
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill", nargs="?", help="Limit the report to one skill.")
    parser.add_argument(
        "--since",
        help="Ref to compare every skill with; defaults to each skill's last "
        "published release, or the latest snapshot tag for a skill never released.",
    )
    arguments = parser.parse_args()

    repository_root = Path(__file__).resolve().parents[2]
    ref = arguments.since or repo_git.latest_snapshot_tag(repository_root)
    if not ref:
        raise SystemExit("error: no snapshot tag found; pass --since <ref>")

    print(f"Changes since {ref}")

    directories = discover_skills(repository_root / "skills")
    present = {directory.name for directory in directories}
    for directory in sorted(directories, key=lambda path: path.name):
        if arguments.skill and directory.name != arguments.skill:
            continue
        report_skill(repository_root, directory, ref, explicit=bool(arguments.since))

    if arguments.skill:
        return

    retirements = repo_git.detect_retirements(repository_root, ref, present=present)
    if retirements:
        print(f"\n{'=' * 78}\nRetirements detected\n{'=' * 78}")
        for entry in retirements:
            state = "reason ready" if entry.reason else "NO REASON — the release will fail"
            print(f"\n  {entry.name}  (last released {entry.last_version})  [{state}]")
            for line in entry.reason.splitlines():
                print(f"      {line}")


if __name__ == "__main__":
    main()
