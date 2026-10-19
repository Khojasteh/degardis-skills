"""Searches over a Space for the point with the lowest loss."""

import math
import random
from dataclasses import dataclass, field

from tuner.space import key

# Annealing schedule. A worse neighbour is accepted with probability
# exp(-increase / temperature), and the temperature cools after every step.
START_TEMPERATURE = 0.05
COOLING = 0.97
# Restart from a random point after this many steps without real progress.
STALL_STEPS = 25
# The least improvement that counts as progress.
MIN_PROGRESS = 0.002


@dataclass
class Result:
    """The outcome of one search."""

    best_point: dict | None
    best_loss: float
    evaluations: int
    history: list = field(default_factory=list)
    stopped_early: bool = False


class _Evaluator:
    """Scores points for one search, consulting a cache and never repeating a point."""

    def __init__(self, objective, cache):
        self._objective = objective
        self._cache = cache
        self._seen = {}
        self.history = []

    def __call__(self, point):
        point_key = key(point)
        if point_key in self._seen:
            return self._seen[point_key]
        loss = self._cache.get(point) if self._cache is not None else None
        if loss is None:
            loss = self._objective.evaluate(point)
            if self._cache is not None:
                self._cache.put(point, loss)
        self._seen[point_key] = loss
        self.history.append((point, loss))
        return loss

    @property
    def evaluations(self):
        return len(self._seen)


def grid_search(objective, space, *, target=0.0, cache=None):
    """Score every point of ``space`` and return the one with the lowest loss.

    Of two points with the same loss, the one scored first is kept. The search
    stops early once a loss at or below ``target`` is found; the default, 0,
    stops only on a perfect result.
    """
    evaluate = _Evaluator(objective, cache)
    best_point, best_loss = None, math.inf
    stopped = False
    for point in space.points():
        loss = evaluate(point)
        if loss < best_loss:
            best_point, best_loss = point, loss
        if best_loss <= target:
            stopped = True
            break
    return Result(best_point, best_loss, evaluate.evaluations, evaluate.history, stopped)


def anneal(objective, space, *, steps=300, seed=0, target=0.0, cache=None):
    """Simulated annealing over ``space`` for spaces too large to score whole.

    Walks between neighbouring points, sometimes accepting a worse one so it
    can leave a local minimum, and restarts from a random point when progress
    stalls. Stops early once a loss at or below ``target`` is found. The same
    ``seed`` gives the same walk.
    """
    rng = random.Random(seed)
    evaluate = _Evaluator(objective, cache)
    current = space.random_point(rng)
    current_loss = evaluate(current)
    best_point, best_loss = current, current_loss
    temperature = START_TEMPERATURE
    stalled = 0
    stopped = best_loss <= target
    for _ in range(0 if stopped else steps):
        candidate = rng.choice(space.neighbours(current))
        loss = evaluate(candidate)
        increase = loss - current_loss
        if increase <= 0 or rng.random() < math.exp(-increase / temperature):
            current, current_loss = candidate, loss
        if loss < best_loss - MIN_PROGRESS:
            best_point, best_loss = candidate, loss
            stalled = 0
        else:
            stalled += 1
        if best_loss <= target:
            stopped = True
            break
        if stalled >= STALL_STEPS:
            current = space.random_point(rng)
            current_loss = evaluate(current)
            temperature = START_TEMPERATURE
            stalled = 0
        temperature *= COOLING
    return Result(best_point, best_loss, evaluate.evaluations, evaluate.history, stopped)
