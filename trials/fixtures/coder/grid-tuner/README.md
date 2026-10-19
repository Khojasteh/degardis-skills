# tuner

Exhaustive parameter search for tuning service configuration. You describe the
candidate values for each setting, write an objective that scores one
combination, and `grid_search` tries the combinations and returns the best one.

```python
from tuner import Space, grid_search
from tuner.report import format_result

space = Space(workers=[2, 4, 8], batch=[16, 32, 64])
result = grid_search(my_objective, space)
print(format_result(result))
```

An objective scores a combination with a loss between 0 and 1, where 0 is a
perfect result; `tuner.objective.normalize` turns a raw cost into that scale.
See `docs/scoring.md` for the full contract and `examples/` for a worked
objective.
