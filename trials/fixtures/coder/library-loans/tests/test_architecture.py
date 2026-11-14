"""Guards the domain layer rule in docs/architecture.md."""

import ast
import unittest
from pathlib import Path

DOMAIN = Path(__file__).resolve().parents[1] / "loans" / "domain"


def imported_modules(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            yield node.module
        elif isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name


class DomainLayer(unittest.TestCase):
    def test_domain_does_not_import_the_api(self):
        for path in DOMAIN.glob("*.py"):
            for module in imported_modules(path):
                self.assertFalse(
                    module.startswith("loans.api"),
                    "%s imports %s" % (path.name, module),
                )


if __name__ == "__main__":
    unittest.main()
