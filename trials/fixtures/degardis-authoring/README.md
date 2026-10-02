# Trial fixtures for `degardis-authoring`

Each directory here gives a blind trial of `degardis-authoring` one reusable input: a small Degardis source to review, revise, or evaluate. The directory is the skill source itself, with `skill.yaml` at its top. Fixtures are grouped under the skill they trial rather than their subject, because each one is built around that skill's open questions and rarely fits another skill as well.

A fixture is deliberately not exemplary. Each contains defects the run is meant to find and decisions it is meant to make, because that is what the trial measures. Nothing here is a model of how to write a skill.

## What every fixture needs

A Degardis compiler that accepts source format 2. Nothing needs installing beyond it, and no network access is required.

## `release-notes`

A skill for writing and reviewing software release notes from a supplied change list: two tasks (`draft` and `review`) that hand off to each other, seven knowledge units, seventeen skill-level principles, two product facets (`library-releases` and `end-user-apps`), and two guides (`house-style` and `migration-section`). The principles are all fifteen canonical ones, carried unchanged, plus two local ones, `reader-impact` and `ticket-references`.

It validates under `--fail-on-warning` with no errors or warnings, so the compiler reports none of its defects: every one is found by reading the generated pages.

### Planted defects

#### Arrangements that need restructuring

- *A guide reachable only through another guide.* No task or facet lists `migration-section`. Its only owner is `house-style`, through an inline reference, and `house-style`'s applicability is publication under the organization's name, so notes that are not published that way never reach the migration guidance. `inspect --only guides` shows it as `-> guide:house-style`.
- *One unit read for two kinds of work.* `knowledge/breaking-change.md` defines a breaking change and then gives drafting instructions ("When drafting, ...") that also land on the review page.

#### Duplicate ownership

- *Prose restating a hand-off.* The last paragraph of `tasks/review.md` ("If the requester also wants the problems fixed, ...") repeats, in its own words, the first half of the condition on the hand-off to `draft`: that the requester asked for the fixes. It also says to switch "once the review is done", a timing the hand-off's condition does not carry, so the prose looks partly load-bearing.
- *Prose restating a guide's condition.* Step 3 of `tasks/draft.md` restates `house-style`'s applicability in drifted words ("on the company blog or otherwise under the organization's name") and names the guide by title.
- *Prose restating a nested guide's condition.* The inline reference in `guides/house-style.md` ("When the release contains breaking changes, also follow ...") restates the first applicability item of `migration-section`.

#### Misplaced ownership

- *Workflow in a facet.* The last paragraph of `facets/library-releases.md` is a completion gate ("notes without one are not finished") for an Upgrade section, which also makes the facet a second owner of what `migration-section` calls the Migration section.
- *A format rule filed as a principle.* `principles/ticket-references.md` is an entry-format convention, named in `skill.yaml` as a skill-level principle.
- *The wrong knowledge kind.* `knowledge/audience-register.md` is guidance declared `kind: fact`.

#### Contradictions

- *Section order.* Step 1 of `tasks/draft.md` says to lead with New features, while `knowledge/section-order.md` puts Breaking changes first. The `reader-impact` principle decides between them.
- *What counts as breaking.* `facets/library-releases.md` counts a change as breaking only when it removes or renames a public API, while `knowledge/breaking-change.md` decides by the change's effect on the reader.
- *Editing during review.* `tasks/review.md` says not to edit the draft, and its goal says the draft stays unchanged, but its next paragraph says to correct spelling and formatting slips in the draft directly.
- *Fixing against the trace check.* `tasks/draft.md` says that when fixing problems in existing notes, the agent changes only the entries they concern and keeps the rest as written, while step 4 removes, before any delivery, every entry that traces to no change-list item. When the requester names the problems and the notes also hold an untraceable entry they did not name, the two disagree, and nothing on the page scopes the numbered steps to fresh drafts.

#### Redundancy

- *Paraphrased applicability.* The two applicability items of `guides/migration-section.md` are one situation under the skill's own definition of a breaking change.
- *A near-copy knowledge unit.* `knowledge/writing-entries.md` restates `knowledge/entry-format.md`, and both land on the draft page. Their wording differs enough that `inspect --only quality` reports no near-duplicate.

### Sound material

Everything else is meant to survive a correct revision:

- the change-list concept
- the breaking-change definition itself
- the section order and its reasoning
- the entry-format rule
- the security-fixes guidance
- the `reader-impact` principle and the fifteen canonical principles
- the ticket-id convention, wherever it ends up
- the library facet's versioning and side-by-side-call content
- the `end-user-apps` facet
- the house-style rules
- the body of `migration-section`
- the hand-offs between `draft` and `review`
- the draft task's rule that a fix changes only the entries its problems concern, and its check that every entry traces to the change list

### Other conditions

The skill's own Markdown is hard-wrapped, while the canonical principle files keep the canonical sources' one line per paragraph. The compiler folds both, so a revision that keeps each file's style keeps its wrapping.

### Suited to

- A whole-source review, or a review followed by revision, from one ordinary request.
- Ownership, contradiction, and redundancy defects that validation does not report.
- Restructuring decided by generated reach.
- Facet removal and addition tests on a facet that holds workflow.

### Not suited to

- Compiler-integrity or validation-repair questions, since it has no findings.
- Creating a source.
- Packaging, scripts, or assets, since it ships none.
- Format migration.
- How the `release-notes` skill itself behaves, since there is no change list or draft to run it on.
