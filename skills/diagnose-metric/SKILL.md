---
name: diagnose-metric
description: "Finds why a metric moved by ruling out the data before the world: data faults first, then a mix-versus-rate decomposition, segments and calendar effects, then ranked hypotheses each tested against data; ends with the drivers and each one's share of the move, checked by review-result. Use when a number dropped or jumped, inside an Incident for metric drift, or when a measured success metric misses or moves unexpectedly. Not for code that misbehaves (use diagnose-bug)."
metadata:
  inspired-by: https://github.com/anthropics/knowledge-work-plugins (analyze, variance-analysis, metrics-review)
---

# Diagnose metric

Explain a move in a metric. Read `data-context` before any query: it holds
the metric's definition, the tables, and the known traps. Write back any new
fact or trap you find, with its source.

## Steps, in order

1. **Rule out the data.** Check pipeline runs, late or missing rows,
   duplicates, and changes to logging or to the metric's definition in
   `data-context`. A data fault ends the diagnosis: it goes to `/start` as a
   Bug fix, and the trap goes into `data-context`.
2. **Decompose.** Split the move into mix versus rate first (did the
   population change, or the behaviour within it?), then by segment, then by
   calendar effects (month length, holidays, seasonality, day-of-week).
3. **Hypothesise.** Rank the possible causes, and test each one against
   data. A hypothesis no query can test is labelled untested, not dropped.
4. **Check.** Run `review-result` on the conclusion.

## Readout

Lead with the conclusion, then the drivers, each with its share of the move
and its uncertainty, then what would change the conclusion. Send the readout
where the question came from: the incident note for an alert, a dated note
on the intent whose metric moved, or the conversation when the user asked.
A code fault goes to `/start` as a Bug fix.

This skill explains a number. `diagnose-bug` explains code that
misbehaves, and `why` traces how code came to be.
