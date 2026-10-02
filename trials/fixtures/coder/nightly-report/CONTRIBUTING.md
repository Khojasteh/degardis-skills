# Contributing

## Tests

Standard library `unittest` only; CI installs nothing else.

```console
python -m unittest discover -s tests -t .
```

## Benchmarks

`bench/run_bench.py` builds a fixed synthetic day and times the render. Run it
before and after anything that claims to change the report's cost, and paste the
numbers into the change description.

```console
python bench/run_bench.py
```

## Style

Standard library only. No new dependencies without a discussion first.
