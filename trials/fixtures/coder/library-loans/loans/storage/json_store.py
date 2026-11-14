"""Loan records kept in a JSON file."""

import json
import os
from datetime import date
from pathlib import Path

from loans.domain.models import Loan

DEFAULT_PATH = Path(__file__).resolve().parents[2] / "data" / "loans.json"


def _decode(raw):
    returned = raw.get("returned_on")
    return Loan(
        loan_id=raw["loan_id"],
        member_id=raw["member_id"],
        isbn=raw["isbn"],
        borrowed_on=date.fromisoformat(raw["borrowed_on"]),
        due_on=date.fromisoformat(raw["due_on"]),
        returned_on=date.fromisoformat(returned) if returned else None,
    )


def _encode(loan):
    return {
        "loan_id": loan.loan_id,
        "member_id": loan.member_id,
        "isbn": loan.isbn,
        "borrowed_on": loan.borrowed_on.isoformat(),
        "due_on": loan.due_on.isoformat(),
        "returned_on": loan.returned_on.isoformat() if loan.returned_on else None,
    }


def load_loans(path=None):
    """Every loan in the file, oldest first."""
    with open(path or DEFAULT_PATH, encoding="utf-8") as handle:
        return [_decode(raw) for raw in json.load(handle)]


def save_loans(loans, path=None):
    """Replace the file's contents with ``loans``, all at once or not at all."""
    target = Path(path or DEFAULT_PATH)
    staging = target.with_name(target.name + ".tmp")
    with open(staging, "w", encoding="utf-8") as handle:
        json.dump([_encode(loan) for loan in loans], handle, indent=2)
    os.replace(staging, target)
