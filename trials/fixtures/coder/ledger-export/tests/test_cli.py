"""The command-line entry point."""

import unittest

from export.cli import build_parser


class ParserTests(unittest.TestCase):
    def test_the_default_format_is_csv(self):
        self.assertEqual(build_parser().parse_args([]).format, "csv")

    def test_a_shipped_format_is_accepted(self):
        self.assertEqual(build_parser().parse_args(["--format", "json"]).format, "json")

    def test_a_format_we_do_not_offer_is_rejected(self):
        with self.assertRaises(SystemExit):
            build_parser().parse_args(["--format", "yaml"])
