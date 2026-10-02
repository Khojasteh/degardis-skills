"""The nightly export job."""

import tempfile
import unittest
from pathlib import Path

from export.nightly import export_all
from export.records import Entry

ENTRIES = [Entry("E-0001", "ACC-1001", "Monthly retainer", "1250.00")]


class ExportAllTests(unittest.TestCase):
    def test_it_writes_one_file_per_registered_format(self):
        with tempfile.TemporaryDirectory() as directory:
            export_all(ENTRIES, directory)
            written = sorted(path.name for path in Path(directory).iterdir())
            self.assertEqual(written, ["ledger.csv", "ledger.json"])

    def test_it_returns_the_paths_it_wrote(self):
        with tempfile.TemporaryDirectory() as directory:
            paths = export_all(ENTRIES, directory)
            names = [path.name for path in paths]
            self.assertEqual(names, ["ledger.csv", "ledger.json"])

    def test_each_file_holds_that_format(self):
        with tempfile.TemporaryDirectory() as directory:
            export_all(ENTRIES, directory)
            written = (Path(directory) / "ledger.csv").read_text(encoding="utf-8")
            self.assertTrue(written.startswith("entry_id,account"))
