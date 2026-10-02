# Get good results

An installed skill gives your agent a better way to work, but your request still decides what that work is aimed at. A few simple habits go a long way, and you don't need a formal brief.

## Start with the outcome, not a skill name

Start with what you want to end up with, and let the agent choose the skills that fit. A task can need more than one. Name a particular skill when you want to steer that choice, or when one you expected didn't get used; the [troubleshooting guide](troubleshooting.md) covers that case.

## Give the agent what it needs to judge its own work

You don't have to supply all of this every time. Include what matters for the task; each useful detail gives the agent less to guess:

1. **Name the outcome.** Do you want an analysis, a plan, a change, or a review of work that's already done?
2. **Share the context that matters:** what you've noticed, the material involved, what must stay as it is, what you've already tried, and sources or dates for anything that changes quickly.
3. **Say where the boundary is.** What may the agent read or change, what may it run, and which destructive, external, privileged, or paid actions should it check with you first?
4. **Describe what done looks like** in terms you can observe: what you'll be able to see or check, and what the final report should show you.

A compact request can carry all four without becoming a document:

```text
[The outcome you want] for [the material it covers].

Context: [what you've noticed, what you've already tried, and where to find the details]
Keep: [what must stay as it is, and what's out of scope]
You may: [read, change, or run these]
Ask before: [anything destructive, external, privileged, or paid]
Done means: [what you'll be able to see or check when it's finished]
```

Each skill's page includes example requests for the work it handles. If you're unsure how much detail to give, pick the closest example and adapt it.

## Look over the result

When the agent reports back, read what changed and what it did, and check what matters to you yourself. Push back on any conclusion that feels broader than the evidence behind it. The skills are [designed to tell you](design-principles.md) what they checked and what they couldn't, so that account is a good place to start.

## Choose model capability and reasoning by evidence

Most agents let you pick a model, and many let you set how much it reasons before it answers. More reasoning can help with complex, multi-step, or long-running work, but it takes more time and usage. Less is faster and cheaper, and can be enough for simple, routine work.

- **Start from the default.** Adjust from there instead of starting at the maximum.
- **Judge on your own work.** How much a higher setting helps depends on the task, so general advice only tells you where to start. Try the same kind of request at two settings and compare the results.
- **Raise it when the work is hard or the skill slips.** Complex, multi-step work is where a higher setting is most likely to help. If an agent keeps [drifting from a skill it loaded](troubleshooting.md#why-an-agent-drifts-from-a-skill-it-loaded), a more capable model or a higher setting is a good first thing to try.
- **Lower it for routine work** once you've seen the results hold at the lower setting.

## Where to next

- [What the skills are designed to do](design-principles.md): what these skills aim for, and what still depends on your run.
- [When a skill is skipped or the result looks wrong](troubleshooting.md): when a skill isn't used, or the result surprises you.
