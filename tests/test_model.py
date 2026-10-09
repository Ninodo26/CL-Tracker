import random
import sys
import types
import unittest
import warnings

# The model helpers are pure Python; stub the network client so these focused
# tests run even when the optional runtime dependency is not installed locally.
requests_stub = types.ModuleType("requests")
requests_stub.RequestException = Exception
requests_stub.get = lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("network disabled in unit tests"))
sys.modules.setdefault("requests", requests_stub)

import scripts.fetch_and_compute as model


class ModelTests(unittest.TestCase):
    def test_team_name_normalization_handles_accents_aliases_and_case(self):
        self.assertEqual(model.normalize_team_name("Bod\u00f8/Glimt"), "Bodo/Glimt")
        self.assertEqual(model.normalize_team_name("Paris Saint Germain"), "Paris Saint-Germain")
        self.assertEqual(model.normalize_team_name("BORUSSIA DORTMUND"), "Borussia Dortmund")
        self.assertEqual(model.normalize_team_name("FC Barcelona"), "Barcelona")
        self.assertEqual(model.normalize_team_name("FC Bayern M\u00fcnchen"), "Bayern Munich")
        self.assertEqual(model.normalize_team_name("SSC Napoli"), "Napoli")

    def test_form_normalization_reaches_coefficient_seed(self):
        baseline = model.seed_elo("Borussia Dortmund", {})
        adjusted = model.seed_elo("BORUSSIA DORTMUND", {"borussia dortmund": 50})
        self.assertEqual(adjusted - baseline, 50)

    def test_current_api_names_use_their_actual_coefficient_seed(self):
        api_names = {
            "Paris Saint-Germain FC": "Paris Saint-Germain",
            "FC Bayern München": "Bayern Munich",
            "FC Barcelona": "Barcelona",
            "Manchester United FC": "Manchester United",
            "Como 1907": "Como",
            "Sporting Clube de Portugal": "Sporting CP",
            "Manchester City FC": "Manchester City",
            "Aston Villa FC": "Aston Villa",
            "Borussia Dortmund": "Borussia Dortmund",
            "Real Betis Balompié": "Real Betis",
            "Racing Club de Lens": "Lens",
            "Real Madrid CF": "Real Madrid",
            "Liverpool FC": "Liverpool",
            "PAE AEK": "AEK Athens",
            "Arsenal FC": "Arsenal",
            "Fenerbahçe SK": "Fenerbahce",
            "AS Roma": "Roma",
            "PSV": "PSV Eindhoven",
            "FK Shakhtar Donetsk": "Shakhtar Donetsk",
            "Club Brugge KV": "Club Brugge",
            "Villarreal CF": "Villarreal",
            "Lille OSC": "Lille",
            "SK Slavia Praha": "Slavia Praha",
            "FC Internazionale Milano": "Inter",
            "Club Atlético de Madrid": "Atletico Madrid",
            "LASK Linz": "LASK",
            "SSC Napoli": "Napoli",
            "Viking FK": "Viking",
            "Galatasaray SK": "Galatasaray",
            "FC Porto": "Porto",
            "Feyenoord Rotterdam": "Feyenoord",
            "Sabah FK": "Sabah FK",
            "ŠK Slovan Bratislava": "Slovan Bratislava",
            "FK Bodø/Glimt": "Bodo/Glimt",
            "VfB Stuttgart": "VfB Stuttgart",
            "RB Leipzig": "RB Leipzig",
        }
        self.assertEqual(len(api_names), 36)
        for api_name, canonical in api_names.items():
            with self.subTest(api_name=api_name):
                self.assertEqual(model.normalize_team_name(api_name), canonical)
                self.assertIn(
                    canonical,
                    model.STARTING_COEFFICIENTS | model.QUALIFYING_COEFFICIENTS,
                )
                coefficient = model.coefficient_for_team(api_name)
                self.assertEqual(model.seed_elo(api_name, {}), model.ELO_BASE + coefficient * model.ELO_COEF_SCALE)

    def test_missing_coefficient_is_an_error_unless_explicit_fallback_is_requested(self):
        with self.assertRaisesRegex(model.MissingCoefficientError, "No UEFA coefficient configured"):
            model.seed_elo("Unknown Confirmed Club", {})
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            coefficient = model.coefficient_for_team("Unlisted Qualifier", allow_unlisted=True)
        self.assertEqual(coefficient, model.DEFAULT_COEFFICIENT)
        self.assertEqual(len(caught), 1)
        self.assertIn("explicit estimate", str(caught[0].message))

    def test_elo_update_is_zero_sum_and_expected_score_is_preserved(self):
        home, away = 1900.0, 1750.0
        expected = model.elo_expected(home, away, model.HOME_ADVANTAGE)
        ph, pd, pa = model.outcome_probabilities(home, away)
        self.assertAlmostEqual(ph + pd + pa, 1.0)
        self.assertAlmostEqual(ph + pd / 2, expected)
        result = 1.0
        change_home = model.ELO_K_FACTOR * (result - expected)
        change_away = model.ELO_K_FACTOR * ((1 - result) - (1 - expected))
        self.assertAlmostEqual(change_home + change_away, 0.0)

    def test_elo_update_is_applied_once_for_each_played_fixture(self):
        fixture = {
            "fixture": {"status": {"short": "FT"}, "date": "2026-09-08T12:00:00Z"},
            "league": {"round": "League Stage - 1"},
            "teams": {
                "home": {"id": 1, "name": "Borussia Dortmund"},
                "away": {"id": 2, "name": "FC Barcelona"},
            },
            "goals": {"home": 2, "away": 1},
        }
        teams = model.build_table([fixture], {})
        home_seed = model.seed_elo("Borussia Dortmund", {})
        away_seed = model.seed_elo("Barcelona", {})
        expected = model.elo_expected(home_seed, away_seed, model.HOME_ADVANTAGE)
        change = model.ELO_K_FACTOR * (1.0 - expected)
        self.assertAlmostEqual(teams[1]["elo"] - home_seed, change)
        self.assertAlmostEqual(teams[2]["elo"] - away_seed, -change)
        self.assertAlmostEqual(teams[1]["elo"] + teams[2]["elo"], home_seed + away_seed)

    def test_match_probabilities_are_valid_for_extreme_ratings(self):
        for home, away in [(1500, 1500), (3000, 500), (500, 3000)]:
            probabilities = model.outcome_probabilities(home, away)
            self.assertAlmostEqual(sum(probabilities), 1.0)
            self.assertTrue(all(0 <= p <= 1 for p in probabilities))

    def test_equal_ratings_have_symmetric_neutral_probabilities(self):
        home, draw, away = model.outcome_probabilities(1800, 1800, home_bonus=0)
        self.assertAlmostEqual(home, away)
        self.assertAlmostEqual(draw, model.BASE_DRAW_PROB + model.DRAW_CLOSENESS_BONUS)
        self.assertAlmostEqual(home + draw / 2, 0.5)

    def test_300_point_gap_preserves_elo_expected_score(self):
        expected = model.elo_expected(1800, 1500, home_bonus=0)
        home, draw, away = model.outcome_probabilities(1800, 1500, home_bonus=0)
        self.assertGreater(home, away)
        self.assertAlmostEqual(home + draw + away, 1.0)
        self.assertAlmostEqual(home + draw / 2, expected)
        self.assertGreater(home, 0.0)
        self.assertGreater(away, 0.0)
        self.assertGreater(expected, 0.8)
        self.assertLess(expected, 0.9)

    def test_stronger_home_ratings_raise_win_probability_and_reduce_loss_probability(self):
        results = [model.outcome_probabilities(rating, 1500, home_bonus=0)
                   for rating in (1500, 1600, 1800, 2100)]
        self.assertTrue(all(a[0] < b[0] for a, b in zip(results, results[1:])))
        self.assertTrue(all(a[2] > b[2] for a, b in zip(results, results[1:])))

    def test_home_advantage_and_reversed_home_away_are_consistent(self):
        neutral = model.outcome_probabilities(1800, 1500, home_bonus=0)
        home_advantage = model.outcome_probabilities(1800, 1500, home_bonus=model.HOME_ADVANTAGE)
        reversed_home = model.outcome_probabilities(1500, 1800, home_bonus=model.HOME_ADVANTAGE)
        self.assertGreater(home_advantage[0], neutral[0])
        self.assertGreater(home_advantage[0], reversed_home[2])
        self.assertAlmostEqual(sum(reversed_home), 1.0)
        self.assertAlmostEqual(home_advantage[0] + home_advantage[1] / 2,
                               model.elo_expected(1800, 1500, model.HOME_ADVANTAGE))
        self.assertAlmostEqual(reversed_home[0] + reversed_home[1] / 2,
                               model.elo_expected(1500, 1800, model.HOME_ADVANTAGE))

    def test_tiebreak_probability_is_bounded_and_zero_sims_rejected(self):
        self.assertEqual(model.elo_tiebreak_probability(3000, 500), 1.0)
        self.assertEqual(model.elo_tiebreak_probability(500, 3000), 0.0)
        with self.assertRaisesRegex(ValueError, "positive integer"):
            model.simulate_two_legged_tie("Real Madrid", "Barcelona", sims=0)
        with self.assertRaisesRegex(ValueError, "positive integer"):
            model.simulate_remaining_leg("Real Madrid", "Barcelona", 0, sims=0)

    def test_qualifying_tie_simulations_handle_extreme_aggregate_edges(self):
        random.seed(23)
        simulated_tie = model.simulate_two_legged_tie("Real Madrid", "Barcelona", sims=100)
        self.assertGreaterEqual(simulated_tie, 0.0)
        self.assertLessEqual(simulated_tie, 1.0)
        self.assertEqual(model.simulate_remaining_leg("Real Madrid", "Barcelona", 100, sims=10), 1.0)
        self.assertEqual(model.simulate_remaining_leg("Real Madrid", "Barcelona", -100, sims=10), 0.0)

    def test_neutral_venue_probabilities_do_not_apply_home_advantage(self):
        ph, pd, pa = model.outcome_probabilities(1800, 1800, home_bonus=0)
        self.assertAlmostEqual(ph, pa)
        self.assertAlmostEqual(ph + pd / 2, 0.5)

    def test_partial_schedule_is_rejected(self):
        teams = {1: {"id": 1, "name": "Borussia Dortmund"}}
        self.assertFalse(model.league_phase_schedule_is_complete([], teams))
        with self.assertRaises(ValueError):
            model.run_monte_carlo(teams, [])

    def test_complete_synthetic_schedule_and_monte_carlo_conservation(self):
        teams = {}
        fixtures = []
        for tid in range(36):
            teams[tid] = {"id": tid, "name": f"Club {tid}", "played": 0,
                          "points": 0, "gf": 0, "ga": 0, "elo": 1500}
        # Ring schedule: each club has four forward and four backward neighbors.
        counts = [0] * 36
        for i in range(36):
            for d in range(1, 5):
                j = (i + d) % 36
                fixtures.append({"teams": {"home": {"id": i}, "away": {"id": j}}})
        # The wraparound condition yields exactly 144 unique pairs and degree 8.
        for fx in fixtures:
            counts[fx["teams"]["home"]["id"]] += 1
            counts[fx["teams"]["away"]["id"]] += 1
        self.assertEqual(len(fixtures), 144)
        self.assertEqual(set(counts), {8})
        self.assertTrue(model.league_phase_schedule_is_complete(fixtures, teams))
        malformed = [dict(fx) for fx in fixtures]
        malformed[0] = {"teams": {"home": {"id": 1}, "away": {"id": 0}}}
        self.assertFalse(model.league_phase_schedule_is_complete(malformed, teams))

        original_sims = model.MONTE_CARLO_SIMULATIONS
        try:
            model.MONTE_CARLO_SIMULATIONS = 50
            random.seed(17)
            model.run_monte_carlo(teams, [{"home_id": f["teams"]["home"]["id"], "away_id": f["teams"]["away"]["id"]} for f in fixtures])
        finally:
            model.MONTE_CARLO_SIMULATIONS = original_sims
        self.assertAlmostEqual(sum(t["prob_top8"] for t in teams.values()), 8.0, delta=0.02)
        self.assertAlmostEqual(sum(t["prob_top24"] for t in teams.values()), 24.0, delta=0.02)
        self.assertTrue(all(0 <= t["prob_top8"] <= t["prob_top24"] <= 1 for t in teams.values()))

    def test_monte_carlo_handles_a_fully_tied_table_without_fixtures(self):
        teams = {
            tid: {"id": tid, "name": f"Club {tid}", "played": 8,
                  "points": 12, "gf": 10, "ga": 10, "elo": 1500}
            for tid in range(36)
        }
        original_sims = model.MONTE_CARLO_SIMULATIONS
        try:
            model.MONTE_CARLO_SIMULATIONS = 5
            model.run_monte_carlo(teams, [])
        finally:
            model.MONTE_CARLO_SIMULATIONS = original_sims
        self.assertTrue(all(0 <= t["prob_top8"] <= 1 for t in teams.values()))
        self.assertTrue(all(0 <= t["prob_top24"] <= 1 for t in teams.values()))
        self.assertAlmostEqual(sum(t["prob_top8"] for t in teams.values()), 8.0)
        self.assertAlmostEqual(sum(t["prob_top24"] for t in teams.values()), 24.0)


if __name__ == "__main__":
    unittest.main()

