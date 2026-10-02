---
title: Write release notes
cues:
- the requester asks for release notes for a release
- the requester supplies a change list and asks what to tell users about it
- the requester asks for problems in existing release notes to be fixed
goal: Release notes that tell each reader what changed in the release and what, if anything, they must do about it.
knowledge:
- change-list
- breaking-change
- section-order
- entry-format
- writing-entries
- audience-register
- security-fixes
guides:
- house-style
handoffs:
- task: review
  applicability:
  - When the requester asked for problems in existing release notes to be fixed without naming them, and no review on this route has identified them
---

Work only from the supplied change list, and ask the requester for it when none
was supplied. When fixing problems in existing notes, whether the requester
named them or a review found them, change only the entries they concern and
keep the rest as written.

1. Sort each change-list item into its section. Lead with New features, since
   they are what most readers open release notes to find, and follow with the
   other sections.
2. Write the entries.
3. If the notes will go out on the company blog or otherwise under the
   organization's name, open the House style guide and apply it.
4. Before delivering, check every entry against the change list and remove any
   entry that traces to no item on it.
