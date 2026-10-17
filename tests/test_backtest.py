import json
from pathlib import Path
import sys
import types
import unittest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Offline stub for requests
if "requests" not in sys.modules:
    requests_stub = types.ModuleType("requests")
    requests_stub.RequestException = Exception
    requests_stub.get = lambda *args, **kwargs: None
    sys.modules["requests"] = requests_stub

import scripts.backtest as backtest
import scripts.fetch_and_compute as model


class BacktestTests(unittest.TestCase):
    def setUp(self):
        self.fixture_path = REPO_ROOT / "tests" / "fixtures" / "backtest_2026_md1_md2.json"
        self.assertTrue(self.fixture_path.exists(), f"Fixture file not found: {self.fixture_path}")
        with open(self.fixture_path, encoding="utf-8") as f:
            self.data = json.load(f)

    def test_fixture_integrity(self):
        matches = self.data.get("matches", [])
        self.assertEqual(len(matches), 36)
        self.assertEqual(self.data.get("season"), 2026)

        for fx in matches:
            self.assertIn(fx["actual"], ("home", "draw", "away"))
            self.assertIn(fx["matchday"], (1, 2))
            self.assertIsInstance(fx["elo_home"], (int, float))
            self.assertIsInstance(fx["elo_away"], (int, float))
            self.assertGreater(fx["elo_home"], 1000)
            self.assertGreater(fx["elo_away"], 1000)
            score = fx["score"].split("-")
            self.assertEqual(len(score), 2)
            gh, ga = int(score[0]), int(score[1])
            expected_actual = "home" if gh > ga else ("away" if gh < ga else "draw")
            self.assertEqual(fx["actual"], expected_actual)

    def test_backtest_beats_uniform_baseline(self):
        results = backtest.run(self.fixture_path)
        self.assertEqual(results["n_matches"], 36)

        model_brier = results["model"]["brier"]
        unif_brier = results["baseline_uniform"]["brier"]

        self.assertLess(model_brier, unif_brier, "Model Brier score must outperform uniform baseline")
        self.assertLess(model_brier, results["pre_market_value"]["brier"], "Calibrated model must outperform pre-MV baseline")
        self.assertLess(model_brier, 0.60, "Model Brier score should be under 0.60 on this test set")
        self.assertGreater(results["model"]["accuracy"], 0.60, "Model pick accuracy should exceed 60%")

    def test_outcome_probabilities_sum_to_one_and_preserve_expectation(self):
        for fx in self.data["matches"]:
            h, d, a = model.outcome_probabilities(fx["elo_home"], fx["elo_away"])
            total = h + d + a
            self.assertAlmostEqual(total, 1.0, places=6)
            self.assertGreaterEqual(h, 0.0)
            self.assertGreaterEqual(d, 0.0)
            self.assertGreaterEqual(a, 0.0)

            # Expected score preservation check
            e = model.elo_expected(fx["elo_home"], fx["elo_away"], home_bonus=model.HOME_ADVANTAGE)
            exp_from_probs = h + 0.5 * d
            self.assertAlmostEqual(exp_from_probs, e, places=12)

    def test_format_report_output(self):
        results = backtest.run(self.fixture_path)
        report = backtest.format_report(results)
        self.assertIn("CL TRACKER", report)
        self.assertIn("N = 36", report)
        self.assertIn("Current Model", report)
        self.assertIn("Calibration Check", report)


if __name__ == "__main__":
    unittest.main()
