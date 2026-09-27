---
name: plain-restate
description: Restate the previous response in plain technical English, with the same substance and roughly the same length. Use only when the user did not follow the response or asks to restate or re-explain it, for example "wait, what?", "I don't follow", or "say that more plainly". Not for shortening (use condense) or adding depth (use deepen).
metadata:
  inspired-by: https://github.com/mattpocock/skills/tree/main/skills/productivity/wait-what
---

# Plain restate

Restate your previous response for a technically capable reader who does
not know this system or domain. If the user points to the part they did
not follow, restate only that part.

1. Keep every fact, condition, caveat, and conclusion.
2. Replace jargon with ordinary words when they are equally precise. Keep
   exact technical terms, and keep the project's glossary terms if it has
   a glossary. Define a term briefly if the reader may not know it.
3. Add the small amount of context the reader needs to follow the point,
   such as what a component does or why a step is needed.
4. Keep code, commands, paths, and program output exactly as they are.
5. Follow the always-on style rules, titled "Response style: technical
   plain English".

Do not shorten for its own sake, and do not add new depth. Output only
the restated response, with no introduction.
