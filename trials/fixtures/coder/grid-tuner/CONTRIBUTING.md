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

`docs/scoring.md` states what the library promises the teams that write
objectives. When behaviour changes, that page changes in the same commit, and
so does any docstring or example that repeats the same promise.

## Style

Standard library only.
