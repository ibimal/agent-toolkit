# Local additions to to-spec

These rules come from this repo's workflow doc. They add to the upstream
instructions in SKILL.md, and they win where the two differ.

- **Where it goes.** Write the spec to
  `docs/sdlc/changes/C-NNNN-<slug>/spec.md`, numbering the change folder after
  the highest existing one. When `docs/sdlc/config` links a tracker, mirror
  the spec to a ticket and record the ticket ID in the spec. When the config
  names the local tracker, the file is the only copy.
- **Read the intent with it.** Read the intent file in
  `docs/sdlc/intents/` before writing, and open the spec with the intent ID,
  the intent revision it was written against, and a one-line reference to the
  outcome. Never copy or redefine the outcome. If the intent changes after
  the spec is approved, the spec is stale and is grilled again.
- **Sections to add** to the template below: **Acceptance criteria** as
  Given/When/Then; **NFRs** (performance, reliability, security, privacy,
  cost) with a number where one exists; **Risks**; and **Which part of the
  intent this change delivers**, since one intent may span several changes.
- **Glossary.** Use the terms in `GLOSSARY.md`. A term that needs settling
  goes to the `grilling` that follows this step, where `glossary` records it.
- **Next step.** A grilling on the spec follows, then the spec gate.
