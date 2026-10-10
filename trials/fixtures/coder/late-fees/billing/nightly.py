"""The nightly billing run."""

from datetime import date

from billing import invoices


def run(today=None, path=invoices.LEDGER):
    """Run the nightly billing steps for ``today`` and return what changed."""
    today = today or date.today()
    return {"overdue": invoices.mark_overdue(today, path=path)}
