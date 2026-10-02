import json
import os
import tempfile
import unittest

from orders import invoice
from orders.cart import Cart


class InvoiceTests(unittest.TestCase):
    def setUp(self):
        handle, self.path = tempfile.mkstemp(suffix=".json")
        os.close(handle)
        with open(self.path, "w", encoding="utf-8") as ledger:
            json.dump([], ledger)

    def tearDown(self):
        os.remove(self.path)

    def test_build_names_the_customer(self):
        cart = Cart()
        cart.add("LAMP-03")
        record = invoice.build("C-1001", cart)
        self.assertEqual(record["billed_to"], "Aurora Bindery")

    def test_issue_numbers_invoices_in_sequence(self):
        cart = Cart()
        cart.add("LAMP-03")
        first = invoice.issue("C-1001", cart, path=self.path)
        second = invoice.issue("C-1002", cart, path=self.path)
        self.assertEqual([first["number"], second["number"]], ["INV-0001", "INV-0002"])

    def test_issued_invoice_records_the_discounted_total(self):
        cart = Cart()
        cart.add("DESK-01", 2)
        record = invoice.issue("C-1003", cart, path=self.path)
        self.assertEqual(record["subtotal"], "850.00")
        self.assertEqual(record["total"], "807.50")


if __name__ == "__main__":
    unittest.main()
