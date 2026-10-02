"""The CSV and JSON serializers."""

import json
import unittest

from export.formats import to_csv, to_json
from export.records import Entry

ENTRIES = [
    Entry("E-0001", "ACC-1001", "Monthly retainer", "1250.00"),
    Entry("E-0002", "ACC-1002", "Refund, see note\nApproved by finance", "-75.50"),
]


class ToCsvTests(unittest.TestCase):
    def test_the_first_row_is_the_header(self):
        header = to_csv(ENTRIES).splitlines()[0]
        self.assertEqual(header, "entry_id,account,description,amount")

    def test_a_plain_row_is_written_unquoted(self):
        self.assertIn("E-0001,ACC-1001,Monthly retainer,1250.00", to_csv(ENTRIES))

    def test_a_field_holding_a_comma_or_a_newline_is_quoted(self):
        self.assertIn('"Refund, see note\nApproved by finance"', to_csv(ENTRIES))

    def test_the_output_ends_with_a_newline(self):
        self.assertTrue(to_csv(ENTRIES).endswith("\n"))


class ToJsonTests(unittest.TestCase):
    def test_each_object_holds_the_fields_in_order(self):
        loaded = json.loads(to_json(ENTRIES))
        self.assertEqual(
            list(loaded[0]), ["entry_id", "account", "description", "amount"]
        )

    def test_a_value_survives_the_round_trip_unaltered(self):
        loaded = json.loads(to_json(ENTRIES))
        self.assertEqual(
            loaded[1]["description"], "Refund, see note\nApproved by finance"
        )

    def test_the_output_ends_with_a_newline(self):
        self.assertTrue(to_json(ENTRIES).endswith("\n"))
