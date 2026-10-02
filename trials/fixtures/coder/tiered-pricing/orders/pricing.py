"""Volume discounts applied to an order subtotal."""

from decimal import Decimal, ROUND_HALF_UP

CENT = Decimal("0.01")

#: Tiers, highest threshold first.
DISCOUNT_TIERS = (
    (Decimal("1000.00"), Decimal("0.10")),
    (Decimal("500.00"), Decimal("0.05")),
    (Decimal("100.00"), Decimal("0.02")),
)


def discount_rate(subtotal):
    """Return the volume discount rate earned by ``subtotal``.

    A subtotal above 100.00 earns 2%, above 500.00 earns 5%, and above
    1000.00 earns 10%. Smaller subtotals earn nothing.
    """
    for threshold, rate in DISCOUNT_TIERS:
        if subtotal > threshold:
            return rate
    return Decimal("0")


def discount_amount(subtotal):
    """Return the money taken off ``subtotal``, rounded to the cent."""
    raw = subtotal * discount_rate(subtotal)
    return raw.quantize(CENT, rounding=ROUND_HALF_UP)


def discounted_total(subtotal):
    """Return ``subtotal`` with its volume discount applied."""
    return subtotal - discount_amount(subtotal)
