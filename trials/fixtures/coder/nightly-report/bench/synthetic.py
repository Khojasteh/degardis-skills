"""Builds a fixed synthetic day so benchmark runs are comparable."""

import random

REGIONS = ("eu-west", "eu-north", "us-east", "us-west", "ap-south")
PLANS = (
    {"code": "P-FREE", "tier": "free", "monthly": "0"},
    {"code": "P-TEAM", "tier": "team", "monthly": "49"},
    {"code": "P-BIZ", "tier": "business", "monthly": "199"},
    {"code": "P-ENT", "tier": "enterprise", "monthly": "999"},
)
KINDS = ("api_call", "export", "seat_change", "storage", "support_ticket")
SEED = 20260804


def build_day(accounts=2500, rows=40000, date="2026-08-04", seed=SEED):
    """Return ``(activity, accounts, plans)`` for one deterministic day."""
    rng = random.Random(seed)
    account_records = []
    for index in range(accounts):
        account_records.append(
            {
                "account_id": "A-%05d" % index,
                "name": "Account %05d" % index,
                "region": REGIONS[index % len(REGIONS)],
                "plan": PLANS[index % len(PLANS)]["code"],
            }
        )

    activity = []
    for _ in range(rows):
        account = account_records[rng.randrange(accounts)]
        activity.append(
            {
                "date": date,
                "account_id": account["account_id"],
                "kind": KINDS[rng.randrange(len(KINDS))],
                "amount": "%.2f" % (rng.random() * 500),
            }
        )

    return activity, account_records, [dict(plan) for plan in PLANS]
