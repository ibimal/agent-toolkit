# Local additions to tidy

These rules come from this repo's workflow doc. They add to the upstream
instructions in SKILL.md, and they win where the two differ.

- **Standards.** `REVIEW.md` is the first project standard: the same file
  that `review-change` and `code-health` use, so new code and old code are
  judged alike. Names follow `GLOSSARY.md`.
- **Inside a playbook,** run in pipeline mode on the change's diff.
- **Regression tests are proof tests.** During a bug fix, never touch the
  test named as the regression test.
- **Subtract first.** Prefer deleting code over adding it.
