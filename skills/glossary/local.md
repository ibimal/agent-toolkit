# Local additions to glossary

These rules come from this repo's workflow doc. They add to the upstream
instructions in SKILL.md, and they win where the two differ.

- **ADRs live in `docs/sdlc/adr/`.** Wherever SKILL.md or
  `ADR-FORMAT.md` says `docs/adr/`, use `docs/sdlc/adr/` instead.
- **The user confirms each entry.** What a project word means is the
  user's call. Draft the entry, show it, and write it to `GLOSSARY.md`
  when the user confirms it. Do this in the same exchange, not in a
  batch later.
- **When to write.** Write an entry the moment a term is settled: in a
  grilling, in a wayfinder ticket, in an architecture-health session, or
  when a design names a new concept.
- **Renames and redefinitions.** Change the glossary first, and move the
  old word to _Avoid_. Then hand the matching code changes to `/start`
  as a Feature S batch or a Refactor. If `/start` is not available, list
  the code changes for the user instead.
- **AFK runs only read the glossary.** In a run that nobody watches, do
  not write `GLOSSARY.md`. Log each term that needs settling in the run
  trail as proposed, and list it in the hand-back.
- **Words, not decisions.** The glossary says what a word means. An ADR
  says why a decision was made. An ADR stays a draft until the user
  approves it.
