import unittest

from tuner.report import format_result
from tuner.search import Result


class FormatResultTest(unittest.TestCase):
    def test_shows_the_best_point_and_its_loss(self):
        result = Result({"workers": 4}, 0.25, 3)
        self.assertEqual(format_result(result), "best: workers=4  loss 25.0%  (3 evaluated)")

    def test_marks_an_early_stop(self):
        result = Result({"workers": 4, "batch": 32}, 0.0, 7, stopped_early=True)
        self.assertEqual(
            format_result(result),
            "best: batch=32, workers=4  loss 0.0%  (7 evaluated)  [target reached]",
        )

    def test_reports_when_no_point_beat_the_worst_loss(self):
        result = Result(None, 1.0, 4)
        self.assertEqual(format_result(result), "no point beat the worst possible loss (4 evaluated)")


if __name__ == "__main__":
    unittest.main()
