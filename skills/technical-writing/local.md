# Local additions to technical-writing

These rules come from this repo's workflow doc. They add to the upstream
instructions in SKILL.md, and they win where the two differ.

- **The user's style rules win.** When the always-on style rules ("Response
  style: technical plain English") are loaded, follow them; where a layer
  below disagrees, the style rules win, because they are the user's own.
- **Glossary.** Use the terms in `GLOSSARY.md`.
- **Analysis readouts** lead with the decision, then the number with its
  uncertainty, then what would change the conclusion.
- **Code snippets** follow the repo's indentation, not tabs by default.
- **Review mode.** When the user asks for a review instead of a rewrite:
  1. Read the whole text, identify the reader and the purpose, and judge
     terms and depth against that reader.
  2. Start with a one-line verdict: ready, needs small fixes, or needs
     restructuring.
  3. Report issues in order of impact: first anything that could mislead (an
     ambiguity, a missing condition, a contradiction, a wrong claim), then
     clarity, then concision.
  4. For each issue, quote the smallest span, name the rule, and give a
     rewrite. Report a repeated issue once, with its count and one example.
  5. Leave code, identifiers, commands, paths, configuration keys and program
     output unchanged.
  6. If nothing is worth changing, say so and stop.
- **Edits instead of a review.** When the user asks you to fix someone's
  text rather than review it, apply the fixes and list the changes briefly.
- **Finish with `unslop`** on what you wrote.
