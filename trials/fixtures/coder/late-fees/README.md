# billing

Invoicing for the accounts team: customer payment terms, invoice issue and due
dates, payments, and the nightly run that marks unpaid invoices overdue.

- `billing/customers.py` — customer records and payment terms
- `billing/invoices.py` — invoice records in the ledger: issue, payment, overdue status
- `billing/nightly.py` — the nightly billing run
- `data/invoices.json` — the invoice ledger

What customers are promised is in [docs/billing.md](docs/billing.md). Approved
work that is not built yet is described alongside it in `docs/`.

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to run the tests.
