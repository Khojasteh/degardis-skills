import unittest

from tuner.report import format_result, histogram, leaderboard
from tuner.search import Result


def result_with(*losses):
    history = [({"n": index}, loss) for index, loss in enumerate(losses)]
    best = min(history, key=lambda entry: entry[1])
    return Result(best[0], best[1], len(history), history)


class FormatResultTest(unittest.TestCase):
    def test_shows_the_best_point_and_its_loss(self):
        result = Result({"timeout_ms": 200, "pool": 16}, 0.25, 15)
        self.assertEqual(
            format_result(result), "best: pool=16,timeout_ms=200  loss 0.2500  (15 evaluated)"
        )

    def test_marks_an_early_stop(self):
        result = Result({"n": 2}, 0.0, 2, stopped_early=True)
        self.assertEqual(format_result(result), "best: n=2  loss 0.0000  (2 evaluated)  [target reached]")


class LeaderboardTest(unittest.TestCase):
    def test_lists_the_best_points_first(self):
        lines = leaderboard(result_with(0.5, 0.1, 0.9, 0.3), size=3)
        self.assertEqual(lines, ["0.1000  n=1", "0.3000  n=3", "0.5000  n=0"])


class HistogramTest(unittest.TestCase):
    def test_counts_losses_per_bin(self):
        lines = histogram(result_with(0.05, 0.15, 0.17, 0.95, 1.0), bins=10, width=4)
        counts = [int(line.split()[1]) for line in lines]
        self.assertEqual(counts, [1, 2, 0, 0, 0, 0, 0, 0, 0, 2])
        self.assertEqual(lines[1], "0.1-0.2    2 ####")


if __name__ == "__main__":
    unittest.main()
