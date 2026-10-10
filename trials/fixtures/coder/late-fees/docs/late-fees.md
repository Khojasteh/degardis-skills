# Late fees

Status: approved by Finance, not built yet.

## Fee

An overdue invoice that is still unpaid when its grace period ends is charged
one late fee: 2% of the invoice total or $15.00, whichever is greater, rounded
to the cent with halves rounded up. No invoice is ever charged a second late
fee.

The grace period starts on the day the invoice becomes overdue. Finance will
set its length before launch.

A charged fee is recorded in the ledger on the invoice it belongs to, in a
`late_fee` field holding the amount. The invoice's `total` does not change.

## Not decided yet

Finance has not decided who charges the fee. Either this billing package
charges it, in the nightly billing run, or the payment processor does: the
processor can add the fee to the payment request it sends the customer, and it
lists every fee it charged in its daily settlement file, which this package
would then read to record each fee in the ledger.
