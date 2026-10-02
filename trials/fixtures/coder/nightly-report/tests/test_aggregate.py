import unittest

from reporting import aggregate

ROWS = [
    {
        "account_id": "A-1",
        "account_name": "One",
        "region": "eu-west",
        "plan_tier": "team",
        "kind": "api_call",
        "amount": 10.0,
    },
    {
        "account_id": "A-1",
        "account_name": "One",
        "region": "eu-west",
        "plan_tier": "team",
        "kind": "export",
        "amount": 5.0,
    },
    {
        "account_id": "A-2",
        "account_name": "Two",
        "region": "us-east",
        "plan_tier": "free",
        "kind": "api_call",
        "amount": 40.0,
    },
]


class ByAccountTests(unittest.TestCase):
    def test_totals_are_summed_per_account(self):
        totals = {entry["account_id"]: entry for entry in aggregate.by_account(ROWS)}
        self.assertEqual(totals["A-1"]["amount"], 15.0)
        self.assertEqual(totals["A-1"]["events"], 2)

    def test_largest_account_comes_first(self):
        self.assertEqual(aggregate.by_account(ROWS)[0]["account_id"], "A-2")


class ByRegionTests(unittest.TestCase):
    def test_regions_are_alphabetical(self):
        self.assertEqual(
            [entry["region"] for entry in aggregate.by_region(ROWS)],
            ["eu-west", "us-east"],
        )


class TopMoversTests(unittest.TestCase):
    def test_limit_is_respected_and_ordered(self):
        movers = aggregate.top_movers(aggregate.by_account(ROWS), limit=1)
        self.assertEqual([entry["account_id"] for entry in movers], ["A-2"])


if __name__ == "__main__":
    unittest.main()
