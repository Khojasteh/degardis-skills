# Performance

## What the nightly job owes

The nightly report is scheduled at 02:00 UTC and must be in the finance team's
inbox before 03:00 UTC, so the render has to finish inside 15 minutes on the
batch host with the rest of the window left for delivery.

A normal night is around 400,000 activity rows against 25,000 accounts.
Month-end is roughly three times the rows against the same accounts.

## Where the numbers live

- Per-stage p95 and the wall-clock history of every nightly run are on the
  reporting dashboard at `https://metrics.internal.example/d/reporting-nightly`.
  It needs an on-call account.
- The batch host keeps the raw job logs under `/var/log/reporting/nightly-*.log`
  for 30 days. Ops grants access per request.
- `bench/` holds what can be measured on a developer machine without either of
  those.

## Budgets

| Stage | Budget |
| --- | --- |
| Load | 120 s |
| Enrich | 300 s |
| Aggregate | 240 s |
| Format and render | 240 s |

These were set when the report was written and have not been revisited since
the account count doubled.
