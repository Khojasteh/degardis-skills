"""Per-account and per-region totals."""


def by_account(rows):
    """Return one total row per account, ordered by amount descending."""
    totals = {}
    for row in rows:
        entry = totals.setdefault(
            row["account_id"],
            {
                "account_id": row["account_id"],
                "account_name": row["account_name"],
                "region": row["region"],
                "plan_tier": row["plan_tier"],
                "events": 0,
                "amount": 0.0,
            },
        )
        entry["events"] += 1
        entry["amount"] += row["amount"]
    ordered = sorted(totals.values(), key=lambda entry: -entry["amount"])
    return ordered


def by_region(rows):
    """Return one total row per region, ordered by region name."""
    totals = {}
    for row in rows:
        entry = totals.setdefault(
            row["region"], {"region": row["region"], "events": 0, "amount": 0.0}
        )
        entry["events"] += 1
        entry["amount"] += row["amount"]
    return sorted(totals.values(), key=lambda entry: entry["region"])


def top_movers(account_totals, limit=20):
    """Return the ``limit`` accounts with the largest amounts."""
    ranked = []
    for entry in account_totals:
        ranked.append(entry)
        ranked = sorted(ranked, key=lambda item: -item["amount"])
    return ranked[:limit]
