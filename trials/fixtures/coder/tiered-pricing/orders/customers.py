"""Customer records."""

CUSTOMERS = {
    "C-1001": {"name": "Aurora Bindery", "region": "eu-west", "terms": "net30"},
    "C-1002": {"name": "Pinewood Studios Ltd", "region": "eu-west", "terms": "prepaid"},
    "C-1003": {"name": "Harbour Analytics", "region": "us-east", "terms": "net30"},
    "C-1004": {"name": "Quill & Pane", "region": "us-east", "terms": "prepaid"},
}


class UnknownCustomer(LookupError):
    """Raised when a customer id is not on file."""


def record(customer_id):
    """Return the record for ``customer_id``."""
    try:
        return dict(CUSTOMERS[customer_id])
    except KeyError:
        raise UnknownCustomer(customer_id) from None


def display_name(customer_id):
    """Return the name to print on an invoice."""
    return record(customer_id)["name"]


def is_prepaid(customer_id):
    """Return whether ``customer_id`` pays before dispatch."""
    return record(customer_id)["terms"] == "prepaid"
