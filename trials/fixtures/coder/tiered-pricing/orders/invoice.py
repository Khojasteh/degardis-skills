"""Invoice records, appended to the invoice ledger."""

import json
import os
from decimal import Decimal

from orders import customers, pricing

LEDGER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "invoices.json",
)


def _load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def _next_number(entries):
    if not entries:
        return "INV-0001"
    highest = max(int(entry["number"].split("-")[1]) for entry in entries)
    return "INV-%04d" % (highest + 1)


def build(customer_id, cart):
    """Return the invoice record for ``customer_id``'s ``cart``."""
    subtotal = cart.subtotal()
    return {
        "customer": customer_id,
        "billed_to": customers.display_name(customer_id),
        "lines": [{"sku": sku, "quantity": quantity} for sku, quantity in cart.lines],
        "subtotal": str(subtotal),
        "discount": str(pricing.discount_amount(subtotal)),
        "total": str(pricing.discounted_total(subtotal)),
    }


def issue(customer_id, cart, path=LEDGER):
    """Append an invoice for ``cart`` to the ledger and return it."""
    entries = _load(path)
    record = build(customer_id, cart)
    record["number"] = _next_number(entries)
    entries.append(record)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(entries, handle, indent=2)
        handle.write("\n")
    return record


def total_billed(path=LEDGER):
    """Return the sum of every issued invoice total."""
    return sum(Decimal(entry["total"]) for entry in _load(path))
