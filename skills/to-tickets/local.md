# Local additions to to-tickets

These rules come from this repo's workflow doc. They add to the upstream
instructions in SKILL.md, and they win where the two differ.

- **Where it goes.** Write the plan to `plan.md` in the change folder. It
  holds the slices in order, their blocking edges, the TDD seam for each
  slice, risks, and the options rejected with the reason. When
  `docs/sdlc/config` links a tracker, also publish one ticket per slice. When
  the config names the local tracker, the file is the only copy.
- **Seams.** Name the seams `tdd` will test at. `implement` and `tdd` treat
  them as agreed.
- **When the user approves.** On Feature M the plan is a report, not a gate:
  present it and continue. On Feature L, `review-plan` and the design-and-plan
  gate follow, so iterate with the user as the instructions below say.
- **Refactor.** Slices are behaviour-preserving steps: migrate the callers,
  then delete the old API. The expand-contract sequence below fits.
