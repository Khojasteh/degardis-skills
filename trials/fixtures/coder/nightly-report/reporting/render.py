"""Assembles the nightly report text."""

import argparse

from reporting import aggregate, enrich, format as fmt, loader


def build_report(date, rows, accounts, plans):
    """Return the whole report text for ``date``."""
    enriched = enrich.enrich(rows, accounts, plans)
    account_totals = aggregate.by_account(enriched)
    region_totals = aggregate.by_region(enriched)
    movers = aggregate.top_movers(account_totals)

    text = ""
    text += "Nightly account activity - %s\n" % date
    text += "=" * 72 + "\n\n"

    text += "Top accounts\n"
    text += fmt.header() + "\n"
    text += "-" * 72 + "\n"
    for entry in movers:
        text += fmt.row(entry) + "\n"

    text += "\nAll accounts\n"
    text += fmt.header() + "\n"
    text += "-" * 72 + "\n"
    for entry in account_totals:
        text += fmt.row(entry) + "\n"

    text += "\nBy region\n"
    for entry in region_totals:
        text += "%s  %s events  %s\n" % (
            fmt.pad(entry["region"], 10, "left"),
            fmt.pad(entry["events"], 8, "right"),
            fmt.money(entry["amount"]),
        )

    text += "\n%d accounts, %d rows\n" % (len(account_totals), len(enriched))
    return text


def render(date, out_path=None):
    """Build the report for ``date`` and write it to ``out_path``."""
    rows = loader.load_activity(date)
    accounts = loader.load_accounts()
    plans = loader.load_plans()
    text = build_report(date, rows, accounts, plans)
    if out_path:
        with open(out_path, "w", encoding="utf-8") as handle:
            handle.write(text)
    return text


def main(argv=None):
    parser = argparse.ArgumentParser(description="Render the nightly report")
    parser.add_argument("--date", required=True)
    parser.add_argument("--out")
    args = parser.parse_args(argv)
    text = render(args.date, args.out)
    if not args.out:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
