"""Carts and the subtotal a cart presents to pricing."""

from decimal import Decimal

from orders import catalog, pricing


class Cart:
    """An ordered collection of SKU/quantity lines."""

    def __init__(self):
        self._lines = []

    def add(self, sku, quantity=1):
        """Add ``quantity`` of ``sku``, merging into an existing line."""
        if quantity < 1:
            raise ValueError("quantity must be at least 1")
        catalog.unit_price(sku)
        for index, (existing, count) in enumerate(self._lines):
            if existing == sku:
                self._lines[index] = (existing, count + quantity)
                return
        self._lines.append((sku, quantity))

    @property
    def lines(self):
        """Return the lines as a list of ``(sku, quantity)`` pairs."""
        return list(self._lines)

    def subtotal(self):
        """Return the sum of every line's list price times its quantity."""
        total = Decimal("0.00")
        for sku, quantity in self._lines:
            total += catalog.unit_price(sku) * quantity
        return total

    def total(self):
        """Return the subtotal with the volume discount applied."""
        return pricing.discounted_total(self.subtotal())
