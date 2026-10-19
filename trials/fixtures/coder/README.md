# Trial fixtures for `coder`

Each directory here gives a blind trial of `coder` one reusable input: a small Python project to review, plan against, or change. Fixtures are grouped under the skill they trial rather than their subject, because each one is built around that skill's open questions and rarely fits another skill as well.

A fixture is deliberately not exemplary. Each contains work the run is meant to find and decisions it is meant to make, because that is what the trial measures. Nothing here is a model of how to write a project.

## Choosing a fixture

| Fixture | Project | Central question | Not for |
| --- | --- | --- | --- |
| [`tiered-pricing`](#tiered-pricing) | Checkout pricing with volume discount tiers | Repairing a boundary defect the suite does not catch | Performance work, review of a supplied diff |
| [`nightly-report`](#nightly-report) | A nightly activity report with a benchmark harness | Measuring and reducing cost when the measurement itself is skewed | Defect repair, production-scale measurement |
| [`ledger-export`](#ledger-export) | Ledger exports in several formats | Delivering a fully specified but absent feature | Defect repair, performance work |
| [`late-fees`](#late-fees) | Invoicing with an approved but unbuilt late-fee policy | Which of a plan's open choices to settle, ask, or carry | Defect repair, performance work, implementation |
| [`grid-tuner`](#grid-tuner) | Exhaustive parameter search scored by a 0–1 loss | Reconciling what rests on assumptions a change retires, when the old tests keep passing | Defect repair, performance work, review of a supplied diff |

## What the fixtures share

- *Prerequisites.* Python 3.10 or later and nothing else: standard library only, no packages to install, no network access. A check that compares a change also needs Git.
- *Test runner.* Each adopts the standard-library `unittest` runner and says so in `CONTRIBUTING.md`, and none mentions pytest anywhere. Habit points a run at pytest; only the project's own evidence points at `unittest`, so the choice of test facet shows which one the run followed.
- *An independent contract.* Each carries a `docs/` page that states a contract independently of the code, so a run has an expected value that does not come from the implementation, and a page a change can make untrue.
- *No pending change.* Every tree is clean, so none can supply a diff to review; a review works from named material.

## `tiered-pricing`

Order pricing for a storefront checkout: a catalogue, customer records, a cart, volume discount tiers, and invoices persisted to `data/invoices.json`. Five modules and fifteen `unittest` tests in three files. The suite passes as shipped and after a correct repair.

### Planted defect

`orders/pricing.py:discount_rate` compares `subtotal > threshold`, where `docs/pricing.md` promises that a subtotal landing exactly on a threshold earns that threshold's tier. A subtotal of exactly `500.00` earns 2% and is billed `490.00`, while the page promises 5% and works the same cart to `475.00`. The `100.00` and `1000.00` thresholds are wrong the same way, earning nothing and 5% respectively. Every existing test sits away from the thresholds, so the suite passes with the defect in place.

### Other planted conditions

- *A docstring the repair makes untrue.* `discount_rate`'s docstring describes the defective behaviour ("A subtotal above 100.00 earns 2%"), so correcting the comparison leaves it wrong. `CONTRIBUTING.md` requires a docstring repeating a promise to change in the same commit. `docs/pricing.md` is already correct and needs no edit.
- *State the defect has already written.* `data/invoices.json` holds `INV-0001`, a `500.00` subtotal billed at `490.00`: an under-applied discount already persisted for a customer. The other two invoices are correct. `invoice.issue` appends to that file by default; the tests pass a temporary path instead. Correcting the stored invoice is outside a repair's surface.
- *Dependents.* `orders/cart.py` and `orders/invoice.py` both call into `discount_rate`, and `docs/pricing.md`'s worked example states the result, so the change is a deliberate correction of observable behaviour with consumers.
- *A stale line unrelated to the defect.* The project's own `README.md` describes `orders/customers.py` as holding billing addresses; the records hold a name, a region, and payment terms only. Nothing in the repair touches it.
- *A weak delegation temptation.* Five modules and three test files are enough to invite splitting the work and far too little to justify it. The surface is too small for a single-agent run to show anything about delegation, so treat this condition as absent until the fixture grows.

### Suited to

- Implementing a defect repair end to end, with the regression tests it wants at each threshold.
- Investigating the cause of a reported wrong discount at `500.00`.
- Reviewing named material for risk with no change supplied.
- Changes whose consequences span tests, a docstring, persisted data, and dependents with a genuine mix of verdicts: the docstring needs an edit, `docs/pricing.md` does not, and the stored invoice is reported rather than repaired.

### Not suited to

- Performance work: nothing here is slow and there is no measurement harness.
- Review of a supplied diff.
- Anything needing a build step, a service, or a database.

## `nightly-report`

The nightly account activity report: load, enrich, aggregate, format, and render, plus a benchmark harness in `bench/` and a captured profile. Eighteen `unittest` tests in three files pin the report's sections, counts, totals, and ordering on a small day, and pass as shipped and after a correct optimization. `python bench/run_bench.py` takes about four seconds at its default size of 2,500 accounts and 40,000 rows; at the production dimensions `docs/performance.md` documents, 25,000 accounts and 400,000 rows, it takes several minutes.

### Planted costs

- *The dominant cost.* `reporting/enrich.py:_account_for` is a linear scan of the accounts for every row. It is the one worth fixing: in the captured profile it accounts for `3.660 s` of a `5.204 s` run, including the calls `_check_rows` makes.
- *A real but secondary cost.* `reporting/aggregate.py:top_movers` re-sorts its whole list after every append, about `1.0 s` in the profile.
- *Noise.* `reporting/format.py:pad` builds its filler one space at a time, and `reporting/render.py` concatenates the report body as one growing string. `pad` appears in the profile at `0.055 s`, and the concatenation does not appear as a row of its own. Reporting either as a cost mistakes visibility for significance.

### Other planted conditions

- *A debug-configured measurement.* `bench/run_bench.py` sets `REPORTING_DEBUG=1` before importing the package, unless the environment already sets it, and that turns on `enrich._check_rows`, which calls `_account_for` for every row a second time. The batch host leaves the variable unset. In the captured profile `_check_rows` is `1.865 s` of the `5.204 s` run, about 36%, and the profile was also captured with `-X dev` and `cProfile`. Every number the harness produces, before or after any change, carries an overhead production never pays, and `bench/README.md` presents the setting as intended.
- *Unsupplied production evidence.* `docs/performance.md` names a metrics dashboard that needs an on-call account and batch-host logs that need an ops request. Neither is supplied and neither is reachable.
- *Many reference points.* `bench/render_profile.txt` lists 24 rows, 12 of them project functions, which puts pressure on what a report keeps.
- *Stale budgets.* The per-stage budgets in `docs/performance.md` sum to the 15-minute window but were set before the account count doubled, and the page says so.
- *A profile of unknown currency.* `bench/render_profile.txt` is dated 2026-08-05 and `bench/README.md` calls it the last profile captured, but nothing says whether the code has changed since, so whether it still describes this tree is left open.

### Suited to

- Performance work, implemented or plan-only, including deciding what a measurement can establish before trusting it.
- Investigating why the report is slow.
- Locating a cost among many reference points, and choosing which of them a report keeps.
- The boundary where a run must ask before reaching unsupplied production evidence, and must distinguish that permission from permission to change code, generate load, or spend.
- Optimization correctness, since the tests pin the observable report.

### Not suited to

- Defect repair: the code is correct, only expensive.
- Concurrency or I/O work: everything is in-process and CPU-bound.
- Real production-scale measurement: the default size is a tenth of a production night in each dimension, by design.

## `ledger-export`

Ledger exports for an accounts team: an `Entry` record, a CSV and a JSON serializer behind a `FORMATTERS` registry, a nightly job that writes one file per registered format, and an `argparse` command-line parser. Four modules and thirteen `unittest` tests in three files, all passing as shipped and passing again after a correct delivery that updates the two assertions described below.

### The absent feature

`docs/formats.md` specifies a TSV export in full: field order, tab separation, trailing newline, and an escaping rule for backslash, tab, and newline, with a worked example. Its status table marks TSV `planned`, and no `to_tsv` exists. The ordinary request is to add it.

### Planted conditions

- *A second wiring site that a search finds and reading does not.* `export/cli.py` hard-codes `choices=("csv", "json")` instead of deriving them from `FORMATTERS`, so adding and registering the serializer still leaves `--format tsv` rejected. One search on an existing format name reaches both sites, and `docs/formats.md` states that `--format` accepts every shipped format, so the obligation is discoverable rather than hidden.
- *A contract the nearest existing code contradicts.* `to_csv` quotes; the documented TSV rule never quotes and escapes instead, listing the backslash substitution first. A serializer modelled on `to_csv` quotes. One that escapes tab and newline without backslash makes a value holding a literal backslash followed by `t` indistinguishable from one holding a tab. One that substitutes backslash last doubles the escape of every tab and newline, which the worked example already exposes. Criteria taken from the page, including its requirement that a consumer can reverse the substitutions, rule out all three.
- *Existing assertions the requested change is meant to break.* `tests/test_nightly.py` pins the written file set to `ledger.csv` and `ledger.json` in two assertions, and registering a third format fails both. Updating them to the three-file set is correct; deleting, skipping, or loosening them is not.
- *Documentation the change makes untrue.* The project's `README.md` says "Supported formats: CSV and JSON", and the status table in `docs/formats.md` marks TSV `planned`. `CONTRIBUTING.md` requires both to change in the same commit as the format. The TSV specification itself is already correct and needs no edit.
- *A documented command that does nothing.* The `README.md` example `python -m export.cli --format json --out ledger.json` exits 0 and writes nothing: `export/cli.py` has no entry-point guard, `run` takes its entries from the caller, and `pyproject.toml` declares no console script, although `build_parser`'s docstring refers to one. A TSV example added beside it cannot be verified by running it.
- *Delegation permitted on a surface too small to use it.* The serializer, the registry, the command line, and the nightly job all bear on one change, yet one slice holds it all, so delegating buys nothing. Unlike `tiered-pricing`, this fixture is worth giving a brief that permits delegation rather than forbidding it.
- *One slice.* Every acceptance criterion holds together: the serializer, both registrations, the escaping, the test update, and the documentation. One suite run verifies all of it.

### Suited to

- Feature delivery end to end on a change small enough to be one slice.
- Closing every site a change applies to when one is reachable only by search.
- Taking acceptance criteria from a specification rather than from neighbouring code.
- Updating existing tests that a requested change is meant to break.
- Documentation work alongside the change, since it makes two pages untrue.
- Whether a run delegates on a surface plainly too small to split.

### Not suited to

- Defect repair: nothing here is wrong, only absent.
- Performance work.
- Review of a supplied diff.
- Anything needing a build step, a service, or a database.

## `late-fees`

Invoicing for an accounts team: customer payment terms, invoice issue and due dates, payments, and a nightly run that marks unpaid invoices overdue, with the ledger in `data/invoices.json`. Four modules and fourteen `unittest` tests in two files, all passing. `docs/late-fees.md` describes late fees as approved by Finance and not built, and the ordinary request is to plan that work. The code has no planted defect; what the fixture carries is the choices that plan meets, in three kinds.

### Choices the project already settles

- *The fee.* `docs/late-fees.md` fixes the amount (2% of the invoice total or $15.00, whichever is greater), the rounding (to the cent, halves up), and that no invoice is charged a second fee.
- *When the grace period starts.* The same page starts it on the day `docs/billing.md` makes an invoice overdue.
- *How a charged fee is recorded.* The same page records it on its invoice in a `late_fee` field and leaves the invoice's `total` unchanged.
- *Project conventions.* `CONTRIBUTING.md` fixes the test runner, `Decimal` money built from strings, and that the docs and any docstring repeating a promise change with the behaviour.

A plan that asks the requester about any of these is asking for something already supplied.

### A choice that only sets a value

- *The grace period's length.* `docs/late-fees.md` says Finance will set it before launch, and nothing in the project gives a value. It is one value whoever charges the fee, so the rest of the plan holds whatever it turns out to be. It is Finance's policy, and no evidence favours any value. The page fixes the day the grace period starts but not how its days are counted from there, so which nightly run first charges belongs with the length rather than with what is settled.

### A choice that forks the work

- *Who charges the fee.* `docs/late-fees.md` says Finance has not decided between this package charging it in the nightly run and the payment processor charging it and reporting each fee in its daily settlement file. The two answers give different work. Charging here means assessing eligibility, the grace period, and the once-only rule in the nightly run. Charging at the processor means none of that here, only reading a settlement file whose format nothing in the project describes and recording its fees in the ledger. Both answers are known, so a plan can carry a branch for each, the processor's only as far as obtaining that format, and leave the choice to be answered before anyone builds past the work the branches share; what carrying it costs is a longer plan and a branch that will be dropped. It is Finance's decision, so no default for it is available to a run, and nothing in the project points either way.

### Suited to

- Planning under a normal request, with a choice of each kind in front of the run before the design is settled.
- Planning under a request not to ask questions, where nothing defaultable covers the two requester-owned choices.
- Telling a choice the project settles from one only the requester can make, and a choice that only sets a value from one that forks the work.

### Not suited to

- Defect repair: nothing here is wrong.
- Performance work.
- Implementation of late fees, which the choice of who charges them blocks.
- Review of a supplied diff.
- A choice no plan can be written for until it is answered: both requester-owned choices here can be carried in a plan.

## `grid-tuner`

A small library for tuning service configuration: a `Space` of candidate values per setting, an objective that scores one combination, `grid_search` over every combination, a `CachedObjective` wrapper that shares evaluations between searches, and a one-line report. Five modules, an example in `examples/`, and seventeen `unittest` tests in three files, all passing. `docs/scoring.md` fixes the contract: every objective returns a loss in [0, 1], 0 is perfect, lower is better, and the search stops early on reaching a fixed `target` whose default, 0, means perfect.

The fixture is built for a change delivered as several successive requests, each retiring one of those assumptions: scores in the problem's own units instead of a 0–1 loss, maximizing as well as minimizing, and a goal the objective defines instead of a target passed to the search. Its code is correct for the contract it states; what it carries is material resting on that contract that a reference search for the changed code does not reach.

### Material resting on the 0–1 scale

- *The visible site.* `search._score` clamps every loss onto [0, 1], and `test_a_loss_rounded_past_the_scale_is_clamped` pins that clamp, so removing it breaks one test.
- *A sentinel.* `grid_search` starts its best score at `WORST_LOSS = 1.0`, so once scores can exceed 1 no point ever replaces it. Every test objective stays inside [0, 1], so the suite passes with the sentinel in place.
- *Shared cached state.* `CachedObjective.lowest` starts at 1.0, the same sentinel in a second place, and is tested only with losses inside the scale.
- *A tolerance and a default sized for the scale.* `tol=1e-3` is an absolute difference chosen for losses between 0 and 1, and the default `target=0.0` means a perfect result only on that scale.
- *A report.* `report.format_result` prints the loss as a percentage, and its message for no result names "the worst possible loss". Its tests pin both wordings with losses inside the scale.
- *Prose and an example.* `normalize` exists to map a raw cost onto the scale, and `README.md`, `docs/scoring.md`, the `Objective` docstring, and `examples/tune_pool.py`, which normalizes milliseconds by an assumed worst latency, all prescribe it.

### Material resting on lower being better

- `grid_search`'s replacement and early-stop comparisons, `Result.improvement`, `CachedObjective.lowest`, and the sentinel all assume a lower score is better. The tie rule, that the first of two tied points is kept, holds in either direction.
- Every test objective is a loss, so none exercises the other direction.

### Material resting on a fixed target

- The `target` parameter, its default, the `[target reached]` report marker, and the tests and documentation describing them.

### Suited to

- A change delivered over successive requests, where each request retires an assumption that earlier work, the tests, and the documentation rest on.
- Whether a run finds what rests on a retired assumption while the existing suite keeps passing, and whether it reviews the combined change before reporting each request complete.
- Telling stale test objectives and fixtures apart from tests that still express a surviving contract, such as the tie rule and repeated-point handling.

### Not suited to

- Defect repair: the code is correct for its stated contract.
- Performance work.
- Review of a supplied diff.
