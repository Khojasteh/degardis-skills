# Billing

## Invoices

Each invoice is numbered `INV-` followed by four digits, in the order invoices
are issued, and records its customer, issue date, due date, and total.

## Due dates

An invoice is due a number of days after it is issued, set by the customer's
payment terms: 15 days for `net15` and 30 days for `net30`.

## Overdue invoices

An invoice still unpaid after its due date becomes overdue on the day after
that date. The nightly billing run marks it overdue.

## Money

All amounts are in US dollars and are rounded to the cent, with halves rounded
up.
