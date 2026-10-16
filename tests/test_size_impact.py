"""Tests for skills/size-impact/scripts/simulate.py."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

SIMULATE = Path(__file__).resolve().parent.parent / "skills" / "size-impact" / "scripts" / "simulate.py"


def simulate(spec):
    result = subprocess.run([sys.executable, str(SIMULATE)], input=json.dumps(spec),
                            capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


class SimulateTest(unittest.TestCase):
    def test_single_normal_driver_keeps_its_range(self):
        out = simulate({"drivers": {"x": {"dist": "normal", "p10": 10, "p90": 30}},
                        "formula": "x", "bar": 20})
        self.assertAlmostEqual(out["p10"], 10, delta=1)
        self.assertAlmostEqual(out["p50"], 20, delta=1)
        self.assertAlmostEqual(out["p90"], 30, delta=1)
        self.assertAlmostEqual(out["chance_of_clearing_bar"], 0.5, delta=0.03)

    def test_product_is_simulated_not_multiplied_at_the_ends(self):
        drivers = {"a": {"dist": "lognormal", "p10": 1, "p90": 4},
                   "b": {"dist": "lognormal", "p10": 1, "p90": 4}}
        out = simulate({"drivers": drivers, "formula": "a * b"})
        # Multiplying the two P90s gives 16; the simulated P90 must be lower.
        self.assertLess(out["p90"], 16)
        self.assertGreater(out["p10"], 1)
        self.assertEqual(set(out["swing_by_driver"]), {"a", "b"})


if __name__ == "__main__":
    unittest.main()
