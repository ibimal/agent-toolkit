# Local additions to make-chart

These rules come from this repo's workflow doc. They add to the upstream
instructions in SKILL.md, and they win where the two differ.

- **Form follows the question:** change over time, comparison, distribution
  or relationship.
- **Honest axes.** Bars start at zero, and there are no dual axes.
- **Uncertainty is shown,** as intervals or bands, whenever the data has it.
- **Direct labels.** Label the data where it sits instead of in a legend,
  where the layout allows.
- **Colours** stay readable for colour-blind readers and in both light and
  dark themes.
- **The title states the chart's claim,** not just the metric.
- **Judging is separate.** This skill makes the chart; `review-result`
  judges whether the number behind it holds. Read `data-context` before
  querying the data for a chart.
