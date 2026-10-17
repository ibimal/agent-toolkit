---
name: implement
description: "Implements a spec or plan slice by slice: tdd at the agreed seams, verify the slice, commit; independent slices run in parallel worktrees once the repo is agent-ready. Use when a playbook reaches implement or the user asks to build from a spec, plan or tickets."
license: MIT
---

Read [local.md](local.md) first. It holds this repo's additions to the
instructions below, and it wins where the two differ. The instructions
below are adapted from an upstream skill and changed in this repo;
`PROVENANCE` names its authors, source and licence, and lists every
change.

Implement the work described by the user in the spec or tickets.

If the user passes a ticket reference, fetch it from the issue tracker and state its title before starting. If the reference is ambiguous, ask.

Call the Skill tool with "tdd" where possible, at pre-agreed seams.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Once done, call the Skill tool with "review-change" to review the work.

Commit your work to the current branch.
