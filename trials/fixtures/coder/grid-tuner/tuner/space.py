"""A discrete search space: named parameters, each with candidate values."""

from itertools import product


class Space:
    """Every combination of the candidate values given for each parameter."""

    def __init__(self, **choices):
        if not choices:
            raise ValueError("a space needs at least one parameter")
        for name, values in choices.items():
            if not values:
                raise ValueError(f"parameter {name!r} has no candidate values")
        self._names = sorted(choices)
        self._choices = {name: list(choices[name]) for name in self._names}

    def points(self):
        """Yield every combination as a dict, in a stable order.

        Parameters vary in name order, the last name fastest. A candidate list
        that repeats a value yields the same point more than once.
        """
        for combo in product(*(self._choices[name] for name in self._names)):
            yield dict(zip(self._names, combo))

    def size(self) -> int:
        """The number of combinations ``points`` yields, repeats included."""
        total = 1
        for values in self._choices.values():
            total *= len(values)
        return total
