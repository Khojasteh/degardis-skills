"""Product catalogue."""

from decimal import Decimal


class UnknownProduct(LookupError):
    """Raised when a SKU is not in the catalogue."""


CATALOG = {
    "DESK-01": ("Standing desk", Decimal("425.00")),
    "CHAIR-02": ("Task chair", Decimal("125.00")),
    "LAMP-03": ("Desk lamp", Decimal("39.50")),
    "MAT-04": ("Anti-fatigue mat", Decimal("62.00")),
    "ARM-05": ("Monitor arm", Decimal("88.75")),
}


def name_of(sku):
    """Return the display name for ``sku``."""
    try:
        return CATALOG[sku][0]
    except KeyError:
        raise UnknownProduct(sku) from None


def unit_price(sku):
    """Return the list price for ``sku``."""
    try:
        return CATALOG[sku][1]
    except KeyError:
        raise UnknownProduct(sku) from None
