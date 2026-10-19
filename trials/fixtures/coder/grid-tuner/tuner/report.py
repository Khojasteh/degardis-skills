"""One-line summaries of a search result for logs and the command line."""

from tuner.search import Result


def format_result(result: Result) -> str:
    """Summarize the best point, its loss, and how the search ended."""
    if result.best_params is None:
        return f"no point beat the worst possible loss ({result.evaluations} evaluated)"
    params = ", ".join(f"{name}={value}" for name, value in sorted(result.best_params.items()))
    line = f"best: {params}  loss {result.best_score:.1%}  ({result.evaluations} evaluated)"
    if result.stopped_early:
        line += "  [target reached]"
    return line
