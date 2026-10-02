# reporting

Builds the nightly account activity report: loads the day's rows, attaches
customer and plan details, aggregates per account, and renders the text report
the finance team receives each morning.

## Layout

- `reporting/loader.py` — reads the day's rows and reference tables
- `reporting/enrich.py` — attaches customer, plan, and region details to rows
- `reporting/aggregate.py` — per-account and per-region totals
- `reporting/format.py` — number, money, and column formatting
- `reporting/render.py` — assembles the report text
- `bench/` — the benchmark harness and the profile captured from it

## Running

```console
python -m reporting.render --date 2026-08-04 --out nightly.txt
python -m unittest discover -s tests -t .
```

The nightly job runs this on the batch host at 02:00 UTC.
