"""Invoice records in the invoice ledger: issue, payment, and overdue status."""

import json
import os
from datetime import date, timedelta
from decimal import ROUND_HALF_UP, Decimal

from billing import customers

CENT = Decimal("0.01")

LEDGER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "invoices.json",
)


def load(path=LEDGER):
    """Return every ledger entry, oldest first."""
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def _save(entries, path):
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(entries, handle, indent=2)
        handle.write("\n")


def _next_number(entries):
    if not entries:
        return "INV-0001"
    highest = max(int(entry["number"].split("-")[1]) for entry in entries)
    return "INV-%04d" % (highest + 1)


def due_date(customer_id, issued_on):
    """Return the date an invoice issued to ``customer_id`` on ``issued_on`` is due."""
    return issued_on + timedelta(days=customers.terms_days(customer_id))


def issue(customer_id, total, issued_on, path=LEDGER):
    """Append an invoice for ``total`` to the ledger and return it."""
    entries = load(path)
    record = {
        "number": _next_number(entries),
        "customer": customer_id,
        "issued_on": issued_on.isoformat(),
        "due_on": due_date(customer_id, issued_on).isoformat(),
        "total": str(Decimal(total).quantize(CENT, rounding=ROUND_HALF_UP)),
        "paid_on": None,
        "overdue_since": None,
    }
    entries.append(record)
    _save(entries, path)
    return record


def record_payment(number, paid_on, path=LEDGER):
    """Mark invoice ``number`` paid on ``paid_on`` and return it."""
    entries = load(path)
    for entry in entries:
        if entry["number"] == number:
            entry["paid_on"] = paid_on.isoformat()
            _save(entries, path)
            return entry
    raise KeyError(number)


def mark_overdue(today, path=LEDGER):
    """Mark unpaid invoices past their due date overdue and return their numbers.

    An unpaid invoice becomes overdue on the day after its due date. Invoices
    already marked are left as they are.
    """
    entries = load(path)
    marked = []
    for entry in entries:
        due_on = date.fromisoformat(entry["due_on"])
        if entry["paid_on"] is None and entry["overdue_since"] is None and today > due_on:
            entry["overdue_since"] = (due_on + timedelta(days=1)).isoformat()
            marked.append(entry["number"])
    if marked:
        _save(entries, path)
    return marked
