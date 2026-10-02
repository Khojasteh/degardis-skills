"""Times the render on a fixed synthetic day.

Run from the repository root:

    python bench/run_bench.py
    python bench/run_bench.py --accounts 500 --rows 5000
"""

import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("REPORTING_DEBUG", "1")

from bench import synthetic  # noqa: E402
from reporting import render  # noqa: E402


def main(argv=None):
    parser = argparse.ArgumentParser(description="Time the nightly render")
    parser.add_argument("--accounts", type=int, default=2500)
    parser.add_argument("--rows", type=int, default=40000)
    parser.add_argument("--repeat", type=int, default=1)
    args = parser.parse_args(argv)

    activity, accounts, plans = synthetic.build_day(args.accounts, args.rows)
    durations = []
    for _ in range(args.repeat):
        started = time.perf_counter()
        text = render.build_report("2026-08-04", activity, accounts, plans)
        durations.append(time.perf_counter() - started)

    print("rows      %d" % args.rows)
    print("accounts  %d" % args.accounts)
    print("output    %d bytes" % len(text))
    for index, duration in enumerate(durations, start=1):
        print("run %-5d %.3f s" % (index, duration))
    print("best      %.3f s" % min(durations))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
