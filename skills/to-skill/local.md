# Local additions to to-skill

These rules come from this repo's workflow doc. They add to the upstream
instructions in SKILL.md, and they win where the two differ.

- **A check first.** Make a skill only when a lint, hook, test or command
  cannot do the job, because a check holds every time and a skill only
  guides.
- **Name.** A name that pairs an action with its object leads with the verb
  (`review-change`, `explore-data`). Knowledge the agent reads keeps a noun
  (`glossary`). `review-` judges something before it is accepted; `-health`
  reports on what exists; `to-` writes an artifact. Other names say what the
  user gets in plain words. Never reuse a name that a harness reserves, and
  never pick a name that promises the opposite of what the skill does.
- **Trigger.** A typed-only skill sets `disable-model-invocation: true` and
  costs no context until typed, so a narrow skill earns its place. An
  agent-startable skill's description loads in every session, so it must be
  used often or be run by a playbook or another skill.
- **Body.** Write it with `writing-for-agents`.
- **Evals.** Add eval cases in the repo's `evals/skills/<name>/`, not in an
  `evals/` folder inside the skill, so an installed skill carries no eval
  data.
- **Review.** Run `review-skill` before the skill is trusted. A new skill
  that overlaps one the user already has is merged into it or dropped.
- **Forks.** For a fork, change only `local.md`; the upstream body stays as
  it is. Record the change in `PROVENANCE`.
- **This repo.** Use spec frontmatter only, plus
  `disable-model-invocation: true` on a typed-only skill, and run
  `bin/toolkit check`.
