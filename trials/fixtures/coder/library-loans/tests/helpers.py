import json
import os
import tempfile


def loan_file(rows):
    """Write ``rows`` to a temporary loan file and return its path."""
    handle, path = tempfile.mkstemp(suffix=".json")
    with os.fdopen(handle, "w", encoding="utf-8") as out:
        json.dump(rows, out)
    return path


def row(loan_id, member_id, due_on, returned_on=None, borrowed_on="2026-01-01"):
    return {
        "loan_id": loan_id,
        "member_id": member_id,
        "isbn": "978-0-00-000000-0",
        "borrowed_on": borrowed_on,
        "due_on": due_on,
        "returned_on": returned_on,
    }
