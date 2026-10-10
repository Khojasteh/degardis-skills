---
title: Observe or measure existing software
cues:
- a report of existing software's behavior or cost when run as it stands is asked
goal: The requested behavior or cost of existing software is stated as observed under the conditions that produced it, or reported as unobtained, from current evidence on the identified project state, with no project source changed.
knowledge:
- authorized-software-surface
- project-grounding
guides:
- user-interface-work
- performance-evidence
- performance-comparisons
- performance-cost-domains
- test-work
- dependency-and-artifact-integrity
- observability-and-diagnostics
- commands-and-tooling
- workspace-integrity
- version-control
handoffs:
- task: investigate-problem
  applicability:
  - When the run fails, the requester asked why it fails, and its cause is neither established nor pending on this route
- task: implement-change
  applicability:
  - When the run shows a failure of the subject, the requester authorized fixing it, the fix changes anything beyond project documentation, and it is neither made nor pending on this route
- task: document-software
  applicability:
  - When the run shows a failure of the subject, the requester authorized fixing it, the fix changes only project documentation, and it is neither made nor pending on this route
---

This task may run the software where authorized but does not repair or alter it. Fixing the subject or editing its configuration to obtain a different result would report on software other than the software asked about.

Identify what is to be run, its inputs and workload, the project revision, configuration, and environment before running.

Then run it. Classify a failure under [[principle:software-evidence]] before attributing it to the subject: an invalid harness, an unavailable dependency, or an environment fault is reported as what it is, and only a run whose harness, dependencies, and environment are sound shows the software's behavior.

Report the result at the width the evidence supports, with the revision, configuration, environment, and workload that produced it. The result reports the software's behavior or cost, not whether that is acceptable, so do not invent a threshold to turn it into a verdict. A result that could not be obtained names the unavailable evidence and the one run that would obtain it.
