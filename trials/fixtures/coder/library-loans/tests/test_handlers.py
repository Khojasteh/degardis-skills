import os
import unittest
from datetime import date
from decimal import Decimal

from loans.api import handlers
from loans.storage import json_store
from tests.helpers import loan_file, row


class Borrow(unittest.TestCase):
    def setUp(self):
        self.path = loan_file([row("L0001", "M-1", "2026-02-01", returned_on="2026-01-20")])

    def tearDown(self):
        os.remove(self.path)

    def test_borrow_records_a_new_loan(self):
        result = handlers.borrow("M-2", "978-0-00-000009-7", date(2026, 3, 1), self.path)
        self.assertEqual(result, {"ok": True, "loan_id": "L0002", "due_on": "2026-03-15"})
        self.assertEqual(len(json_store.load_loans(self.path)), 2)

    def test_borrow_refused_with_too_many_overdue_loans(self):
        os.remove(self.path)
        self.path = loan_file([row("L%d" % n, "M-1", "2026-02-0%d" % n) for n in (1, 2, 3)])
        result = handlers.borrow("M-1", "978-0-00-000009-7", date(2026, 3, 1), self.path)
        self.assertFalse(result["ok"])


class GiveBack(unittest.TestCase):
    def setUp(self):
        self.path = loan_file([row("L0001", "M-1", "2026-03-15")])

    def tearDown(self):
        os.remove(self.path)

    def test_on_time_return_owes_nothing_and_sends_nothing(self):
        outbox = []
        owed = handlers.give_back("L0001", date(2026, 3, 10), self.path, outbox)
        self.assertEqual(owed, Decimal("0.00"))
        self.assertEqual(outbox, [])

    def test_late_return_records_the_fine_and_composes_a_reminder(self):
        outbox = []
        owed = handlers.give_back("L0001", date(2026, 3, 19), self.path, outbox)
        self.assertEqual(owed, Decimal("1.00"))
        self.assertEqual(len(outbox), 1)
        self.assertIn("fine 1.00", outbox[0])
        self.assertEqual(json_store.load_loans(self.path)[0].returned_on, date(2026, 3, 19))

    def test_a_loan_cannot_be_returned_twice(self):
        handlers.give_back("L0001", date(2026, 3, 10), self.path)
        with self.assertRaises(ValueError):
            handlers.give_back("L0001", date(2026, 3, 19), self.path)

    def test_unknown_loan(self):
        with self.assertRaises(KeyError):
            handlers.give_back("L9999", date(2026, 3, 19), self.path)


if __name__ == "__main__":
    unittest.main()
