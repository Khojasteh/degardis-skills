"""Nightly account activity report."""

import os

__version__ = "2.4.1"


def debug_checks_enabled():
    """Return whether the extra invariant checks run.

    The batch host leaves ``REPORTING_DEBUG`` unset. Development and the
    benchmark harness turn it on so a malformed day fails loudly instead of
    producing a wrong report.
    """
    return os.environ.get("REPORTING_DEBUG") == "1"
