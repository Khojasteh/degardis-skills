import unittest

from reporting import enrich, render

ACCOUNTS = [
    {"account_id": "A-1", "name": "One", "region": "eu-west", "plan": "P-TEAM"},
    {"account_id": "A-2", "name": "Two", "region": "us-east", "plan": "P-FREE"},
]
PLANS = [
    {"code": "P-TEAM", "tier": "team", "monthly": "49"},
    {"code": "P-FREE", "tier": "free", "monthly": "0"},
]
ACTIVITY = [
    {"date": "2026-08-04", "account_id": "A-1", "kind": "api_call", "amount": "10.00"},
    {"date": "2026-08-04", "account_id": "A-2", "kind": "export", "amount": "40.00"},
    {"date": "2026-08-04", "account_id": "A-1", "kind": "storage", "amount": "5.50"},
]


class EnrichTests(unittest.TestCase):
    def test_plan_tier_is_attached_from_the_account(self):
        rows = enrich.enrich(ACTIVITY, ACCOUNTS, PLANS)
        self.assertEqual(rows[0]["plan_tier"], "team")

    def test_amounts_become_numbers(self):
        rows = enrich.enrich(ACTIVITY, ACCOUNTS, PLANS)
        self.assertEqual(rows[1]["amount"], 40.0)

    def test_rows_for_unknown_accounts_are_dropped(self):
        extra = ACTIVITY + [
            {
                "date": "2026-08-04",
                "account_id": "A-9",
                "kind": "export",
                "amount": "1.00",
            }
        ]
        self.assertEqual(len(enrich.enrich(extra, ACCOUNTS, PLANS)), 3)


class BuildReportTests(unittest.TestCase):
    def setUp(self):
        self.text = render.build_report("2026-08-04", ACTIVITY, ACCOUNTS, PLANS)

    def test_report_names_the_date(self):
        self.assertIn("Nightly account activity - 2026-08-04", self.text)

    def test_report_has_all_three_sections(self):
        for heading in ("Top accounts", "All accounts", "By region"):
            self.assertIn(heading, self.text)

    def test_report_counts_accounts_and_rows(self):
        self.assertTrue(self.text.rstrip().endswith("2 accounts, 3 rows"))

    def test_totals_reach_the_body(self):
        self.assertIn("40.00", self.text)
        self.assertIn("15.50", self.text)


if __name__ == "__main__":
    unittest.main()
