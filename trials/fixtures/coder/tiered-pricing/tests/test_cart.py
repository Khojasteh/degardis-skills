import unittest
from decimal import Decimal

from orders import catalog
from orders.cart import Cart


class CartTests(unittest.TestCase):
    def test_subtotal_sums_line_prices(self):
        cart = Cart()
        cart.add("CHAIR-02", 2)
        cart.add("LAMP-03")
        self.assertEqual(cart.subtotal(), Decimal("289.50"))

    def test_adding_the_same_sku_merges_the_line(self):
        cart = Cart()
        cart.add("CHAIR-02", 1)
        cart.add("CHAIR-02", 3)
        self.assertEqual(cart.lines, [("CHAIR-02", 4)])

    def test_unknown_sku_is_rejected(self):
        cart = Cart()
        with self.assertRaises(catalog.UnknownProduct):
            cart.add("NOPE-99")

    def test_quantity_must_be_positive(self):
        cart = Cart()
        with self.assertRaises(ValueError):
            cart.add("LAMP-03", 0)

    def test_total_applies_the_volume_discount(self):
        cart = Cart()
        cart.add("DESK-01", 2)
        self.assertEqual(cart.total(), Decimal("807.50"))


if __name__ == "__main__":
    unittest.main()
