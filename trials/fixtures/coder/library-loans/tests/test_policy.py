import os
import unittest
from datetime import date
from decimal import Decimal

from loans.domain import policy
from loans.domain.models import Loan
from tests.helpers import loan_file, row


def loan(due_on, returned_on=None):
    return Loan("L1", "M-1", "978-0-00-000000-0", date(2026, 1, 1), due_on, returned_on)


class DueDate(unittest.TestCase):
    def test_due_fourteen_days_after_borrowing(self):
        self.assertEqual(policy.due_date(date(2026, 3, 1)), date(2026, 3, 15))


class Fine(unittest.TestCase):
    def test_no_fine_on_or_before_the_due_date(self):
        self.assertEqual(policy.fine(loan(date(2026, 3, 15)), date(2026, 3, 15)), Decimal("0.00"))

    def test_daily_fine_for_each_late_day(self):
        self.assertEqual(policy.fine(loan(date(2026, 3, 15)), date(2026, 3, 19)), Decimal("1.00"))

    def test_fine_is_capped(self):
        self.assertEqual(policy.fine(loan(date(2026, 3, 15)), date(2026, 6, 1)), Decimal("5.00"))

    def test_returned_loan_stops_accruing(self):
        returned = loan(date(2026, 3, 15), returned_on=date(2026, 3, 17))
        self.assertEqual(policy.fine(returned, date(2026, 6, 1)), Decimal("0.50"))


class MayBorrow(unittest.TestCase):
    def setUp(self):
        self.path = loan_file([
            row("L1", "M-1", "2026-02-01"),
            row("L2", "M-1", "2026-02-02"),
            row("L3", "M-1", "2026-02-03"),
            row("L4", "M-2", "2026-02-01"),
        ])

    def tearDown(self):
        os.remove(self.path)

    def test_three_overdue_loans_refuse_borrowing(self):
        self.assertFalse(policy.may_borrow("M-1", date(2026, 3, 1), self.path))

    def test_fewer_overdue_loans_allow_borrowing(self):
        self.assertTrue(policy.may_borrow("M-2", date(2026, 3, 1), self.path))


if __name__ == "__main__":
    unittest.main()
