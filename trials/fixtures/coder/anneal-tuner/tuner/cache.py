"""Scores kept on disk so that repeated tuning runs skip points already measured."""

import json
import os

from tuner.space import key


class ScoreCache:
    """A JSON file mapping each measured point to its loss.

    Measuring a real configuration can take minutes, so a tuning session keeps
    its measurements and later sessions reuse them. Call ``save`` to write new
    entries back.
    """

    def __init__(self, path):
        self.path = path
        self._scores = {}
        if os.path.exists(path):
            with open(path, encoding="utf-8") as handle:
                self._scores = json.load(handle)
        self._dirty = False

    def get(self, point):
        return self._scores.get(key(point))

    def put(self, point, loss):
        self._scores[key(point)] = loss
        self._dirty = True

    def __len__(self):
        return len(self._scores)

    def save(self):
        if not self._dirty:
            return
        with open(self.path, "w", encoding="utf-8") as handle:
            json.dump(self._scores, handle, indent=2, sort_keys=True)
            handle.write("\n")
        self._dirty = False
