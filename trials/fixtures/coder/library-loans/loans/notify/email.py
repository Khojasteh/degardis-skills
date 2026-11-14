"""Composes overdue reminders. Delivery is left to the library's mail relay."""

from loans.api.handlers import describe_loan


def compose_reminder(loan, today):
    """The reminder message for ``loan`` as of ``today``."""
    return "To: %s\nSubject: Library loan reminder\n\n%s\n" % (
        loan.member_id,
        describe_loan(loan, today),
    )
