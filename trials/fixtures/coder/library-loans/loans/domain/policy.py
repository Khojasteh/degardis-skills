"""Lending rules: due dates, fines, and who may borrow."""

from datetime import timedelta
from decimal import Decimal

from loans.storage import json_store

LOAN_DAYS = 14
DAILY_FINE = Decimal("0.25")
FINE_CAP = Decimal("5.00")
MAX_OVERDUE = 3


def due_date(borrowed_on):
    """A book is due ``LOAN_DAYS`` days after it is borrowed."""
    return borrowed_on + timedelta(days=LOAN_DAYS)


def fine(loan, today):
    """The fine owed on ``loan``: a daily amount for each late day, capped."""
    end = loan.returned_on or today
    days_late = (end - loan.due_on).days
    if days_late <= 0:
        return Decimal("0.00")
    return min(DAILY_FINE * days_late, FINE_CAP)


def may_borrow(member_id, today, path=None):
    """A member with ``MAX_OVERDUE`` or more overdue loans may not borrow."""
    loans = json_store.load_loans(path)
    overdue = [
        loan
        for loan in loans
        if loan.member_id == member_id and loan.is_overdue(today)
    ]
    return len(overdue) < MAX_OVERDUE
