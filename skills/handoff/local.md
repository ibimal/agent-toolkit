# Local additions to handoff

These rules come from this repo's workflow doc. They add to the upstream
instructions in SKILL.md, and they win where the two differ.

- **Where it goes.** On the same device, write it to the temp folder, as the
  instructions below say. When the user switches devices, write it to
  `handoff.md` in the change folder (`docs/sdlc/changes/C-NNNN-<slug>/`) and
  commit it on the change's branch, because the temp folder does not travel.
- **Resume point.** Name the playbook and the step it stopped at, so that
  `/start continue <change>` can resume at that step.
- **Lifetime.** A handoff in a change folder is deleted when the change
  merges; `ship` removes it.
- **Suggested skills** use the names in this skills repo, such as `grilling`,
  `to-spec`, `implement` or `review-change`.
