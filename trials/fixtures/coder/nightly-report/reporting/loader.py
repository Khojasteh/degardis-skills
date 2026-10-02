"""Reads the day's activity rows and the reference tables."""

import csv
import os

DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
)


def _read(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_activity(date, data_dir=DATA_DIR):
    """Return the activity rows recorded on ``date``."""
    rows = _read(os.path.join(data_dir, "activity.csv"))
    return [row for row in rows if row["date"] == date]


def load_accounts(data_dir=DATA_DIR):
    """Return every account record."""
    return _read(os.path.join(data_dir, "accounts.csv"))


def load_plans(data_dir=DATA_DIR):
    """Return every plan record."""
    return _read(os.path.join(data_dir, "plans.csv"))
