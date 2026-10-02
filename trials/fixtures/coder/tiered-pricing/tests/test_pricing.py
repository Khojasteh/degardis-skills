import unittest
from decimal import Decimal

from orders import pricing


class DiscountRateTests(unittest.TestCase):
    def test_small_order_earns_nothing(self):
        self.assertEqual(pricing.discount_rate(Decimal("50.00")), Decimal("0"))

    def test_mid_order_earns_two_percent(self):
        self.assertEqual(pricing.discount_rate(Decimal("250.00")), Decimal("0.02"))

    def test_large_order_earns_five_percent(self):
        self.assertEqual(pricing.discount_rate(Decimal("750.00")), Decimal("0.05"))

    def test_very_large_order_earns_ten_percent(self):
        self.assertEqual(pricing.discount_rate(Decimal("1500.00")), Decimal("0.10"))


class DiscountAmountTests(unittest.TestCase):
    def test_amount_is_rounded_to_the_cent(self):
        self.assertEqual(pricing.discount_amount(Decimal("464.50")), Decimal("9.29"))

    def test_amount_rounds_half_up(self):
        self.assertEqual(pricing.discount_amount(Decimal("612.50")), Decimal("30.63"))

    def test_no_discount_leaves_the_subtotal_alone(self):
        self.assertEqual(pricing.discounted_total(Decimal("80.00")), Decimal("80.00"))


if __name__ == "__main__":
    unittest.main()
