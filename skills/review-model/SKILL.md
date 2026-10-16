---
name: review-model
description: "Reviews a model before it is adopted, in the change that ships or replaces it: an evaluation split that matches real use, no leakage, baselines including the system it replaces, results per slice, calibration, a threshold set by error costs, training-serving parity, and a monitoring plan; the verdict goes in the PR body and model-review.md. Use whenever a change ships or replaces a model."
metadata:
  inspired-by: https://github.com/K-Dense-AI/claude-scientific-skills (shap, scientific-critical-thinking)
---

# Review model

Decide whether a model is fit to adopt. Read `data-context` before any
query, and write back what you learn. Every number in this review goes
through `review-result`.

## Checks

1. **Split.** The evaluation split matches how the model will be used: by
   time, and by entity (household, user, account), so that no entity appears
   on both sides.
2. **Leakage.** No feature carries information from after the prediction
   time or from the label itself.
3. **Baselines.** Compare with a simple baseline and with the system the
   model replaces, on the same split.
4. **Slices.** Report results per slice that matters to the product, not only
   the average. Name any slice where the model does worse than the baseline.
5. **Calibration.** Predicted probabilities match observed rates.
6. **Threshold.** Set it from what each kind of error costs, and state those
   costs.
7. **Training-serving parity.** Features are computed the same way in
   training and in serving; show the check.
8. **Monitoring.** The plan names the metrics, their alert thresholds, and
   who the alerts reach.

## Verdict

Adopt, adopt with limits (name them), or not yet (name what is missing).
Write the review to `model-review.md` in the change folder and the verdict
with its limits into the PR body. The verdict informs the merge gate; it
does not replace it.
