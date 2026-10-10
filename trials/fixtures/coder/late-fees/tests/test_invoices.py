import json
import os
import tempfile
import unittest
from datetime import date

from billing import invoices


class LedgerTestCase(unittest.TestCase):
    def setUp(self):
        handle, self.path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(handle, "w", encoding="utf-8") as ledger:
            json.dump([], ledger)

    def tearDown(self):
        os.remove(self.path)


class DueDateTests(unittest.TestCase):
    def test_net30_customer_is_due_thirty_days_after_issue(self):
        self.assertEqual(invoices.due_date("C-001", date(2026, 9, 1)), date(2026, 10, 1))

    def test_net15_customer_is_due_fifteen_days_after_issue(self):
        self.assertEqual(invoices.due_date("C-002", date(2026, 9, 1)), date(2026, 9, 16))


class IssueTests(LedgerTestCase):
    def test_first_invoice_is_numbered_one(self):
        record = invoices.issue("C-001", "100", date(2026, 9, 1), path=self.path)
        self.assertEqual(record["number"], "INV-0001")

    def test_numbers_follow_issue_order(self):
        invoices.issue("C-001", "100", date(2026, 9, 1), path=self.path)
        record = invoices.issue("C-002", "50", date(2026, 9, 2), path=self.path)
        self.assertEqual(record["number"], "INV-0002")

    def test_total_is_rounded_half_up_to_the_cent(self):
        record = invoices.issue("C-001", "10.005", date(2026, 9, 1), path=self.path)
        self.assertEqual(record["total"], "10.01")

    def test_new_invoice_is_unpaid_and_not_overdue(self):
        record = invoices.issue("C-001", "100", date(2026, 9, 1), path=self.path)
        self.assertIsNone(record["paid_on"])
        self.assertIsNone(record["overdue_since"])


class PaymentTests(LedgerTestCase):
    def test_payment_records_the_date(self):
        invoices.issue("C-001", "100", date(2026, 9, 1), path=self.path)
        record = invoices.record_payment("INV-0001", date(2026, 9, 20), path=self.path)
        self.assertEqual(record["paid_on"], "2026-09-20")

    def test_unknown_invoice_is_rejected(self):
        with self.assertRaises(KeyError):
            invoices.record_payment("INV-0099", date(2026, 9, 20), path=self.path)


class OverdueTests(LedgerTestCase):
    def setUp(self):
        super().setUp()
        invoices.issue("C-002", "100", date(2026, 9, 1), path=self.path)  # due 2026-09-16

    def test_invoice_is_not_overdue_on_its_due_date(self):
        self.assertEqual(invoices.mark_overdue(date(2026, 9, 16), path=self.path), [])

    def test_unpaid_invoice_is_overdue_from_the_day_after_its_due_date(self):
        self.assertEqual(invoices.mark_overdue(date(2026, 9, 17), path=self.path), ["INV-0001"])
        self.assertEqual(invoices.load(self.path)[0]["overdue_since"], "2026-09-17")

    def test_paid_invoice_is_never_overdue(self):
        invoices.record_payment("INV-0001", date(2026, 9, 10), path=self.path)
        self.assertEqual(invoices.mark_overdue(date(2026, 10, 1), path=self.path), [])

    def test_overdue_invoice_is_marked_once(self):
        invoices.mark_overdue(date(2026, 9, 17), path=self.path)
        self.assertEqual(invoices.mark_overdue(date(2026, 9, 30), path=self.path), [])
        self.assertEqual(invoices.load(self.path)[0]["overdue_since"], "2026-09-17")


if __name__ == "__main__":
    unittest.main()
