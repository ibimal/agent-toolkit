# Local additions to diagnose-bug

These rules come from this repo's workflow doc. They add to the upstream
instructions in SKILL.md, and they win where the two differ.

- **Same surface.** Reproduce where the user saw the problem: the same UI,
  API, job or notebook, before any lower-level test.
- **bugfix.md first.** Before the fix, write `bugfix.md` in the change folder
  with the current behaviour, the expected behaviour, and the behaviour that
  must not change.
- **Lock the regression test.** Once the failing regression test exists,
  add its path to `docs/sdlc/locks`, so the guard blocks edits to it while
  the fix is in progress. Remove the line once the fix is verified.
- **Other instances.** After the fix, search the codebase for the same cause
  elsewhere: the same pattern, the same misuse, the same wrong assumption.
  List each instance. Fix it in the same change when it is small; otherwise
  hand it to `/start` as its own Bug fix.
- **Inside an Incident,** stay read-only: find the cause and write it into
  the incident note. The fix goes through a Bug fix.
- **Lesson.** If the cause was one word used two ways, `codify` settles the
  word in the glossary.
