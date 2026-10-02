# Contributing

## Tests

The suite runs on the standard library's `unittest` runner. Nothing else is
installed in CI, and adding a test dependency needs a separate discussion.

```console
python -m unittest discover -s tests -t .
```

Every test lives in `tests/`, is named `test_*.py`, and runs without network
access or a writable home directory.

## Documentation

`docs/` states what we promise customers. When behaviour changes, the page that
describes it changes in the same commit, and so does any docstring that repeats
the same promise.

## Style

Standard library only. Money is `decimal.Decimal`, never `float`.
