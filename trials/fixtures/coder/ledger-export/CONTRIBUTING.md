# Contributing

## Tests

The suite runs on the standard library's `unittest` runner. Nothing else is
installed in CI, and adding a test dependency needs a separate discussion.

```console
python -m unittest discover -s tests -t .
```

Every test lives in `tests/`, is named `test_*.py`, and runs without network
access.

## Documentation

`docs/formats.md` is what the accounts team and every downstream consumer read as
the promise. A change to what a format produces changes that page in the same
commit, and so does `README.md` where it repeats the same promise.

## Style

Standard library only. Amounts stay decimal strings and are never parsed into a
float on the way through an export.
