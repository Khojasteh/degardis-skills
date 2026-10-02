# Benchmarks

`run_bench.py` builds one fixed synthetic day from `synthetic.py` and times
`reporting.render.build_report` on it. The seed is pinned, so two runs on the
same machine compare.

`render_profile.txt` is the last profile we captured:

```console
python -X dev -m cProfile -s cumtime bench/run_bench.py --accounts 2500 --rows 40000
```

It was taken on a developer laptop, not on the batch host.

The default size is a tenth of a production night in each dimension, because a
full night does not finish on a laptop while you wait. Pass `--accounts` and
`--rows` to change it.

The harness sets `REPORTING_DEBUG=1` before importing the package, which is what
we want while developing: a malformed synthetic day should fail rather than
render.
