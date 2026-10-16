# Local additions to wayfinder

These rules come from this repo's workflow doc. They add to the upstream
instructions in SKILL.md, and they win where the two differ.

- **Tracker.** `docs/sdlc/config` names the tracker. With the local tracker,
  the map is `.scratch/<effort>/map.md` and each ticket is
  `.scratch/<effort>/issues/NN-<slug>.md`.
- **Destination.** The map usually serves a paused playbook. Its destination
  is that playbook's next writer, normally `to-spec` or `to-design`. When
  nothing is left to decide, hand back to `/start continue <change>`.
- **Research tickets** are resolved by the `research` skill, which writes its
  note into the ticket or `docs/research/`. Do not create throwaway research
  branches.
- **Settled terms** go to `GLOSSARY.md` through the `glossary` skill the
  moment a ticket settles them, and decisions that are hard to reverse become
  ADRs in `docs/sdlc/adr/`.
- **Runs that nobody watches.** In an AFK run, a HITL ticket is a gate: the
  `afk` skill parks it for the hand-back and moves to other unblocked work.
