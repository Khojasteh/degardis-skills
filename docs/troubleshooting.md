# When a skill is skipped or the result looks wrong

This happens to everyone, and the cause is usually small. A skill isn't a command you run. It's guidance your agent loads when your request matches what the skill is for, or when you name the skill. A confident, polished answer doesn't prove the skill was involved, so check the host's skill list, the transcript, and what the agent actually did. Then work through the quickest causes first.

- **It never mentions the skill.** Check that it's installed where *this* agent looks by asking it to list the skills it can see. Locations differ per agent and per scope, and each agent's documentation lists its own; the [installation guide](installation.md#filesystem-based-agents) links to them. If the agent can't see the skill, no amount of rewording will help.
- **Another copy or another skill answered instead.** Two installed skills that cover the same work compete for your request: an older version installed in another scope, say, or a skill that a newer one replaces. Ask the agent which skill it loaded, its version, and where it loaded it from, then remove the copy you don't want — [upgrading an installed skill](installation.md#upgrade-an-installed-skill) covers skills a replacement supersedes.
- **The skill is visible but unavailable in this run.** Host modes, invocation controls, session state, account or workspace permissions, and workspace policy can all filter what an agent may load, so it is worth a look at the host's skill settings and picker. If you installed the skill after the session began and it has not appeared, starting a new session or restarting the host usually sorts it out.
- **It loads the skill but does not follow it.** This can look two ways: the agent says afterwards that the skill fitted but handled the work itself, or the transcript shows it loading the skill and then never returning to the instructions. Make the order explicit in your *next* request:

  ```text
  Before touching anything, load the [skill name] skill and follow its instructions.
  ```

  If it keeps happening, the section on [why an agent drifts from a skill it loaded](#why-an-agent-drifts-from-a-skill-it-loaded) has the things that actually help.
- **It followed something else instead.** Your own request, an instruction file in your workspace that your agent reads automatically, something your agent remembers from an earlier session, or the host's policy can each pull against a skill, and the agent may resolve that quietly, so the outcome changes with nothing in the transcript announcing why. See [when something outranks the skill](#when-something-outranks-the-skill).
- **Nothing matched, because the request was open-ended.** A skill routes on what you asked for, and "have a look at this" gives it nothing to match. Naming the outcome — diagnose, review, plan, upgrade, document — is usually enough on its own, and there's [more on phrasing a request](using-skills.md) if you want it.
- **It followed the skill, and the result is still wrong.** Then the skill itself may be at fault, which is worth knowing about — see [what can be wrong with a skill](#what-can-be-wrong-with-a-skill) below.

## Why an agent drifts from a skill it loaded

When the skill itself is not at fault, drift can be related to the agent's capability and reasoning setting. A skill asks the agent to handle several things at once: its instructions, the standards they carry, and your request. One configuration may follow the same skill more closely than another.

It is hard to spot, because nothing fails when an instruction is skipped: a run that weighed a rule and a run that never reached it can produce output that looks the same.

Things that help:

- **Raise the model or reasoning setting** for that run and compare. If a skill only holds together on your most capable configuration, that is worth reporting about the skill as well as your setup.
- **Start a fresh session** and load the skill first, so it is the most recent thing the agent read rather than something behind an hour of other work. A fresh session still brings along anything your agent remembers, so if a memory pulls against the skill, see [when something outranks the skill](#when-something-outranks-the-skill).
- **Ask for fewer outcomes at once.** Each one adds to what the agent has to hold.
- **Name the part you care about** — "before you write the report, re-read the skill's reporting rules" — which is cheaper than hoping it stayed in view.

## When something outranks the skill

A skill is never the only instruction in the room. Your request arrives with it. Many workspaces also have instruction files that the agent reads automatically, and the host adds policy of its own. A skill can behave differently in one workspace than another because of one of those instructions.

Memory is easy to forget. Some agents keep notes from earlier sessions, such as a preference you once stated or a lesson from a past task, and bring them into new sessions. A memory recorded for a different task can pull against a skill long after you've forgotten it exists.

Some of that is exactly as intended. These skills are [designed to put your instructions first](design-principles.md#your-instructions-come-first), so "findings only" or "keep it short" should win over a skill's own defaults. The problem is when the agent resolves a conflict without telling you. The outcome may then differ from what the skill's own page describes.

It tends to look like this:

- A workspace file says final checks are someone else's job, and a skill's verification step quietly becomes an unverified claim — you assumed a check ran that never did.
- A workspace file says to tidy and save every file the agent opens, so an analysis-only request comes back having changed files.
- A workspace file prescribes a house format for reports, and the skill's own report shape loses whichever parts did not fit.
- A memory from months ago says to keep every answer to three bullet points, so a skill's report drops the limits it was meant to state.
- You said "just fix it" to a skill whose job is to assess, so it either changes something you wanted described first, or spends the run explaining why it will not.
- The host forbids a command a step depends on, and the step degrades instead of stopping.

One question will often clarify what happened. Ask it in a fresh turn so the agent can answer directly:

```text
For [the step or decision], which instruction did you actually follow, and what else in this session, this workspace, or your memory told you something different?
```

Then decide the order yourself and state it in the request — "follow the skill's reporting rules even where the workspace file asks for our house format". If the conflict is permanent rather than specific to one run, narrow the workspace file instead. If a memory is the cause, review what your agent remembers, through its memory settings or by asking it, and remove or correct the entry. Fixing it at the source keeps the same conflict from coming back in the next session.

This is worth reporting when it happens. If a skill resolves a conflict without saying which way it went, you cannot supervise that decision; the skill needs improvement rather than another change to your setup.

## What can be wrong with a skill

A skill is written text, so it can be wrong in the ways written instructions are wrong. These are common problems, and how they appear in a transcript:

- **A gap** — your situation is one the skill does not cover, so the agent falls back on its own judgment without saying so. A skill that says "follow the workspace's style guide" meets a workspace with two style guides and no word on which wins, and quietly picks one.
- **An ambiguity** — the text can be read two ways, and different runs read it differently. "Keep the report short" alongside a requirement to list every finding forces the agent to break one of the two, and it will not always break the same one.
- **A routing mismatch** — the skill's description does not match how people actually ask, so the wrong requests select it or the right ones do not. You ask to "tidy up this report" and a skill that only reviews answers, when you wanted the report rewritten.
- **A rule the run never reaches** — the skill carries the rule, but nothing on the path your request took ever brings it into play. The protection you were counting on simply does not apply, and nothing looks wrong from outside.
- **A stale fact** — a flag, version, threshold, or command the skill asserts has changed since it was written, so a step fails, or worse, succeeds at something slightly different.
- **Too much for one run** — the instructions are right but there are more of them than the agent can carry, which is the drift described above rather than a mistake in any single sentence.

### Telling a skill defect from an agent slip

One question separates them: *would someone following the skill's own text have produced this result?*

Find the instruction that should have governed the moment things went wrong, and read it. There are three answers, and they point different ways:

- **The text says plainly what should have happened, and the run did otherwise.** Either the agent diverged, or something outranked it. Check your request, the workspace's instruction files, and anything your agent remembers before blaming the agent.
- **The text doesn't actually say**, or says two things, or says something that's no longer true. That's a gap, an ambiguity, or a stale fact, and the next run will hit it too.
- **The text says what happened, and what happened was wrong for your case.** The skill was followed faithfully into a situation its author didn't have in mind.

The second and third answers point at the skill itself, and both are worth reporting. You don't need to diagnose them precisely. Keep the transcript, then use the [problem-report prompt](feedback.md#ask-the-agent-to-draft-a-problem-report), which is built to separate what the transcript proves from what it only suggests.
