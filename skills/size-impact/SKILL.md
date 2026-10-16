---
name: size-impact
description: "Sizes a decision's impact as a range before anything is built: the user's bar, drivers each estimated with a sourced range, a simulation to P10, P50 and P90 and the chance of clearing the bar, the driver worth measuring first, and a go, no-go or measure-first verdict; later records actuals and reports its own calibration. Use at milestone planning, when intents compete for a cut, or when an idea's value is unclear."
metadata:
  inspired-by: https://github.com/K-Dense-AI/claude-scientific-skills (what-if-oracle), How to Measure Anything (Douglas Hubbard)
---

# Size impact

Give a range, never a point. Read `data-context` before any query.

## Steps

1. **Frame.** The decision, the metric, the horizon, and the bar: the
   smallest impact that justifies the cost. The bar is the user's; ask for
   it.
2. **Drivers.** Break the impact into drivers that can each be estimated,
   and write the formula that combines them.
3. **Ranges.** Give each driver a P10 and a P90. Source them from data
   through `data-context` first, then from a comparable past launch, then
   from judgement labelled as such.
4. **Simulate.** Combine the ranges by simulation, never by multiplying lows
   and highs. Run `scripts/simulate.py` with a JSON spec on stdin:
   ```json
   {"drivers": {"households": {"p10": 2000, "p90": 6000, "dist": "lognormal"},
                "uptake": {"p10": 0.05, "p90": 0.2, "dist": "normal", "min": 0, "max": 1}},
    "formula": "households * uptake", "bar": 400}
   ```
   `dist` is `normal`, `lognormal`, `uniform` or `fixed` (with `value`). The
   script prints P10, P50 and P90, the chance of clearing the bar, and each
   driver's swing.
5. **Measure first.** Name the driver that moves the answer most, and
   whether it can be measured cheaply before building: a query, a fake door,
   a `to-questionnaire` survey, or a thin slice.
6. **Verdict.** Go, no-go, or measure first. `review-result` checks the
   arithmetic.

## Record

Save the sizing to `docs/sdlc/sizing/<slug>.md`: the frame, the drivers with
their sources, the formula, the simulation output, the driver to measure
first, and the verdict. An intent that follows links to it.

## Calibration

After release, the measure step writes each measured driver's actual beside
its range. About 8 in 10 actuals should land inside P10 to P90. When asked
to size, first report the hit rate across past sizings, and widen new ranges
if the actuals have run outside them.
