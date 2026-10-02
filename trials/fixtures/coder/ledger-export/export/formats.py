"""Serializers for ledger entries, and the registry every exporter reads."""

import json

from .records import FIELDS


def to_csv(entries):
    """Return ``entries`` as CSV.

    A header row of the field names, then one row per entry. A field holding a
    comma, a double quote, or a newline is wrapped in double quotes, and a
    double quote inside such a field is doubled.
    """
    lines = [",".join(FIELDS)]
    for entry in entries:
        lines.append(",".join(_csv_field(value) for value in entry.as_dict().values()))
    return "\n".join(lines) + "\n"


def _csv_field(value):
    """Return ``value`` quoted for CSV where the CSV rules require it."""
    if any(character in value for character in ',"\n'):
        return '"' + value.replace('"', '""') + '"'
    return value


def to_json(entries):
    """Return ``entries`` as a two-space indented JSON array of objects."""
    return json.dumps([entry.as_dict() for entry in entries], indent=2) + "\n"


#: Every format the exporters offer, keyed by the name the documentation uses.
FORMATTERS = {
    "csv": to_csv,
    "json": to_json,
}
