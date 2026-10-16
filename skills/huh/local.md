# Local additions to huh

These rules come from this repo's workflow doc. They add to the upstream
instructions in SKILL.md, and they win where the two differ.

- **Plain technical English.** Use short, direct sentences and the terms in
  `GLOSSARY.md` (follow `GLOSSARY-MAP.md` when the repo has several). When
  the always-on style rules are loaded, follow them.
- **Explain; never re-decide.** Keep every caveat, add no claim the original
  did not make, and say so when the original was wrong.
- **With something after `/huh`** (`Q2`, a passage, a file or a link),
  explain just that.
- **With nothing after it,** explain what is waiting on the user. Check in
  this order and use the first that applies:
  1. A lot has happened since the user last wrote: give a catch-up, with
     what changed for them, then each decision waiting on them with a
     recommendation and what happens if they do not answer.
  2. The last reply asks one question: that question, with what is being
     decided, why it matters, what each answer leads to, and the
     recommendation.
  3. The last reply asks several: each in a plain line or two, numbered as
     asked, so the user can pick one with `/huh Q2`.
  4. The last reply asks nothing: the last reply in plain words. Keep
     every fact, condition, caveat and conclusion; only the wording gets
     plainer, so do not shorten for its own sake.
- **A catch-up is read-only.** Change nothing and start nothing. Check each
  number against the fact it comes from. Name things the way the user would
  know them.
- **Scope.** `/huh` covers this session since the user's last message;
  `/start` on its own covers all their work.
