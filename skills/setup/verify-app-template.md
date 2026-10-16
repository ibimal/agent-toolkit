# verify-app template

Write this as `.claude/skills/verify-app/SKILL.md` in the product repo, and
fill in the placeholders. It is project-local because only this repo knows
what "works end to end" means. Update it whenever a feature changes what the
app does.

```markdown
---
name: verify-app
description: "Proves this app or pipeline works end to end by running the real artifact and reporting the evidence. Use after implement and before review-change, after any change to what the app does, and as the first check of an agent-readiness run."
---

# Verify app

Run the real thing and report what happened. A claim without output is not
evidence.

1. Run: `<the one command that builds, starts and exercises the app>`
2. Check: <what the output must show for each capability, such as a page
   that loads, an API call that returns the expected body, or a job that
   writes the expected rows>.
3. Report the command, the relevant output and a pass or fail for each
   capability.

For data work, also: run the pipeline on the sample data in `<path>`, check
the schemas and data-quality tests, and check each metric against its
threshold on the fixed eval set in `<path>`.
```
