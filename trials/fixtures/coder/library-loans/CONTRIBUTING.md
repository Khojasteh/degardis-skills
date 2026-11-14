# Contributing

## Tests

The suite runs on the standard library's `unittest` runner. Nothing else is
installed in CI, and adding a test dependency needs a separate discussion.

```console
python -m unittest discover -s tests -t .
```

Every test lives in `tests/`, is named `test_*.py`, and runs without network
access or a writable home directory.

## Architecture

`docs/architecture.md` is the service's architecture decision record. Amend it
by adding a dated section below the decision; do not rewrite the decision in
place.

## Style

Standard library only. Money is `decimal.Decimal`, never `float`.
