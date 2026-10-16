# Local additions to writing-for-agents

These rules come from this repo's workflow doc. They add to the upstream
instructions in SKILL.md, and they win where the two differ.

These rules come from Anthropic's skill-authoring guide and its prompting
guidance for current Claude models. They add to the instructions below.

- **Description.** Write it in the third person ("Explains...", not "I
  explain..." or "You can..."). Say what the skill does and when to use it,
  with the key terms first, because harnesses may shorten long descriptions.
  Trigger text may carry calibrated urgency; body text explains instead of
  shouting.
- **Only what the model cannot know.** The model is already capable. Keep
  context only the author has: the audience, the environment, the quality
  bar, and the reason behind each constraint. Cut restatements of default
  behaviour.
- **Normal volume.** Write each rule plainly, with its reason. Capitalised
  MUST, NEVER or CRITICAL, and stacks of prohibitions, cause over-triggering
  and rigid behaviour on current models. State the target behaviour as a
  positive statement, and keep a prohibition only for a failure that really
  happens.
- **Goals over choreography.** For judgement tasks, state the outcome, the
  constraints and how to verify. Keep numbered steps where order truly
  matters, and exact commands only for fragile operations.
- **No thinking scaffolds.** Do not write "think step by step" or ask for
  reasoning in the output; the model thinks on its own, and its depth is set
  by effort, not prose.
- **Structure.** Keep SKILL.md under 500 lines. Keep references one level
  deep, and give a reference file over 100 lines a table of contents. Put the
  most important instructions near the top, because after compaction a
  harness may keep only the start of a skill.
- **Must-hold rules belong in hooks or checks.** Prose guides; a hook or CI
  check enforces.
- **No time-sensitive text and no history.** State the current rule. Leave
  out dates, incident stories and "now works differently" phrasing.
- **One term per concept,** matching the project's glossary.
- **Evaluate.** Write at least three test scenarios before polishing a skill,
  and check that a fresh session with the skill handles them.
- **This repo's own rules** also apply: spec frontmatter only (plus
  `disable-model-invocation: true` on a typed-only skill), actions instead of
  harness tool names, and `bin/toolkit check` before each commit.
