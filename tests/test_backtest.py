"""
Unit tests for the historical backtesting and knockout simulation engine.
"""

import math
import random
import unittest
from pathlib import Path

import scripts.backtest as bt
import scripts.fetch_and_compute as model


class BacktestTests(unittest.TestCase):
    def test_elo_delta_zero_sum(self):
        dh, da = bt.calculate_elo_delta(1800, 1600, 2, 1, variant="standard")
        self.assertAlmostEqual(dh + da, 0.0)

        dh_m, da_m = bt.calculate_elo_delta(1800, 1600, 5, 0, variant="goal_margin")
        self.assertAlmostEqual(dh_m + da_m, 0.0)

    def test_goal_margin_scaling_is_monotonic(self):
        # Home team winning 1-0 vs 3-0 vs 6-0
        dh_1, _ = bt.calculate_elo_delta(1700, 1700, 1, 0, variant="goal_margin")
        dh_3, _ = bt.calculate_elo_delta(1700, 1700, 3, 0, variant="goal_margin")
        dh_6, _ = bt.calculate_elo_delta(1700, 1700, 6, 0, variant="goal_margin")

        self.assertGreater(dh_3, dh_1)
        self.assertGreater(dh_6, dh_3)

        # Standard model must produce identical delta regardless of scoreline
        std_1, _ = bt.calculate_elo_delta(1700, 1700, 1, 0, variant="standard")
        std_6, _ = bt.calculate_elo_delta(1700, 1700, 6, 0, variant="standard")
        self.assertAlmostEqual(std_1, std_6)
        self.assertGreater(dh_6, std_6)

    def test_match_log_loss_and_brier_score_values(self):
        # Perfect prediction
        loss_perf = bt.match_log_loss(1.0, 0.0, 0.0, "H")
        brier_perf = bt.match_brier_score(1.0, 0.0, 0.0, "H")
        self.assertAlmostEqual(loss_perf, 0.0, places=5)
        self.assertAlmostEqual(brier_perf, 0.0, places=5)

        # Uniform prediction
        loss_unif = bt.match_log_loss(1/3, 1/3, 1/3, "H")
        brier_unif = bt.match_brier_score(1/3, 1/3, 1/3, "H")
        self.assertAlmostEqual(loss_unif, -math.log(1/3), places=4)
        self.assertAlmostEqual(brier_unif, 0.5 * ((2/3)**2 + (1/3)**2 + (1/3)**2), places=4)

        # Completely wrong prediction
        loss_wrong = bt.match_log_loss(0.0, 0.0, 1.0, "H")
        brier_wrong = bt.match_brier_score(0.0, 0.0, 1.0, "H")
        self.assertGreater(loss_wrong, 30.0)  # Clipped by eps
        self.assertAlmostEqual(brier_wrong, 1.0, places=5)

    def test_spearman_rho_extremes(self):
        self.assertAlmostEqual(bt.spearman_rho([1, 2, 3, 4], [1, 2, 3, 4]), 1.0)
        self.assertAlmostEqual(bt.spearman_rho([1, 2, 3, 4], [4, 3, 2, 1]), -1.0)

    def test_step_up_backtest_chronology_and_leak_free_execution(self):
        # Create minimal synthetic 2-matchday scenario
        seeds = [
            {"name": "Club A", "baseline_elo": 1600.0, "coefficient": 25.0},
            {"name": "Club B", "baseline_elo": 1500.0, "coefficient": 0.0},
            {"name": "Club C", "baseline_elo": 1500.0, "coefficient": 0.0},
            {"name": "Club D", "baseline_elo": 1400.0, "coefficient": 0.0},
        ]
        fixtures = [
            # MD 1
            {"match_id": 1, "matchday": 1, "home": "Club A", "away": "Club B", "home_score": 3, "away_score": 0, "result": "H"},
            {"match_id": 2, "matchday": 1, "home": "Club C", "away": "Club D", "home_score": 0, "away_score": 2, "result": "A"},
            # MD 2
            {"match_id": 3, "matchday": 2, "home": "Club A", "away": "Club D", "home_score": 1, "away_score": 1, "result": "D"},
            {"match_id": 4, "matchday": 2, "home": "Club B", "away": "Club C", "home_score": 2, "away_score": 1, "result": "H"},
        ]

        summary = bt.run_step_up_backtest(seeds, fixtures, variant="standard")
        self.assertEqual(summary["matches_evaluated"], 4)
        
        # Verify pre-match Elo on MD 1 is strictly baseline
        m1 = summary["match_details"][0]
        self.assertEqual(m1["elo_home_pre"], 1600.0)
        self.assertEqual(m1["elo_away_pre"], 1500.0)

        # Verify pre-match Elo on MD 2 reflected MD 1 update but NOT MD 2
        m3 = summary["match_details"][2]
        self.assertGreater(m3["elo_home_pre"], 1600.0)  # Club A won MD 1
        self.assertGreater(m3["elo_away_pre"], 1400.0)  # Club D won MD 1

    def test_knockout_simulation_conserves_probabilities(self):
        # 36 mock clubs with arbitrary rankings
        actual_standings = [
            {"rank": i, "name": f"Team {i}"} for i in range(1, 37)
        ]
        elo_ratings = {f"Team {i}": 1500 + (37 - i) * 10 for i in range(1, 37)}

        probs = bt.run_knockout_bracket_simulations(actual_standings, elo_ratings, sims=200, seed=123)
        self.assertEqual(len(probs), 36)

        # Sum of champions across all 36 teams must equal exactly 1.0
        total_champs = sum(p["prob_champion"] for p in probs.values())
        self.assertAlmostEqual(total_champs, 1.0, delta=0.01)

        # Sum of finalists must equal 2.0
        total_finalists = sum(p["prob_final"] for p in probs.values())
        self.assertAlmostEqual(total_finalists, 2.0, delta=0.01)

        # Top 8 seeds must have 100% R16 probability (bye)
        for i in range(1, 9):
            self.assertEqual(probs[f"Team {i}"]["prob_r16"], 1.0)


if __name__ == "__main__":
    unittest.main()
