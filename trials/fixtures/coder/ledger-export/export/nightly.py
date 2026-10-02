"""The nightly job that writes the ledger in every registered format."""

from pathlib import Path

from .formats import FORMATTERS


def export_all(entries, directory):
    """Write ``entries`` in every registered format into ``directory``.

    Each file is named ``ledger`` with the format name as its extension. The
    paths written are returned in format-name order.
    """
    written = []
    for name in sorted(FORMATTERS):
        path = Path(directory) / f"ledger.{name}"
        path.write_text(FORMATTERS[name](entries), encoding="utf-8", newline="")
        written.append(path)
    return written
