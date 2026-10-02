# Export formats

Every export writes the same four fields, always in this order:

`entry_id`, `account`, `description`, `amount`

`amount` is a decimal string exactly as it was posted, including a leading minus
for a credit. A `description` may hold a comma, a tab, or a newline, so each
format below says what it does about those.

| Format | Extension | Status |
| ------ | --------- | ------ |
| CSV    | `.csv`    | shipped |
| JSON   | `.json`   | shipped |
| TSV    | `.tsv`    | planned |

`--format` accepts every format listed above whose status is shipped, and the
nightly job writes one file per registered format into its output directory,
named `ledger` with the format's extension.

## CSV

A header row of the four field names separated by commas, then one row per entry
in the same order. A field holding a comma, a double quote, or a newline is
wrapped in double quotes, and a double quote inside such a field is doubled.
Lines end with a single newline and the file ends with one.

## JSON

A JSON array of objects, one per entry, each holding the four fields in the
order above, indented by two spaces. The file ends with a single newline.

## TSV

For the spreadsheet import the accounts team runs each month, which cannot read
our quoted CSV.

A header row of the four field names separated by single tab characters, then one
line per entry, fields in the same order, separated by single tab characters.
Lines end with a single newline and the file ends with one.

TSV has no quoting convention, so a value is never wrapped. Instead, inside a
field value:

- a backslash is written as `\\`
- a tab is written as `\t`
- a newline is written as `\n`

A consumer reverses those three substitutions to recover the posted value, and
nothing else in a value is altered.

### Worked example

The entry `E-0002` / `ACC-1002` / `Refund, see note` + newline +
`Approved by finance` / `-75.50` is one TSV line reading:

```text
E-0002	ACC-1002	Refund, see note\nApproved by finance	-75.50
```

The comma needs nothing done to it, and the newline has become the two
characters `\` and `n`.
