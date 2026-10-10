"""Customer records and their payment terms."""

#: Days from issue to due date for each payment term.
TERMS_DAYS = {"net15": 15, "net30": 30}

CUSTOMERS = {
    "C-001": {"name": "Example Customer One", "terms": "net30"},
    "C-002": {"name": "Example Customer Two", "terms": "net15"},
    "C-003": {"name": "Example Customer Three", "terms": "net30"},
}


def terms_days(customer_id):
    """Return how many days after issue ``customer_id``'s invoices fall due."""
    return TERMS_DAYS[CUSTOMERS[customer_id]["terms"]]
