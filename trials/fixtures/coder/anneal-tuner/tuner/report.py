"""Text summaries of a search result for logs and the command line."""

from tuner.space import key


def format_result(result) -> str:
    """One line: the best point, its loss, and how the search ended."""
    if result.best_point is None:
        return f"nothing evaluated ({result.evaluations} evaluated)"
    line = f"best: {key(result.best_point)}  loss {result.best_loss:.4f}  ({result.evaluations} evaluated)"
    if result.stopped_early:
        line += "  [target reached]"
    return line


def leaderboard(result, size=3) -> list[str]:
    """The best ``size`` distinct points, best first, one line each."""
    ranked = sorted(result.history, key=lambda entry: entry[1])
    lines = []
    for point, loss in ranked[:size]:
        lines.append(f"{loss:.4f}  {key(point)}")
    return lines


def histogram(result, bins=10, width=40) -> list[str]:
    """How the evaluated losses are spread, as one bar per equal-width bin."""
    counts = [0] * bins
    for _, loss in result.history:
        counts[min(int(loss * bins), bins - 1)] += 1
    peak = max(counts) or 1
    lines = []
    for index, count in enumerate(counts):
        low, high = index / bins, (index + 1) / bins
        bar = "#" * round(width * count / peak)
        lines.append(f"{low:.1f}-{high:.1f} {count:4d} {bar}")
    return lines
