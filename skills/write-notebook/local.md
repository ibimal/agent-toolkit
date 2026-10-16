# Local additions to write-notebook

These rules come from this repo's workflow doc. They add to the upstream
instructions in SKILL.md, and they win where the two differ.

- **Why marimo.** A plain `.py` notebook diffs cleanly in a PR, stores no
  outputs (so no personal data is committed), and runs top to bottom as a
  script, so `review-result` can re-run it from a clean start.
- **Jupyter notebooks.** The first time a `.ipynb` file is touched, convert it
  with `marimo convert`, check the result runs as a script, and replace the
  original in the same change.
- **Read `data-context` before any query,** and write back what you learn
  about grain, keys, freshness and traps, with its source.
