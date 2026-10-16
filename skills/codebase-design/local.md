# Local additions to codebase-design

These rules come from this repo's workflow doc. They add to the upstream
instructions in SKILL.md, and they win where the two differ.

- **Design words stay out of the glossary.** `GLOSSARY.md` holds the
  project's own words. Module, seam, adapter and the other terms here are
  shared design vocabulary and live only in this skill.
- **When standards disagree,** the repo's own rules win (`CLAUDE.md`,
  `REVIEW.md`, ADRs), then this vocabulary, then general guidance such as
  Clean Code. Where "keep functions small" would produce shallow
  pass-through code, deep modules win.
