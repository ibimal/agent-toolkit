# Local additions to prototype

These rules come from this repo's workflow doc. They add to the upstream
instructions in SKILL.md, and they win where the two differ.

- **Data questions** get a throwaway marimo notebook written through
  `write-notebook`, instead of the two branches below.
- **Where the verdict goes.** In a Spike, record the question and verdict in
  `findings.md` in the change folder. For a wayfinder ticket, record it on
  the ticket. Where the instructions below say "implementation issue", use
  the change folder.
- **Nothing ships.** A prototype never merges to `main`; only the validated
  decision does.
