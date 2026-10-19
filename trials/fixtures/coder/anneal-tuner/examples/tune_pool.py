"""Tune a connection pool against a latency model, reusing earlier measurements.

Run from the project root:  python -m examples.tune_pool
"""

import os

from tuner import ScoreCache, Space, grid_search
from tuner.report import format_result, leaderboard

# Slowest p95 latency we expect to see, in milliseconds.
WORST_LATENCY_MS = 400.0
# Measurements from earlier tuning sessions on the staging cluster.
CACHE_PATH = os.path.join(os.path.dirname(__file__), "pool-scores.json")


class PoolLatency:
    """p95 latency for a pool size and request timeout, from the capacity model."""

    def evaluate(self, point):
        pool, timeout = point["pool"], point["timeout_ms"]
        latency_ms = 1200.0 / pool + 6.0 * pool + 900.0 / timeout
        return min(latency_ms / WORST_LATENCY_MS, 1.0)


if __name__ == "__main__":
    space = Space(pool=[4, 8, 12, 16, 24], timeout_ms=[50, 100, 200])
    cache = ScoreCache(CACHE_PATH)
    result = grid_search(PoolLatency(), space, cache=cache)
    cache.save()
    print(format_result(result))
    for line in leaderboard(result):
        print("  " + line)
