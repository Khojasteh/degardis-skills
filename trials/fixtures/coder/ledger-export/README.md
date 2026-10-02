# export

Ledger exports for the accounts team. One posted ledger line becomes one row, in
whichever format the caller asks for.

Supported formats: CSV and JSON.

```console
python -m export.cli --format json --out ledger.json
```

The nightly job writes every format at once; see `docs/formats.md` for what each
one promises.
