"""Loads the notifier named in ``config.json``."""

import importlib
import json
from pathlib import Path

CONFIG = Path(__file__).resolve().parents[1] / "config.json"


def notifier(config_path=None):
    """The callable that composes an overdue reminder."""
    with open(config_path or CONFIG, encoding="utf-8") as handle:
        target = json.load(handle)["notifier"]
    module_name, _, attribute = target.partition(":")
    return getattr(importlib.import_module(module_name), attribute)
