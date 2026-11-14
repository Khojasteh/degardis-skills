"""The loan record."""

from dataclasses import dataclass, replace
from datetime import date
from typing import Optional


@dataclass(frozen=True)
class Loan:
    loan_id: str
    member_id: str
    isbn: str
    borrowed_on: date
    due_on: date
    returned_on: Optional[date] = None

    def is_overdue(self, today):
        """True while the book is out after its due date."""
        return self.returned_on is None and today > self.due_on

    def returned(self, on):
        """Return a copy of this loan marked as returned ``on`` that day."""
        return replace(self, returned_on=on)
