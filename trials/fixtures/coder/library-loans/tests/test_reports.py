import os
import unittest
from datetime import date

from loans.reports.overdue import overdue_report
from tests.helpers import loan_file, row


class OverdueReport(unittest.TestCase):
    def setUp(self):
        self.path = loan_file([
            row("L1", "M-2", "2026-02-01"),
            row("L2", "M-1", "2026-02-01"),
            row("L3", "M-1", "2026-02-01", returned_on="2026-02-05"),
            row("L4", "M-3", "2026-04-01"),
        ])

    def tearDown(self):
        os.remove(self.path)

    def test_lists_unreturned_loans_past_due_sorted_by_member(self):
        self.assertEqual(
            overdue_report(date(2026, 3, 1), self.path),
            "M-1 978-0-00-000000-0 due 2026-02-01\nM-2 978-0-00-000000-0 due 2026-02-01",
        )


if __name__ == "__main__":
    unittest.main()
