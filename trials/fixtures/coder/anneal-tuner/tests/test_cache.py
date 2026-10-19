import json
import os
import tempfile
import unittest

from tuner import ScoreCache, Space, grid_search


class Counting:
    def __init__(self, losses):
        self._losses = losses
        self.calls = []

    def evaluate(self, point):
        self.calls.append(point["n"])
        return self._losses[point["n"]]


class ScoreCacheTest(unittest.TestCase):
    def setUp(self):
        self._dir = tempfile.TemporaryDirectory()
        self.path = os.path.join(self._dir.name, "scores.json")

    def tearDown(self):
        self._dir.cleanup()

    def test_saved_losses_are_read_back(self):
        cache = ScoreCache(self.path)
        cache.put({"n": 1, "m": 2}, 0.25)
        cache.save()
        again = ScoreCache(self.path)
        self.assertEqual(again.get({"m": 2, "n": 1}), 0.25)
        self.assertEqual(len(again), 1)

    def test_a_search_skips_points_already_cached(self):
        with open(self.path, "w", encoding="utf-8") as handle:
            json.dump({"n=2": 0.1}, handle)
        objective = Counting({1: 0.5, 2: 0.9, 3: 0.7})
        result = grid_search(objective, Space(n=[1, 2, 3]), cache=ScoreCache(self.path))
        self.assertEqual(objective.calls, [1, 3])
        self.assertEqual(result.best_point, {"n": 2})

    def test_new_measurements_are_kept_after_save(self):
        cache = ScoreCache(self.path)
        grid_search(Counting({1: 0.5, 2: 0.3}), Space(n=[1, 2]), cache=cache)
        cache.save()
        with open(self.path, encoding="utf-8") as handle:
            self.assertEqual(json.load(handle), {"n=1": 0.5, "n=2": 0.3})


if __name__ == "__main__":
    unittest.main()
