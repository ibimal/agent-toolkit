# Local additions to tdd

These rules come from this repo's workflow doc. They add to the upstream
instructions in SKILL.md, and they win where the two differ.

- **Agreed seams** are the ones in `plan.md`. Confirm with the user only a
  seam the plan does not name.
- **Bug fixes.** The failing regression test comes first. While the fix is in
  progress, a hook blocks edits to it, so fix the code, not the test.
- **Data transformations** get fixture tests and property-based tests
  (shapes, schemas, invariants, distributions; Hypothesis for Python) rather
  than strict red-green.
- **Data pipelines** get schema and data-quality tests where data enters and
  leaves them (pandera, or dbt tests in a dbt project), so bad data fails
  loudly at the boundary.
- **Spikes and exploratory notebooks** are exempt; `review-result` re-runs
  them from a clean start instead.
- **Refactoring** belongs to the `tidy` step after implement.
