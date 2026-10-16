# Local additions to afk

These rules come from this repo's workflow doc. They add to the upstream
instructions in SKILL.md, and they win where the two differ.

The instructions below define the trail. This file adds how a run with
nobody watching behaves.

- **Readiness first.** Start only when CI, deploy, `verify-app` and the
  destructive-command guard exist. Otherwise report what is missing and
  stop, because nothing would catch the run's mistakes.
- **Hold every gate.** Never approve on the user's behalf. The gates are
  preference calls (a brief, an MVP cut, an intent, a spec, an architecture,
  a design and plan, an experiment's bar, a sizing's verdict) and
  irreversible or shared-state actions (merge to `main`, production deploy,
  migrations, data deletion, messages to people, and loosening any of the
  agent's own controls). A HITL wayfinder ticket is a gate too. At a gate,
  park that task and move to other unblocked work. When none is left, stop.
- **Defaults instead of questions.** For each ambiguous choice, pick the
  default and log it with its evidence, so review moves to the end instead of
  disappearing. What a word or a metric means is never a default: a term or
  definition that needs settling waits in the hand-back.
- **Glossary and data context.** Read `GLOSSARY.md`; do not change it. Log a
  term that needs settling as proposed. `data-context` still records facts as
  usual; a proposed metric definition waits in the hand-back.
- **Where the trail lives.** Write it to `.audit/<slug>.tsv` and commit it
  with the run's changes, because the user reviews the run from it.
- **Transcript audit.** Read only this run's transcript, wherever the current
  harness keeps it. Append any decision the log missed; never edit an earlier
  row.
- **Cross-family review.** Use `second-opinion` to have a model from another
  family flag rows whose evidence is missing. If no other family is
  reachable, use the strongest same-family model in a fresh context and say
  so in the hand-back.
- **Hand-back.** Top the trail with a hand-back that lists what finished,
  what waits at which gate, and which rows to check first.
- **Models and subagents.** Ignore the `pstack-models.mdc` rule, the default
  model slugs and the Task-tool flags in the instructions below; they belong
  to Cursor. Use the subagent mechanism of the current harness, read-only
  where the instructions say so. When `docs/sdlc/config` names models for
  this skill's roles, use them; otherwise use the harness default. Ignore
  references to the `poteto-mode` skill.
