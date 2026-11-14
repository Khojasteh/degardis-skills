# loans

The circulation service for a small lending library: borrowing and returning
books, due dates and fines, overdue reminders, and the nightly overdue report.

## Layout

- `loans/domain/` — loans and the lending rules: due dates, fines, and who may borrow
- `loans/storage/` — loan records kept in `data/loans.json`
- `loans/api/` — handlers the circulation desk calls
- `loans/notify/` — overdue reminder messages
- `loans/reports/` — the nightly overdue report
- `loans/plugins.py` — loads the notifier named in `config.json`

The service keeps a clean, layered design; the layering rule is recorded in
[docs/architecture.md](docs/architecture.md).

## Running

```console
python -m unittest discover -s tests -t .
```
