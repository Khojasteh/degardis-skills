"""Column, money, and number formatting for the report body."""

COLUMNS = (
    ("account_name", 28, "left"),
    ("region", 10, "left"),
    ("plan_tier", 10, "left"),
    ("events", 8, "right"),
    ("amount", 14, "right"),
)


def pad(text, width, align):
    """Return ``text`` padded to ``width``."""
    text = str(text)
    if len(text) >= width:
        return text[:width]
    filler = ""
    while len(filler) < width - len(text):
        filler += " "
    return filler + text if align == "right" else text + filler


def money(value):
    """Return ``value`` as a grouped amount with two decimal places."""
    whole, _, fraction = ("%.2f" % value).partition(".")
    sign = ""
    if whole.startswith("-"):
        sign, whole = "-", whole[1:]
    grouped = ""
    while len(whole) > 3:
        grouped = "," + whole[-3:] + grouped
        whole = whole[:-3]
    return sign + whole + grouped + "." + fraction


def header():
    """Return the column header line."""
    line = ""
    for name, width, align in COLUMNS:
        line += pad(name.replace("_", " ").title(), width, align)
    return line


def row(entry):
    """Return one rendered table line for ``entry``."""
    line = ""
    for name, width, align in COLUMNS:
        value = entry[name]
        if name == "amount":
            value = money(value)
        line += pad(value, width, align)
    return line
