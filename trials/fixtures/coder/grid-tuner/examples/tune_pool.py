"""Tune a connection pool against a simulated latency model.

Run from the project root:  python -m examples.tune_pool
"""

from tuner import Space, grid_search, normalize
from tuner.report import format_result

# Slowest p95 latency we expect to see, in milliseconds.
WORST_LATENCY_MS = 400.0


class PoolLatency:
    """Simulated p95 latency for a pool size and request timeout."""

    def evaluate(self, params):
        pool, timeout = params["pool"], params["timeout_ms"]
        queueing = 1200.0 / pool
        overhead = 6.0 * pool
        retries = 900.0 / timeout
        latency_ms = queueing + overhead + retries
        return normalize(latency_ms, WORST_LATENCY_MS)


if __name__ == "__main__":
    space = Space(pool=[4, 8, 12, 16, 24], timeout_ms=[50, 100, 200])
    print(format_result(grid_search(PoolLatency(), space)))
