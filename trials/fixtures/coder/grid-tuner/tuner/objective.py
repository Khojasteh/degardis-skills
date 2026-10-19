"""What a search optimizes: an objective scores one point of the space."""

from typing import Mapping, Protocol

Params = Mapping[str, object]


class Objective(Protocol):
    """Scores one point of the search space.

    ``evaluate`` returns a loss in [0, 1]: 0 is a perfect result and 1 is the
    worst the objective can report.
    """

    def evaluate(self, params: Params) -> float: ...


def normalize(raw: float, worst: float) -> float:
    """Map a raw cost in [0, worst] onto the loss scale, capping at 1."""
    if worst <= 0:
        raise ValueError("worst must be positive")
    return min(raw / worst, 1.0)


class CachedObjective:
    """Wraps an objective so each distinct point is evaluated only once.

    Useful when several searches share one expensive objective. ``lowest`` is
    the lowest loss any evaluation has returned so far.
    """

    def __init__(self, objective: Objective):
        self._objective = objective
        self._losses: dict[tuple, float] = {}
        self.lowest = 1.0

    def evaluate(self, params: Params) -> float:
        key = tuple(sorted(params.items()))
        if key not in self._losses:
            loss = self._objective.evaluate(params)
            self._losses[key] = loss
            self.lowest = min(self.lowest, loss)
        return self._losses[key]

    @property
    def evaluations(self) -> int:
        """How many distinct points the wrapped objective has scored."""
        return len(self._losses)
