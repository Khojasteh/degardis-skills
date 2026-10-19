# Scoring contract

This page is what `tuner` promises the teams that write objectives.

## Objectives

An objective has one method, `evaluate(point)`, which receives one point of
the search space as a mapping from parameter name to value and returns that
point's **loss**: a float in [0, 1], where 0 is a perfect result and 1 is the
worst result the objective can report.

Most objectives measure a raw cost first, such as latency in milliseconds or
spend in dollars. Divide it by the worst cost you expect and cap the result at
1, as `examples/tune_pool.py` does.

## Searches

Both searches return a `Result` with the best point, its loss, the number of
points scored, the scoring history in order, and whether the search stopped
early.

`grid_search(objective, space, target=0.0, cache=None)` scores every point of
the space in the order `Space.points` yields them and returns the one with the
lowest loss. Of two points with the same loss, the one scored first is kept.

`anneal(objective, space, steps=300, seed=0, target=0.0, cache=None)` is for
spaces too large to score whole. It walks between neighbouring points,
sometimes accepting a worse one so it can leave a local minimum, and restarts
from a random point when it stops making progress. The same seed gives the
same walk.

Both stop early once a loss at or below `target` is found. The default target,
0, stops only on a perfect result. Neither search scores the same point twice.

## Cached measurements

`ScoreCache(path)` keeps losses in a JSON file so that later tuning sessions
skip points already measured. Pass it as `cache=` to either search, and call
`save()` afterwards to keep new measurements.

## Reports

`tuner.report` turns a result into text:

- `format_result` gives one line with the best point and its loss, for
  example `best: pool=16,timeout_ms=200  loss 0.4387  (15 evaluated)`.
- `leaderboard` lists the best few points scored, best first.
- `histogram` shows how the losses spread across ten equal bins from 0 to 1.
