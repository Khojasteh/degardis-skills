# Blind Trial Material

The skills in this collection are checked by putting them to work. A fresh agent, told nothing about the skill's source or the expected result, receives a small self-contained project and an ordinary request. Its work can then be compared with the behavior the skill was written to guide. This directory holds the material for those blind trials; none of it ships in a published bundle.

- `fixtures/<skill-name>/` — the small projects a run receives, with one directory per fixture. Each collection has a `README.md` explaining what its fixtures contain and which questions they suit. Fixtures are deliberately not exemplary: several contain planted defects, and a few are meant to fail validation, because that is what the trial measures. Nothing here is a model of how to write a project.
- `pending/<skill-name>/` — questions a trial raised but could not settle, together with any material a later run will need. A question leaves the list once it is settled, so this is a view of what remains open rather than a history of every question. A skill with nothing pending has no directory there.
