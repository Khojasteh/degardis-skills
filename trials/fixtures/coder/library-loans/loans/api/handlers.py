"""Borrowing and returning books at the circulation desk."""

from loans import plugins
from loans.domain import policy
from loans.domain.models import Loan
from loans.storage import json_store


def describe_loan(loan, today):
    """One line describing ``loan`` as the desk and reminders show it."""
    line = "%s: %s due %s" % (loan.loan_id, loan.isbn, loan.due_on.isoformat())
    owed = policy.fine(loan, today)
    if owed:
        line += ", fine %s" % owed
    return line


def borrow(member_id, isbn, today, path=None):
    """Lend ``isbn`` to ``member_id`` unless the lending rules refuse it."""
    if not policy.may_borrow(member_id, today, path):
        return {"ok": False, "reason": "too many overdue loans"}
    loans = json_store.load_loans(path)
    loan = Loan(
        loan_id="L%04d" % (len(loans) + 1),
        member_id=member_id,
        isbn=isbn,
        borrowed_on=today,
        due_on=policy.due_date(today),
    )
    json_store.save_loans(loans + [loan], path)
    return {"ok": True, "loan_id": loan.loan_id, "due_on": loan.due_on.isoformat()}


def give_back(loan_id, today, path=None, outbox=None, config_path=None):
    """Record the return of ``loan_id`` and return the fine owed on it.

    When a fine is owed and an ``outbox`` is given, a reminder for the fine is
    composed into it.
    """
    loans = json_store.load_loans(path)
    for index, loan in enumerate(loans):
        if loan.loan_id == loan_id:
            if loan.returned_on is not None:
                raise ValueError("%s was already returned" % loan_id)
            loans[index] = loan.returned(today)
            json_store.save_loans(loans, path)
            owed = policy.fine(loans[index], today)
            if owed and outbox is not None:
                outbox.append(plugins.notifier(config_path)(loans[index], today))
            return owed
    raise KeyError(loan_id)
