import json
import os
import tempfile
import unittest
from datetime import date

from billing import invoices, nightly


class NightlyRunTests(unittest.TestCase):
    def setUp(self):
        handle, self.path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(handle, "w", encoding="utf-8") as ledger:
            json.dump([], ledger)
        invoices.issue("C-001", "100", date(2026, 9, 1), path=self.path)  # due 2026-10-01

    def tearDown(self):
        os.remove(self.path)

    def test_run_reports_newly_overdue_invoices(self):
        self.assertEqual(nightly.run(date(2026, 10, 2), path=self.path), {"overdue": ["INV-0001"]})

    def test_run_before_any_due_date_changes_nothing(self):
        self.assertEqual(nightly.run(date(2026, 9, 30), path=self.path), {"overdue": []})


if __name__ == "__main__":
    unittest.main()
