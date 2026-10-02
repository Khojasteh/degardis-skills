# Questions, reports, and defects

Questions and real-world experiences are always welcome, and you do not need to polish them before sharing. This guide helps you choose the right place and include the details that make a report easier to act on.

## Choose the right place

[Discussions](https://github.com/Khojasteh/degardis-skills/discussions) are the place for usage questions, field reports that still need digging into, what you have seen with a particular agent or model, and ideas for skills that do not exist yet.

Open an [issue](https://github.com/Khojasteh/degardis-skills/issues) when you have evidence of a reproducible defect in a skill, a documented claim that does not hold, or a routing boundary that keeps sending work to the wrong skill.

Not sure which one you have? Start with the [troubleshooting guide](troubleshooting.md). A skill your agent never loaded is a different problem from one it loaded and followed badly, and knowing which saves everyone a round trip.

## Field reports are genuinely useful

Your real-world experience can improve these skills in ways prepared examples cannot. When a skill helps, misses, or leaves something unclear, a field report supplies the context a prepared case may never reveal: an unusual workspace, a particular host, or an ambiguous request nobody anticipated.

A strong way to check a skill is a blind trial: a fresh agent receives a safe, representative task, and someone reviews the result. Those trials take time and usage, so field reports help focus them on the situations where they will do the most good.

If you would rather not write the report by hand, ask the agent that did the work:

```text
Give me your honest feedback on every skill you loaded in this session, including where one got in your way. Name each skill, and its version if you can see it, so I can set aside any that are not mine.

Your reader is another AI agent that has the skill's source but was not in this session and does not know what I asked you to do. Make each point stand on its own: name the skill and the step or instruction you mean, and say what you observed rather than what you concluded.

For each skill:

- The task you used it for: what I asked for, and what about the situation shaped how the skill applied — the kind of workspace, the tools and permissions you had, a request that turned out to be ambiguous. Enough that the reader can tell whether the skill was even meant for this, described generically.
- Defects and gaps you hit: what the instruction said, or failed to say, and what it cost you — a wrong turn, a retry, a judgment you had to make with nothing to go on.
- What you needed instead: the missing decision, the threshold you had to guess, or the wording that misled you. Do not design the fix.
- What worked and should not be lost: anything that kept you on track, or stopped you doing something you would otherwise have done.

Be terse and specific. Where a section has nothing, say "none" rather than filling it. Do not invent a problem, do not soften one, and do not report on a skill you only saw listed and never loaded.

Omit workspace-specific and sensitive details, including credentials, personal data, proprietary source, and internal paths.

Return the whole thing as one copyable block.
```

Read the draft before you share it. The agent is reporting on its own run, so treat the draft as a lead, not a verdict. Remove anything sensitive that slipped through.

Field reports go in [discussions](https://github.com/Khojasteh/degardis-skills/discussions). Include the details you can, say plainly what is confidential or unavailable, and keep the original evidence until a maintainer confirms that the report can be reproduced. Reports about runs that went *well* are welcome too — especially when they identify a boundary, host, model, or task shape that worked reliably.

## Ask the agent to draft a problem report

Use this after you have saved the original transcript. Treat what comes back as a lead rather than proof, and compare it with the transcript, skill files, commands, and artifacts it cites. Agents are not always right about their own runs.

```text
Investigate the completed run in this conversation to find where the skill fell short. Do not change files, rerun commands, or continue the original task.

1. Name the skill and its version, and say whether the transcript shows it was loaded. If it wasn't, stop there.
2. Find the first point where the result went wrong: what kind of thing was asked, what you did, and what you should have done instead.
3. Quote the skill instruction that governed that point, with its file and heading. If no instruction covered it, say so.
4. Give the most likely cause, marking what the transcript shows apart from what you infer: the instruction was missing, ambiguous, or wrong for this case; you didn't follow it; something outranked it — my request, an instruction file in the workspace, or the host; or a tool or permission it needed wasn't available.
5. Include your progress register as it stands, if the skill had you keep one.

Don't guess at what the transcript doesn't show. Describe my request and my workspace in general terms rather than quoting them. Replace anything that identifies them — names, paths, file contents, credentials, personal data — with [redacted] everywhere, the register included, and change nothing else in it. Return the report as one copyable block.
```

Please remove credentials, personal data, proprietary source, and internal paths before sharing the report.

A minimal reproducer helps a lot when you can share one safely. When you cannot, say what is confidential or unavailable and start a discussion anyway — a report with gaps in it is still much better than none.
