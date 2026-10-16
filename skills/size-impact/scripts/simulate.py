#!/usr/bin/env python3
"""Monte Carlo sizing for size-impact. Standard library only.

Reads a JSON spec on stdin:
  drivers  name -> {"dist": normal|lognormal|uniform|fixed, "p10", "p90"
              (or "value" for fixed), optional "min" and "max" clips}
  formula  a Python expression over the driver names, written by the agent
  bar      optional threshold to clear
  samples  optional, default 20000
  seed     optional, default 1

Prints P10, P50 and P90 of the formula, the chance of clearing the bar, and
each driver's swing: the change in the median when that driver moves from
its P10 to its P90 while the others vary.
"""
import json
import math
import random
import statistics
import sys

Z90 = 1.2815515655446004  # the standard normal's 90th percentile


def sampler(spec, rng):
    dist = spec.get("dist", "normal")
    if dist == "fixed":
        value = float(spec["value"])
        return lambda: value
    p10, p90 = float(spec["p10"]), float(spec["p90"])
    if dist == "normal":
        mean, sd = (p10 + p90) / 2, (p90 - p10) / (2 * Z90)
        draw = lambda: rng.gauss(mean, sd)
    elif dist == "lognormal":
        if p10 <= 0:
            raise ValueError("lognormal needs p10 > 0")
        mu, sigma = (math.log(p10) + math.log(p90)) / 2, (math.log(p90) - math.log(p10)) / (2 * Z90)
        draw = lambda: rng.lognormvariate(mu, sigma)
    elif dist == "uniform":
        width = (p90 - p10) / 0.8
        low = p10 - 0.1 * width
        draw = lambda: rng.uniform(low, low + width)
    else:
        raise ValueError(f"unknown dist {dist!r}")
    lo, hi = spec.get("min", -math.inf), spec.get("max", math.inf)
    return lambda: min(max(draw(), lo), hi)


def evaluate(formula, values):
    return float(eval(formula, {"__builtins__": {}}, {**values, "math": math, "min": min, "max": max}))


def percentile(sorted_values, q):
    index = min(len(sorted_values) - 1, max(0, round(q * (len(sorted_values) - 1))))
    return sorted_values[index]


def run(spec):
    rng = random.Random(spec.get("seed", 1))
    n = int(spec.get("samples", 20000))
    samplers = {name: sampler(d, rng) for name, d in spec["drivers"].items()}
    formula = spec["formula"]
    results = sorted(evaluate(formula, {k: s() for k, s in samplers.items()}) for _ in range(n))
    out = {"p10": percentile(results, 0.1), "p50": percentile(results, 0.5), "p90": percentile(results, 0.9)}
    if "bar" in spec:
        out["chance_of_clearing_bar"] = sum(r >= spec["bar"] for r in results) / n
    swings = {}
    for name, d in spec["drivers"].items():
        if d.get("dist") == "fixed":
            continue
        medians = []
        for fixed in (d["p10"], d["p90"]):
            values = [evaluate(formula, {**{k: s() for k, s in samplers.items()}, name: fixed})
                      for _ in range(max(1000, n // 10))]
            medians.append(statistics.median(values))
        swings[name] = medians[1] - medians[0]
    out["swing_by_driver"] = dict(sorted(swings.items(), key=lambda kv: -abs(kv[1])))
    return out


if __name__ == "__main__":
    print(json.dumps(run(json.load(sys.stdin)), indent=2))
