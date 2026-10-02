import unittest

from reporting import format as fmt


class PadTests(unittest.TestCase):
    def test_left_pads_on_the_right(self):
        self.assertEqual(fmt.pad("ab", 5, "left"), "ab   ")

    def test_right_pads_on_the_left(self):
        self.assertEqual(fmt.pad("ab", 5, "right"), "   ab")

    def test_overlong_text_is_truncated(self):
        self.assertEqual(fmt.pad("abcdef", 4, "left"), "abcd")


class MoneyTests(unittest.TestCase):
    def test_groups_thousands(self):
        self.assertEqual(fmt.money(1234567.5), "1,234,567.50")

    def test_small_amount_is_left_alone(self):
        self.assertEqual(fmt.money(12.3), "12.30")

    def test_negative_amount_keeps_its_sign(self):
        self.assertEqual(fmt.money(-4200.0), "-4,200.00")


class RowTests(unittest.TestCase):
    def test_row_is_the_sum_of_its_column_widths(self):
        entry = {
            "account_name": "Account 00001",
            "region": "eu-west",
            "plan_tier": "team",
            "events": 3,
            "amount": 1200.0,
        }
        self.assertEqual(len(fmt.row(entry)), 70)


if __name__ == "__main__":
    unittest.main()
