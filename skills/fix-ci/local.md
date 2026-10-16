# Local additions to fix-ci

These rules come from this repo's workflow doc. They add to the upstream
instructions in SKILL.md, and they win where the two differ.

- **Fix causes, not checks.** Never disable, skip or delete a check, and
  never loosen its threshold, to get green. Loosening a control is the
  user's call.
- **Reproduce first.** Run the failing command locally before changing code,
  so the fix is checked before it is pushed.
- **Three attempts.** After three failed attempts, stop and report what you
  tried, the error each time, and your best hypothesis.
- **A wrong check** is reported to the user with evidence; do not edit it.
