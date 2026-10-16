# Local additions to preregister

These rules come from this repo's workflow doc. They add to the upstream
instructions in SKILL.md, and they win where the two differ.

- **Read `data-context` before any query,** and write back what you learn
  about grain, keys, freshness and traps, with its source.
- **The plan holds,** in this order: the hypothesis and the decision it
  drives; the primary metric, as `data-context` defines it; the unit, design
  and randomisation; the sample size from the smallest effect worth acting
  on, with its power; the duration and stop rule; the analysis plan; and, for
  a paid model evaluation, its cost before anything runs.
- **Without randomisation** (an observational question such as "did the
  redesign raise retention?"), the plan also names the causal graph, how the
  effect will be identified (difference-in-differences, synthetic control,
  regression discontinuity or matching), and the checks that could prove it
  wrong, such as pre-trends and placebo outcomes.
- **The bar is the user's.** The smallest effect worth acting on, and the
  decision the result drives, are preference calls; ask for them.
- **Where it goes.** Save it as `preregistration.md` in the change folder,
  before the data is seen. `review-result` later checks the result against
  it.
