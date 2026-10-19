"""Exhaustive search of a Space for the point with the lowest loss."""

from dataclasses import dataclass, field

WORST_LOSS = 1.0


@dataclass
class Result:
    """The outcome of one search."""

    best_params: dict | None
    best_score: float
    evaluations: int
    history: list = field(default_factory=list)
    stopped_early: bool = False

    def improvement(self) -> float:
        """How much the best point improved on the first point evaluated."""
        if not self.history:
            return 0.0
        return self.history[0][1] - self.best_score


def grid_search(objective, space, *, target=0.0, tol=1e-3, max_evals=None):
    """Evaluate the points of ``space`` and return the one with the lowest loss.

    A point replaces the best so far only when its loss is lower by more than
    ``tol``, so of two points that tie, the one evaluated first is kept. The
    search stops early once the best loss is within ``tol`` of ``target``; the
    default target, 0, is a perfect result. A point the space yields more than
    once is evaluated once. ``max_evals`` caps the number of evaluations.

    ``history`` lists each evaluated point with its loss, in evaluation order.
    """
    best_params, best_score = None, WORST_LOSS
    seen = {}
    history = []
    stopped = False
    for params in space.points():
        if max_evals is not None and len(seen) >= max_evals:
            break
        key = tuple(sorted(params.items()))
        if key in seen:
            continue
        score = _score(objective, params)
        seen[key] = score
        history.append((params, score))
        if score < best_score - tol:
            best_params, best_score = params, score
        if best_score <= target + tol:
            stopped = True
            break
    return Result(best_params, best_score, len(seen), history, stopped)


def _score(objective, params) -> float:
    loss = objective.evaluate(params)
    # Floating-point rounding can put a loss a hair outside the scale.
    return min(max(loss, 0.0), WORST_LOSS)
