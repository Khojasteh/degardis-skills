---
kind: concept
title: Breaking change
---

A breaking change is any change that requires a reader to change their code,
configuration, or data for what worked before to keep working. The effect
decides it, not the change-list label: an unlabeled change in behavior can be
breaking, and a change labeled `breaking` that asks nothing of the reader is
not.

When drafting, put each breaking change in the Breaking changes section, bold
its first words, and follow it with the action the reader must take to upgrade.
