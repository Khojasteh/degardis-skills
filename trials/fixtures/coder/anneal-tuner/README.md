# tuner

Parameter search for tuning service configuration. Describe the candidate
values for each setting, write an objective that scores one combination, and
let a search find the best combination: `grid_search` scores every one, and
`anneal` explores spaces too large for that.

```python
from tuner import Space, anneal
from tuner.report import format_result, leaderboard

space = Space(workers=[2, 4, 8, 16], batch=[16, 32, 64, 128], prefetch=[0, 1, 2, 4])
result = anneal(my_objective, space, steps=200)
print(format_result(result))
print("\n".join(leaderboard(result)))
```

Objectives score a combination with a loss from 0 (perfect) to 1 (worst).
Measurements can be kept between sessions with `ScoreCache`. See
`docs/scoring.md` for the full contract and `examples/` for a worked tuning
session.
