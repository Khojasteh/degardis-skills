import unittest

from tuner import CachedObjective, normalize


class Counting:
    def __init__(self, losses):
        self._losses = losses
        self.calls = 0

    def evaluate(self, params):
        self.calls += 1
        return self._losses[params["n"]]


class NormalizeTest(unittest.TestCase):
    def test_divides_by_the_worst_cost(self):
        self.assertEqual(normalize(50.0, 200.0), 0.25)

    def test_caps_at_one(self):
        self.assertEqual(normalize(300.0, 200.0), 1.0)

    def test_rejects_a_non_positive_worst(self):
        with self.assertRaises(ValueError):
            normalize(1.0, 0.0)


class CachedObjectiveTest(unittest.TestCase):
    def test_evaluates_each_distinct_point_once(self):
        inner = Counting({1: 0.3, 2: 0.1})
        cached = CachedObjective(inner)
        for n in (1, 2, 1, 2, 1):
            cached.evaluate({"n": n})
        self.assertEqual(inner.calls, 2)
        self.assertEqual(cached.evaluations, 2)

    def test_tracks_the_lowest_loss_seen(self):
        cached = CachedObjective(Counting({1: 0.3, 2: 0.1, 3: 0.5}))
        for n in (1, 2, 3):
            cached.evaluate({"n": n})
        self.assertEqual(cached.lowest, 0.1)


if __name__ == "__main__":
    unittest.main()
