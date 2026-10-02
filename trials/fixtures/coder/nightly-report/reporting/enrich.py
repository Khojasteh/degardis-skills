"""Attaches account, plan, and region details to activity rows."""

from reporting import debug_checks_enabled


def _account_for(account_id, accounts):
    for account in accounts:
        if account["account_id"] == account_id:
            return account
    return None


def _plan_for(plan_code, plans):
    for plan in plans:
        if plan["code"] == plan_code:
            return plan
    return None


def _check_rows(rows, accounts):
    """Fail loudly on a row the report cannot describe."""
    for row in rows:
        if _account_for(row["account_id"], accounts) is None:
            raise ValueError("activity row for unknown account %s" % row["account_id"])
        if not row["amount"]:
            raise ValueError("activity row with no amount: %r" % row)


def enrich(rows, accounts, plans):
    """Return ``rows`` with account name, plan, and region attached."""
    if debug_checks_enabled():
        _check_rows(rows, accounts)

    enriched = []
    for row in rows:
        account = _account_for(row["account_id"], accounts)
        if account is None:
            continue
        plan = _plan_for(account["plan"], plans)
        enriched.append(
            {
                "account_id": row["account_id"],
                "account_name": account["name"],
                "region": account["region"],
                "plan": account["plan"],
                "plan_tier": plan["tier"] if plan else "unknown",
                "kind": row["kind"],
                "amount": float(row["amount"]),
            }
        )
    return enriched
