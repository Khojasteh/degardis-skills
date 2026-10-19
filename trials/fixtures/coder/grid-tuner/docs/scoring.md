# Scoring contract

This page is what `tuner` promises the teams that write objectives.

## Objectives

An objective has one method, `evaluate(params)`, which receives one point of
the search space as a mapping from parameter name to value and returns that
point's **loss**: a float in [0, 1], where 0 is a perfect result and 1 is the
worst result the objective can report.

Most objectives measure a raw cost first, such as latency in milliseconds or
spend in dollars. Map it onto the loss scale with
`tuner.objective.normalize(raw, worst)`, which divides by the worst cost you
expect and caps the result at 1.

A loss that rounding puts a hair outside [0, 1] is clamped onto the scale.

## Search

`grid_search(objective, space, target=0.0, tol=1e-3, max_evals=None)`
evaluates the points of `space` in the order `Space.points` yields them and
returns the point with the lowest loss.

- A point replaces the best so far only when its loss is lower by more than
  `tol`. Of two points whose losses tie, the one evaluated first is kept.
- The search stops early once the best loss is within `tol` of `target`. The
  default target, 0, stops only on a perfect result.
- A point the space yields more than once is evaluated once.
- `max_evals`, when given, caps the number of evaluations.

The `Result` holds the best point and its loss, the number of evaluations,
the evaluation history, and whether the search stopped early.

`CachedObjective` wraps an objective so that searches sharing it evaluate each
distinct point once; its `lowest` attribute is the lowest loss seen so far.

## Reports

`tuner.report.format_result` prints the best point and its loss as a
percentage of the worst possible result, for example `loss 12.5%`.

## Worked example

Searching `Space(workers=[2, 4, 8])` with an objective whose losses are 0.40,
0.25, and 0.25 returns `workers=4` with loss 0.25: the third point ties the
second and does not replace it. The report reads
`best: workers=4  loss 25.0%  (3 evaluated)`.
