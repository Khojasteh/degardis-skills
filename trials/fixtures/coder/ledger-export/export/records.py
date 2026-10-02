"""The ledger entry an export serializes."""

from dataclasses import dataclass

#: The field order every export format writes.
FIELDS = ("entry_id", "account", "description", "amount")


@dataclass(frozen=True)
class Entry:
    """One posted ledger line.

    ``amount`` is the posted decimal string, never a float, so an export can
    write it back exactly as it was posted.
    """

    entry_id: str
    account: str
    description: str
    amount: str

    def as_dict(self):
        """Return this entry as a mapping in :data:`FIELDS` order."""
        return {name: getattr(self, name) for name in FIELDS}
