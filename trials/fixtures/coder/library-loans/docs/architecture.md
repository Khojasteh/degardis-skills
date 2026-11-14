# Architecture

Status: accepted, 2025-03-04.

## Context

Lending rules change with library policy every year, and the rules have to be
testable without files, a mail relay, or the circulation desk. Storage is also
expected to change: the loan file was always meant to be temporary.

## Decision

The service is layered. Each package may import only the packages listed for
it:

| Package | May import |
| --- | --- |
| `loans.domain` | nothing inside `loans` |
| `loans.storage` | `loans.domain` |
| `loans.notify` | `loans.domain` |
| `loans.reports` | `loans.domain`, `loans.storage` |
| `loans.api` | `loans.domain`, `loans.storage`, and `loans.notify` through `loans.plugins` |

Only `loans.storage` reads or writes the loan file. Every other package that
needs loan records gets them through `loans.storage`.

```text
api ------> storage ------> domain
api ----------------------> domain
api ··(plugins)··> notify -> domain
reports --> storage ------> domain
reports ------------------> domain
```

## Enforcement

`tests/test_architecture.py` checks the domain rule on every test run.

## Planned

Loan records move from `data/loans.json` to SQLite during 2026. Under the
decision above, only `loans.storage` should need to change.
