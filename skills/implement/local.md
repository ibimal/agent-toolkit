# Local additions to implement

These rules come from this repo's workflow doc. They add to the upstream
instructions in SKILL.md, and they win where the two differ.

- **Per slice:** `tdd` at the seams in `plan.md`, verify the slice, commit on
  the change's branch. Never commit to `main`; merging is a gate.
- **Parallel worktrees** only once CI, deploy, `verify-app` and the
  destructive-command guard exist, and only for slices with no blocking edge
  between them.
- **Inside a playbook, stop after the last slice.** The playbook's next steps
  (`tidy`, `verify-app`, `review-change`) follow as their own steps. Run
  `review-change` yourself only when implement runs outside a playbook.
- **Names** in code and tests use the terms in `GLOSSARY.md`.
