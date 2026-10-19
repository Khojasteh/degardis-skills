"""A discrete search space: named parameters, each with ordered candidate values."""

from itertools import product


class Space:
    """Every combination of the candidate values given for each parameter.

    Candidate values are kept in the order given, and a point's neighbours are
    the points that move one parameter to an adjacent value in that order.
    """

    def __init__(self, **choices):
        if not choices:
            raise ValueError("a space needs at least one parameter")
        for name, values in choices.items():
            if not values:
                raise ValueError(f"parameter {name!r} has no candidate values")
        self._names = sorted(choices)
        self._choices = {name: list(choices[name]) for name in self._names}

    def points(self):
        """Yield every combination as a dict, in a stable order."""
        for combo in product(*(self._choices[name] for name in self._names)):
            yield dict(zip(self._names, combo))

    def random_point(self, rng):
        """A point drawn uniformly using the given ``random.Random``."""
        return {name: rng.choice(values) for name, values in self._choices.items()}

    def neighbours(self, point):
        """The points one step away from ``point`` along a single parameter."""
        result = []
        for name in self._names:
            values = self._choices[name]
            index = values.index(point[name])
            for step in (-1, 1):
                if 0 <= index + step < len(values):
                    moved = dict(point)
                    moved[name] = values[index + step]
                    result.append(moved)
        return result


def key(point) -> str:
    """A stable text key for a point, used by caches and reports."""
    return ",".join(f"{name}={point[name]}" for name in sorted(point))
