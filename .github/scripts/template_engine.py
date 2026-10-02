"""Small, dependency-free template helpers for repository generators."""

from __future__ import annotations

import re
from pathlib import Path


PLACEHOLDER = re.compile(r"{{\s*([^{}]+?)\s*}}")


def render_template(
    template: str,
    values: dict[str, str],
    template_path: Path,
) -> str:
    """Replace named placeholders and normalize generated Markdown spacing."""
    required = set(PLACEHOLDER.findall(template))
    missing = required - set(values)
    if missing:
        raise ValueError(
            f"{template_path}: no values supplied for "
            f"{', '.join(sorted(missing))}"
        )

    rendered = PLACEHOLDER.sub(lambda match: values[match.group(1)], template)
    return re.sub(r"\n{3,}", "\n\n", rendered).strip() + "\n"
