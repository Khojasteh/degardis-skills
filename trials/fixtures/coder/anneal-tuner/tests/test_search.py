import unittest

from tuner import Space, anneal, grid_search

GRID = [round(i / 10, 1) for i in range(11)]


class Bowl:
    """Loss is the mean squared distance from a centre inside the unit square."""

    def __init__(self, cx, cy):
        self.cx, self.cy = cx, cy
        self.calls = 0

    def evaluate(self, point):
        self.calls += 1
        return ((point["x"] - self.cx) ** 2 + (point["y"] - self.cy) ** 2) / 2


class TwoValleys:
    """A shallow valley at x=0.2 and a deeper one at x=0.8."""

    def evaluate(self, point):
        x = point["x"]
        return min(0.3 + (x - 0.2) ** 2, (x - 0.8) ** 2)


class Scripted:
    """Returns preset losses in order."""

    def __init__(self, *losses):
        self._losses = list(losses)

    def evaluate(self, point):
        return self._losses.pop(0)


class GridSearchTest(unittest.TestCase):
    def test_finds_the_point_with_the_lowest_loss(self):
        result = grid_search(Bowl(0.33, 0.62), Space(x=GRID, y=GRID))
        self.assertEqual(result.best_point, {"x": 0.3, "y": 0.6})
        self.assertEqual(result.evaluations, 121)
        self.assertFalse(result.stopped_early)

    def test_a_tie_keeps_the_point_scored_first(self):
        result = grid_search(Scripted(0.4, 0.25, 0.25), Space(workers=[2, 4, 8]))
        self.assertEqual(result.best_point, {"workers": 4})

    def test_stops_once_the_target_is_reached(self):
        result = grid_search(Scripted(0.5, 0.1, 0.0), Space(n=[1, 2, 3]), target=0.1)
        self.assertEqual(result.best_point, {"n": 2})
        self.assertTrue(result.stopped_early)
        self.assertEqual(result.evaluations, 2)

    def test_stops_on_a_perfect_result_by_default(self):
        result = grid_search(Bowl(0.0, 0.2), Space(x=GRID, y=GRID))
        self.assertEqual(result.best_point, {"x": 0.0, "y": 0.2})
        self.assertTrue(result.stopped_early)
        self.assertEqual(result.evaluations, 3)

    def test_a_repeated_point_is_scored_once(self):
        objective = Bowl(0.5, 0.5)
        result = grid_search(objective, Space(x=[0.1, 0.1, 0.2], y=[0.5]))
        self.assertEqual(objective.calls, 2)
        self.assertEqual(result.evaluations, 2)


class AnnealTest(unittest.TestCase):
    def test_finds_the_bottom_of_a_bowl(self):
        result = anneal(Bowl(0.7, 0.2), Space(x=GRID, y=GRID), steps=200)
        self.assertEqual(result.best_point, {"x": 0.7, "y": 0.2})

    def test_leaves_a_shallow_valley_for_a_deeper_one(self):
        space = Space(x=[round(i / 20, 2) for i in range(21)])
        for seed in range(5):
            with self.subTest(seed=seed):
                result = anneal(TwoValleys(), space, steps=150, seed=seed)
                self.assertEqual(result.best_point, {"x": 0.8})

    def test_the_same_seed_gives_the_same_walk(self):
        space = Space(x=GRID, y=GRID)
        first = anneal(Bowl(0.4, 0.9), space, steps=60, seed=7)
        second = anneal(Bowl(0.4, 0.9), space, steps=60, seed=7)
        self.assertEqual(first.history, second.history)

    def test_never_scores_a_point_twice(self):
        objective = Bowl(0.5, 0.5)
        result = anneal(objective, Space(x=GRID[:4], y=GRID[:4]), steps=300)
        self.assertEqual(objective.calls, result.evaluations)
        self.assertLessEqual(result.evaluations, 16)

    def test_stops_once_the_target_is_reached(self):
        result = anneal(Bowl(0.5, 0.5), Space(x=GRID, y=GRID), steps=300, target=0.02)
        self.assertTrue(result.stopped_early)
        self.assertLessEqual(result.best_loss, 0.02)


if __name__ == "__main__":
    unittest.main()
