import unittest

from tuner import Space, grid_search


class Bowl:
    """Loss is the mean squared distance from a centre inside the unit square."""

    def __init__(self, cx, cy):
        self.cx, self.cy = cx, cy

    def evaluate(self, params):
        return ((params["x"] - self.cx) ** 2 + (params["y"] - self.cy) ** 2) / 2


class Scripted:
    """Returns preset losses in evaluation order and counts calls."""

    def __init__(self, *losses):
        self._losses = list(losses)
        self.calls = 0

    def evaluate(self, params):
        self.calls += 1
        return self._losses.pop(0)


GRID = [0.0, 0.25, 0.5, 0.75, 1.0]


class GridSearchTest(unittest.TestCase):
    def test_finds_the_point_with_the_lowest_loss(self):
        result = grid_search(Bowl(0.6, 0.6), Space(x=GRID, y=GRID))
        self.assertEqual(result.best_params, {"x": 0.5, "y": 0.5})
        self.assertAlmostEqual(result.best_score, 0.01)
        self.assertEqual(result.evaluations, 25)
        self.assertFalse(result.stopped_early)

    def test_a_tie_keeps_the_point_evaluated_first(self):
        result = grid_search(Scripted(0.40, 0.25, 0.25), Space(workers=[2, 4, 8]))
        self.assertEqual(result.best_params, {"workers": 4})
        self.assertEqual(result.best_score, 0.25)

    def test_an_improvement_within_tolerance_is_a_tie(self):
        result = grid_search(Scripted(0.3000, 0.2995), Space(n=[1, 2]))
        self.assertEqual(result.best_params, {"n": 1})

    def test_stops_once_the_target_is_reached(self):
        objective = Scripted(0.5, 0.1, 0.05, 0.0)
        result = grid_search(objective, Space(n=[1, 2, 3, 4]), target=0.1)
        self.assertEqual(result.best_params, {"n": 2})
        self.assertTrue(result.stopped_early)
        self.assertEqual(objective.calls, 2)

    def test_stops_on_a_perfect_result_by_default(self):
        result = grid_search(Bowl(0.5, 0.5), Space(x=GRID, y=GRID))
        self.assertEqual(result.best_params, {"x": 0.5, "y": 0.5})
        self.assertTrue(result.stopped_early)
        self.assertEqual(result.evaluations, 13)

    def test_a_repeated_point_is_evaluated_once(self):
        objective = Scripted(0.6, 0.4)
        result = grid_search(objective, Space(n=[1, 1, 2]))
        self.assertEqual(objective.calls, 2)
        self.assertEqual(result.evaluations, 2)
        self.assertEqual(result.best_params, {"n": 2})

    def test_max_evals_caps_the_evaluations(self):
        result = grid_search(Bowl(1.0, 1.0), Space(x=GRID, y=GRID), max_evals=5)
        self.assertEqual(result.evaluations, 5)
        self.assertEqual(result.best_params, {"x": 0.0, "y": 1.0})

    def test_a_loss_rounded_past_the_scale_is_clamped(self):
        result = grid_search(Scripted(1.0000001, -0.0000001), Space(n=[1, 2]))
        self.assertEqual(result.history[0][1], 1.0)
        self.assertEqual(result.best_score, 0.0)

    def test_improvement_compares_the_best_with_the_first_point(self):
        result = grid_search(Scripted(0.8, 0.3, 0.5), Space(n=[1, 2, 3]))
        self.assertAlmostEqual(result.improvement(), 0.5)


if __name__ == "__main__":
    unittest.main()
