"""Read skill changelogs, the authoritative record of what has been published."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


SECTION_HEADING = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
RELEASE_HEADING = re.compile(
    r"^\[(\d+\.\d+\.\d+)\]\(([^)]+)\)\s*-\s*(\d{4}-\d{2}-\d{2})$"
)
ASSET_URL = re.compile(
    r"^https://github\.com/[^/]+/[^/]+/releases/download/([^/]+)/([^/]+\.zip)$"
)


@dataclass(frozen=True)
class Release:
    version: str
    date: str
    tag: str
    asset: str
    asset_url: str
    summary: str


@dataclass(frozen=True)
class Changelog:
    path: Path
    releases: tuple[Release, ...]

    @property
    def latest(self) -> Release | None:
        return self.releases[0] if self.releases else None

    def release_for(self, version: str) -> Release | None:
        for release in self.releases:
            if release.version == version:
                return release
        return None


def parse_sections(text: str) -> list[tuple[str, str]]:
    """Split a changelog into (heading, body) pairs in document order."""
    sections: list[tuple[str, str]] = []
    matches = list(SECTION_HEADING.finditer(text))
    for index, match in enumerate(matches):
        start = match.end()
        end = (
            matches[index + 1].start()
            if index + 1 < len(matches)
            else len(text)
        )
        sections.append((match.group(1).strip(), text[start:end].strip()))
    return sections


def summary_paragraph(body: str) -> str:
    """Return a section's first paragraph, stopping at bullets or headings."""
    lines: list[str] = []
    started = False
    for line in body.splitlines():
        stripped = line.strip()
        if not started:
            if stripped:
                started = True
                lines.append(stripped)
            continue
        if not stripped or stripped.startswith(("- ", "##")):
            break
        lines.append(stripped)
    return " ".join(lines)


def load(path: Path) -> Changelog | None:
    """Read a changelog, or return None when the skill has never been released.

    A changelog holds released history and nothing else. Draft sections were
    removed in favour of commit bodies, so any other heading is an error rather
    than a register this reader has to understand.
    """
    if not path.is_file():
        return None
    return load_text(path.read_text(encoding="utf-8"), path)


def load_text(text: str, path: Path) -> Changelog:
    """Parse changelog text; `path` names it in error messages."""
    releases: list[Release] = []
    for heading, body in parse_sections(text):
        match = RELEASE_HEADING.match(heading)
        if not match:
            raise ValueError(
                f"{path}: section heading is not a linked and dated version: "
                f"{heading!r}. A changelog holds released history only; a "
                "pending change is recorded in its commit body."
            )

        version, url, date = match.groups()
        asset = ASSET_URL.match(url)
        if not asset:
            raise ValueError(
                f"{path}: version {version} must link to a release asset as "
                f"https://github.com/<owner>/<repository>/releases/download/"
                f"<tag>/<skill-name>.zip, not {url!r}"
            )
        releases.append(
            Release(
                version=version,
                date=date,
                tag=asset.group(1),
                asset=asset.group(2),
                asset_url=url,
                summary=summary_paragraph(body),
            )
        )

    if not releases:
        raise ValueError(
            f"{path}: contains no released version. Delete the changelog until "
            "the skill's first release."
        )

    return Changelog(path=path, releases=tuple(releases))
