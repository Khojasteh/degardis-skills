"""The command-line entry point for a one-off export."""

import argparse
import sys

from .formats import FORMATTERS


def build_parser():
    """Return the argument parser the console script uses."""
    parser = argparse.ArgumentParser(
        prog="ledger-export",
        description="Export ledger entries in one of the documented formats.",
    )
    parser.add_argument(
        "--format",
        choices=("csv", "json"),
        default="csv",
        help="output format; see docs/formats.md",
    )
    parser.add_argument(
        "--out",
        help="write to this file instead of standard output",
    )
    return parser


def run(entries, argv=None):
    """Render ``entries`` under the parsed arguments and return the exit code."""
    arguments = build_parser().parse_args(argv)
    rendered = FORMATTERS[arguments.format](entries)
    if arguments.out:
        with open(arguments.out, "w", encoding="utf-8", newline="") as handle:
            handle.write(rendered)
    else:
        sys.stdout.write(rendered)
    return 0
