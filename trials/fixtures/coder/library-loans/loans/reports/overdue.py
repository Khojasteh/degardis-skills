"""The nightly overdue report."""

import json
from datetime import date
from pathlib import Path

LOANS_FILE = Path(__file__).resolve().parents[2] / "data" / "loans.json"


def overdue_report(today, path=None):
    """One line per overdue loan, sorted by member."""
    with open(path or LOANS_FILE, encoding="utf-8") as handle:
        rows = json.load(handle)
    lines = []
    for row in rows:
        if row.get("returned_on") is None and date.fromisoformat(row["due_on"]) < today:
            lines.append("%s %s due %s" % (row["member_id"], row["isbn"], row["due_on"]))
    return "\n".join(sorted(lines))
