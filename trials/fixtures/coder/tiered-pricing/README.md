# orders

Order pricing for the storefront checkout: catalogue lookup, cart totals,
volume discounts, and invoice records.

## Layout

- `orders/catalog.py` — product records and price lookup
- `orders/cart.py` — line items and subtotals
- `orders/pricing.py` — volume discount tiers
- `orders/invoice.py` — invoice records written to `data/invoices.json`
- `orders/customers.py` — customer records and billing addresses

The discount tiers customers are promised are in [docs/pricing.md](docs/pricing.md).

## Running

```console
python -m unittest discover -s tests -t .
```
