"""
CL Tracker — Historical Backtesting & Knockout Prediction Engine
Evaluates CL Tracker model variants against ground truth historical seasons,
compares against expert benchmarks (Opta Supercomputer), and simulates the
full knockout stage bracket.
"""

import json
import math
import random
import sys
from collections import defaultdict
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import scripts.fetch_and_compute as model

HISTORICAL_DIR = PROJECT_ROOT / "data" / "historical" / "2024_25"


# ---------------------------------------------------------------------------
# Elo Variants & Scoring Helpers
# ---------------------------------------------------------------------------

def calculate_elo_delta(elo_home, elo_away, h_score, a_score, variant="standard"):
    """
    Computes Elo adjustment for home and away teams.
    variant:
      'standard': fixed K-factor (model.ELO_K_FACTOR = 22)
      'goal_margin': K-factor scaled by margin of victory: K * (1 + ln(margin + 1) / 2)
    """
    expected_home = model.elo_expected(elo_home, elo_away, home_bonus=model.HOME_ADVANTAGE)
    
    if h_score > a_score:
        result_h = 1.0
        margin = h_score - a_score
    elif h_score < a_score:
        result_h = 0.0
        margin = a_score - h_score
    else:
        result_h = 0.5
        margin = 0

    if variant == "goal_margin" and margin > 0:
        multiplier = 1.0 + math.log(margin + 1) / 2.0
    else:
        multiplier = 1.0

    k = model.ELO_K_FACTOR * multiplier
    delta_home = k * (result_h - expected_home)
    delta_away = -delta_home  # strictly zero-sum
    return delta_home, delta_away


def match_log_loss(p_home, p_draw, p_away, result, eps=1e-15):
    """Multi-class log loss for a single match."""
    p_h = max(eps, min(1.0 - eps, p_home))
    p_d = max(eps, min(1.0 - eps, p_draw))
    p_a = max(eps, min(1.0 - eps, p_away))
    
    if result == "H":
        return -math.log(p_h)
    elif result == "D":
        return -math.log(p_d)
    else:
        return -math.log(p_a)


def match_brier_score(p_home, p_draw, p_away, result):
    """
    Multi-class Brier score for a single 3-way match:
    BS = 0.5 * ((p_h - y_h)^2 + (p_d - y_d)^2 + (p_a - y_a)^2)
    Ranges from 0.0 (perfect) to 1.0 (completely wrong).
    """
    y_h = 1.0 if result == "H" else 0.0
    y_d = 1.0 if result == "D" else 0.0
    y_a = 1.0 if result == "A" else 0.0
    return 0.5 * ((p_home - y_h) ** 2 + (p_draw - y_d) ** 2 + (p_away - y_a) ** 2)


def spearman_rho(ranks1, ranks2):
    """Computes Spearman's rank correlation coefficient."""
    n = len(ranks1)
    if n != len(ranks2) or n == 0:
        return 0.0
    d_sq = sum((r1 - r2) ** 2 for r1, r2 in zip(ranks1, ranks2))
    return 1.0 - (6.0 * d_sq) / (n * (n * n - 1))


# ---------------------------------------------------------------------------
# Pre-Season Monte Carlo Simulator (Macro League Phase)
# ---------------------------------------------------------------------------

def run_preseason_monte_carlo(seeds, fixtures, sims=20000, seed=42):
    """
    Simulates the entire 144-match league phase from pre-season starting state.
    """
    random.seed(seed)
    team_names = [s["name"] for s in seeds]
    elo_by_team = {s["name"]: s["baseline_elo"] for s in seeds}

    top8_counts = {t: 0 for t in team_names}
    top24_counts = {t: 0 for t in team_names}
    points_accum = {t: 0 for t in team_names}
    rank_accum = {t: [] for t in team_names}

    # Pre-calculate match outcome probabilities so simulation loop is fast
    match_probs = []
    for fx in fixtures:
        h, a = fx["home"], fx["away"]
        ph, pd, pa = model.outcome_probabilities(elo_by_team[h], elo_by_team[a])
        match_probs.append((h, a, ph, pd, pa))

    for _ in range(sims):
        points = {t: 0 for t in team_names}
        gd = {t: 0 for t in team_names}
        gf = {t: 0 for t in team_names}

        for h, a, ph, pd, pa in match_probs:
            roll = random.random()
            if roll < ph:
                points[h] += 3
                m = random.choice([1, 1, 2, 2, 3])
                gd[h] += m; gd[a] -= m; gf[h] += m
            elif roll < ph + pd:
                points[h] += 1; points[a] += 1
                g = random.choice([0, 1, 1, 2, 2, 3])
                gf[h] += g; gf[a] += g
            else:
                points[a] += 3
                m = random.choice([1, 1, 2, 2, 3])
                gd[a] += m; gd[h] -= m; gf[a] += m

        # Rank teams by points, GD, GF
        ranked = sorted(team_names, key=lambda t: (-points[t], -gd[t], -gf[t]))
        for rank_pos, t in enumerate(ranked, 1):
            if rank_pos <= 8:
                top8_counts[t] += 1
            if rank_pos <= 24:
                top24_counts[t] += 1
            points_accum[t] += points[t]
            rank_accum[t].append(rank_pos)

    results = {}
    for t in team_names:
        ranks = sorted(rank_accum[t])
        median_rank = ranks[len(ranks) // 2]
        results[t] = {
            "name": t,
            "prob_top8": round(top8_counts[t] / sims, 4),
            "prob_top24": round(top24_counts[t] / sims, 4),
            "mean_points": round(points_accum[t] / sims, 2),
            "median_rank": median_rank,
            "starting_elo": elo_by_team[t],
        }

    return results


# ---------------------------------------------------------------------------
# Step-Up (Walk-Forward Matchday-by-Matchday) Runner (Micro)
# ---------------------------------------------------------------------------

def run_step_up_backtest(seeds, fixtures, variant="standard"):
    """
    Simulates chronological progression through Matchdays 1 to 8.
    Predicts matches BEFORE each kickoff; updates Elo AFTER results.
    Zero future leakage.
    """
    current_elo = {s["name"]: s["baseline_elo"] for s in seeds}
    elo_history = {s["name"]: [s["baseline_elo"]] for s in seeds}
    
    match_evaluations = []
    matchdays = defaultdict(list)
    for fx in fixtures:
        matchdays[fx["matchday"]].append(fx)

    for md in sorted(matchdays.keys()):
        md_fixtures = matchdays[md]
        md_updates = []

        for fx in md_fixtures:
            h, a = fx["home"], fx["away"]
            gh, ga = fx["home_score"], fx["away_score"]
            result = fx["result"]

            # PREDICTION (using only information available prior to this matchday)
            ph, pd, pa = model.outcome_probabilities(current_elo[h], current_elo[a])
            pred_outcome = "H" if ph >= pd and ph >= pa else ("A" if pa >= pd else "D")
            is_hit = 1 if pred_outcome == result else 0

            loss = match_log_loss(ph, pd, pa, result)
            brier = match_brier_score(ph, pd, pa, result)

            match_evaluations.append({
                "match_id": fx["match_id"],
                "matchday": md,
                "home": h,
                "away": a,
                "elo_home_pre": round(current_elo[h], 1),
                "elo_away_pre": round(current_elo[a], 1),
                "prob_home": round(ph, 4),
                "prob_draw": round(pd, 4),
                "prob_away": round(pa, 4),
                "predicted_outcome": pred_outcome,
                "actual_outcome": result,
                "home_score": gh,
                "away_score": ga,
                "is_hit": is_hit,
                "log_loss": round(loss, 4),
                "brier_score": round(brier, 4),
            })

            # Queue Elo updates (applied at end of matchday to simulate simultaneous round)
            dh, da = calculate_elo_delta(current_elo[h], current_elo[a], gh, ga, variant=variant)
            md_updates.append((h, dh))
            md_updates.append((a, da))

        # Apply matchday Elo adjustments
        for team, delta in md_updates:
            current_elo[team] += delta

        # Record snapshot of ratings after this matchday
        for s in seeds:
            team = s["name"]
            elo_history[team].append(round(current_elo[team], 1))

    # Aggregate metrics
    n_matches = len(match_evaluations)
    total_loss = sum(m["log_loss"] for m in match_evaluations)
    total_brier = sum(m["brier_score"] for m in match_evaluations)
    total_hits = sum(m["is_hit"] for m in match_evaluations)

    summary = {
        "variant": variant,
        "matches_evaluated": n_matches,
        "mean_log_loss": round(total_loss / n_matches, 4),
        "mean_brier_score": round(total_brier / n_matches, 4),
        "outcome_accuracy": round(total_hits / n_matches, 4),
        "final_elo": {t: round(current_elo[t], 1) for t in current_elo},
        "elo_history": elo_history,
        "match_details": match_evaluations,
    }
    return summary


# ---------------------------------------------------------------------------
# Knockout Stage Full Bracket Simulator
# ---------------------------------------------------------------------------

def simulate_two_legged_knockout_tie(elo_high, elo_low):
    """
    Simulates a 2-legged tie between a higher-seeded club and a lower-seeded club.
    Leg 1: lower seed hosts (elo_low has home bonus).
    Leg 2: higher seed hosts (elo_high has home bonus).
    Aggregate score determines winner. If tied, shootout decided by elo_tiebreak_probability.
    """
    # Leg 1: Low hosts
    p_l1, p_d1, p_h1 = model.outcome_probabilities(elo_low, elo_high)
    roll1 = random.random()
    agg_high = 0
    if roll1 < p_l1:
        agg_high -= random.choice([1, 1, 2, 2, 3])
    elif roll1 >= p_l1 + p_d1:
        agg_high += random.choice([1, 1, 2, 2, 3])

    # Leg 2: High hosts
    p_h2, p_d2, p_l2 = model.outcome_probabilities(elo_high, elo_low)
    roll2 = random.random()
    if roll2 < p_h2:
        agg_high += random.choice([1, 1, 2, 2, 3])
    elif roll2 >= p_h2 + p_d2:
        agg_high -= random.choice([1, 1, 2, 2, 3])

    if agg_high > 0:
        return "high"
    elif agg_high < 0:
        return "low"
    else:
        # Penalties shootout
        p_high_pk = model.elo_tiebreak_probability(elo_high, elo_low)
        return "high" if random.random() < p_high_pk else "low"


def simulate_single_match_final(elo_a, elo_b):
    """Neutral venue single match final."""
    pa, pd, pb = model.outcome_probabilities(elo_a, elo_b, home_bonus=0)
    roll = random.random()
    if roll < pa:
        return "a"
    elif roll >= pa + pd:
        return "b"
    else:
        p_a_pk = model.elo_tiebreak_probability(elo_a, elo_b)
        return "a" if random.random() < p_a_pk else "b"


def run_knockout_bracket_simulations(actual_standings, elo_ratings, sims=10000, seed=42):
    """
    Simulates the UEFA knockout bracket 10,000 times starting from the 36-team standings.
    Bracket rules:
      - Seeds 1-8 receive bye to Round of 16.
      - Play-offs (9-24):
        Pairing pool A: 9/10 vs 23/24
        Pairing pool B: 11/12 vs 21/22
        Pairing pool C: 13/14 vs 19/20
        Pairing pool D: 15/16 vs 17/18
      - Round of 16: Top 8 paired against the 8 playoff winners.
      - QF, SF, Final.
    """
    random.seed(seed)
    teams_by_rank = {s["rank"]: s["name"] for s in actual_standings}
    all_teams = [s["name"] for s in actual_standings]

    r16_counts = {t: 0 for t in all_teams}
    qf_counts = {t: 0 for t in all_teams}
    sf_counts = {t: 0 for t in all_teams}
    final_counts = {t: 0 for t in all_teams}
    champion_counts = {t: 0 for t in all_teams}

    top8_seeds = [teams_by_rank[r] for r in range(1, 9)]
    for t in top8_seeds:
        r16_counts[t] = sims  # Direct bye to R16

    for _ in range(sims):
        # 1. Playoff Round (9-24)
        playoff_pairs = [
            (teams_by_rank[9], teams_by_rank[24]),
            (teams_by_rank[10], teams_by_rank[23]),
            (teams_by_rank[11], teams_by_rank[22]),
            (teams_by_rank[12], teams_by_rank[21]),
            (teams_by_rank[13], teams_by_rank[20]),
            (teams_by_rank[14], teams_by_rank[19]),
            (teams_by_rank[15], teams_by_rank[18]),
            (teams_by_rank[16], teams_by_rank[17]),
        ]
        
        playoff_winners = []
        for high, low in playoff_pairs:
            win_side = simulate_two_legged_knockout_tie(elo_ratings[high], elo_ratings[low])
            winner = high if win_side == "high" else low
            playoff_winners.append(winner)
            r16_counts[winner] += 1

        # 2. Round of 16: Top 8 paired against 8 playoff winners
        # Shuffle pairings to represent draw mechanics
        shuffled_playoff = list(playoff_winners)
        random.shuffle(shuffled_playoff)
        
        qf_teams = []
        for top_seed, po_winner in zip(top8_seeds, shuffled_playoff):
            win_side = simulate_two_legged_knockout_tie(elo_ratings[top_seed], elo_ratings[po_winner])
            winner = top_seed if win_side == "high" else po_winner
            qf_teams.append(winner)
            qf_counts[winner] += 1

        # 3. Quarter-Finals: 4 ties
        random.shuffle(qf_teams)
        sf_teams = []
        for i in range(0, 4):
            t1, t2 = qf_teams[i * 2], qf_teams[i * 2 + 1]
            win_side = simulate_two_legged_knockout_tie(elo_ratings[t1], elo_ratings[t2])
            winner = t1 if win_side == "high" else t2
            sf_teams.append(winner)
            sf_counts[winner] += 1

        # 4. Semi-Finals: 2 ties
        random.shuffle(sf_teams)
        finalists = []
        for i in range(0, 2):
            t1, t2 = sf_teams[i * 2], sf_teams[i * 2 + 1]
            win_side = simulate_two_legged_knockout_tie(elo_ratings[t1], elo_ratings[t2])
            winner = t1 if win_side == "high" else t2
            finalists.append(winner)
            final_counts[winner] += 1

        # 5. Final: 1 match neutral
        champ_side = simulate_single_match_final(elo_ratings[finalists[0]], elo_ratings[finalists[1]])
        champion = finalists[0] if champ_side == "a" else finalists[1]
        champion_counts[champion] += 1

    knockout_probs = {}
    for t in all_teams:
        knockout_probs[t] = {
            "name": t,
            "prob_r16": round(r16_counts[t] / sims, 4),
            "prob_qf": round(qf_counts[t] / sims, 4),
            "prob_sf": round(sf_counts[t] / sims, 4),
            "prob_final": round(final_counts[t] / sims, 4),
            "prob_champion": round(champion_counts[t] / sims, 4),
        }

    return knockout_probs


# ---------------------------------------------------------------------------
# Comprehensive Backtest Suite & Benchmark Evaluation
# ---------------------------------------------------------------------------

def evaluate_predictions(predicted_dict, actual_standings, expert_benchmark, seeds):
    """
    Computes rigorous evaluation metrics comparing:
      1. CL Tracker Model (Pre-Season)
      2. Opta Supercomputer
      3. Naive UEFA Coefficient Baseline
    Against Actual Ground Truth.
    """
    actual_map = {s["name"]: s for s in actual_standings}
    opta_preds = expert_benchmark["predictions"]
    seed_map = {s["name"]: s for s in seeds}

    # Brier Scores on Top 8
    bs_top8_model = sum((predicted_dict[t]["prob_top8"] - (1.0 if actual_map[t]["top8_qualified"] else 0.0)) ** 2 for t in predicted_dict) / len(predicted_dict)
    bs_top8_opta = sum((opta_preds[t]["top8"] - (1.0 if actual_map[t]["top8_qualified"] else 0.0)) ** 2 for t in opta_preds) / len(opta_preds)
    bs_top8_naive = sum(((1.0 if seed_map[t]["seed_rank"] <= 8 else 0.0) - (1.0 if actual_map[t]["top8_qualified"] else 0.0)) ** 2 for t in seed_map) / len(seed_map)

    # Brier Scores on Top 24
    bs_top24_model = sum((predicted_dict[t]["prob_top24"] - (1.0 if actual_map[t]["top24_qualified"] else 0.0)) ** 2 for t in predicted_dict) / len(predicted_dict)
    bs_top24_opta = sum((opta_preds[t]["top24"] - (1.0 if actual_map[t]["top24_qualified"] else 0.0)) ** 2 for t in opta_preds) / len(opta_preds)
    bs_top24_naive = sum(((1.0 if seed_map[t]["seed_rank"] <= 24 else 0.0) - (1.0 if actual_map[t]["top24_qualified"] else 0.0)) ** 2 for t in seed_map) / len(seed_map)

    # Spearman Rank Correlation
    team_list = sorted(actual_map.keys())
    actual_ranks = [actual_map[t]["rank"] for t in team_list]
    model_ranks = [predicted_dict[t]["median_rank"] for t in team_list]
    naive_ranks = [seed_map[t]["seed_rank"] for t in team_list]
    
    # Opta ranks by sorting their top 8 probability
    opta_sorted = sorted(opta_preds.keys(), key=lambda t: (-opta_preds[t]["top8"], -opta_preds[t]["top24"]))
    opta_rank_map = {t: r for r, t in enumerate(opta_sorted, 1)}
    opta_ranks = [opta_rank_map[t] for t in team_list]

    rho_model = spearman_rho(model_ranks, actual_ranks)
    rho_opta = spearman_rho(opta_ranks, actual_ranks)
    rho_naive = spearman_rho(naive_ranks, actual_ranks)

    # Points MAE
    mae_points_model = sum(abs(predicted_dict[t]["mean_points"] - actual_map[t]["points"]) for t in team_list) / len(team_list)

    return {
        "brier_score_top8": {
            "cl_tracker": round(bs_top8_model, 4),
            "opta_supercomputer": round(bs_top8_opta, 4),
            "naive_coefficient_seed": round(bs_top8_naive, 4),
        },
        "brier_score_top24": {
            "cl_tracker": round(bs_top24_model, 4),
            "opta_supercomputer": round(bs_top24_opta, 4),
            "naive_coefficient_seed": round(bs_top24_naive, 4),
        },
        "rank_correlation_rho": {
            "cl_tracker": round(rho_model, 4),
            "opta_supercomputer": round(rho_opta, 4),
            "naive_coefficient_seed": round(rho_naive, 4),
        },
        "points_mae": {
            "cl_tracker": round(mae_points_model, 2),
        }
    }


def main():
    print("=====================================================================")
    print("  CL TRACKER -- 2024/25 HISTORICAL BACKTEST & EVALUATION ENGINE      ")
    print("=====================================================================\n")

    # 1. Load Data
    seeds = json.loads((HISTORICAL_DIR / "starting_seeds.json").read_text(encoding="utf-8"))
    fixtures = json.loads((HISTORICAL_DIR / "fixtures.json").read_text(encoding="utf-8"))
    actual_standings = json.loads((HISTORICAL_DIR / "actual_standings.json").read_text(encoding="utf-8"))
    expert = json.loads((HISTORICAL_DIR / "expert_benchmarks.json").read_text(encoding="utf-8"))
    knockout_truth = json.loads((HISTORICAL_DIR / "knockout_results.json").read_text(encoding="utf-8"))

    print(f"Loaded benchmark dataset: {len(seeds)} clubs, {len(fixtures)} fixtures.\n")

    # 2. Run Pre-Season Monte Carlo Simulation
    print(">>> Running Pre-Season Monte Carlo Simulation (20,000 runs)...")
    preseason_sim = run_preseason_monte_carlo(seeds, fixtures, sims=20000)
    print("    Pre-season simulation complete.")

    # 3. Macro Benchmark Evaluation vs Opta & Ground Truth
    macro_eval = evaluate_predictions(preseason_sim, actual_standings, expert, seeds)
    print("\n--- MACRO LEAGUE PHASE EVALUATION ---")
    print(f"Top 8 Brier Score  (lower is better):")
    print(f"  * CL Tracker:         {macro_eval['brier_score_top8']['cl_tracker']}")
    print(f"  * Opta Supercomputer: {macro_eval['brier_score_top8']['opta_supercomputer']}")
    print(f"  * Naive Coef Seed:    {macro_eval['brier_score_top8']['naive_coefficient_seed']}")

    print(f"\nTop 24 Brier Score (lower is better):")
    print(f"  * CL Tracker:         {macro_eval['brier_score_top24']['cl_tracker']}")
    print(f"  * Opta Supercomputer: {macro_eval['brier_score_top24']['opta_supercomputer']}")
    print(f"  * Naive Coef Seed:    {macro_eval['brier_score_top24']['naive_coefficient_seed']}")

    print(f"\nSpearman Rank Correlation rho (higher is better):")
    print(f"  * CL Tracker:         {macro_eval['rank_correlation_rho']['cl_tracker']}")
    print(f"  * Opta Supercomputer: {macro_eval['rank_correlation_rho']['opta_supercomputer']}")
    print(f"  * Naive Coef Seed:    {macro_eval['rank_correlation_rho']['naive_coefficient_seed']}")
    print(f"Points MAE (CL Tracker): {macro_eval['points_mae']['cl_tracker']} pts")

    # 4. Step-Up (Walk-Forward) Matchday-by-Matchday Backtest
    print("\n>>> Running Step-Up Walk-Forward Backtest (Matchdays 1 to 8)...")
    step_up_standard = run_step_up_backtest(seeds, fixtures, variant="standard")
    step_up_margin = run_step_up_backtest(seeds, fixtures, variant="goal_margin")

    print("\n--- STEP-UP MATCH-LEVEL OUT-OF-SAMPLE EVALUATION ---")
    print(f"Standard Model (Fixed K=22):")
    print(f"  * Mean Log Loss:      {step_up_standard['mean_log_loss']}")
    print(f"  * Multi-class Brier:  {step_up_standard['mean_brier_score']}")
    print(f"  * Outcome Accuracy:   {step_up_standard['outcome_accuracy'] * 100:.2f}%")

    print(f"\nGoal-Margin Scaled Model (K * (1 + ln(margin+1)/2)):")
    print(f"  * Mean Log Loss:      {step_up_margin['mean_log_loss']}")
    print(f"  * Multi-class Brier:  {step_up_margin['mean_brier_score']}")
    print(f"  * Outcome Accuracy:   {step_up_margin['outcome_accuracy'] * 100:.2f}%")

    loss_diff = step_up_margin['mean_log_loss'] - step_up_standard['mean_log_loss']
    brier_diff = step_up_margin['mean_brier_score'] - step_up_standard['mean_brier_score']
    print(f"  Delta (Goal-Margin vs Standard): Log Loss {loss_diff:+.4f}, Brier {brier_diff:+.4f}")

    # 5. Knockout Stage Prediction Simulation
    print("\n>>> Running Knockout Bracket Simulation (10,000 runs)...")
    final_elo_for_knockout = step_up_margin["final_elo"]
    knockout_sim = run_knockout_bracket_simulations(actual_standings, final_elo_for_knockout, sims=10000)

    # Sort knockout predictions by title odds
    sorted_champ = sorted(knockout_sim.values(), key=lambda x: -x["prob_champion"])
    print("\n--- KNOCKOUT TITLE PROBABILITIES (TOP CONTENDERS) ---")
    for row in sorted_champ[:8]:
        actual_mark = " [ACTUAL CHAMPION]" if row["name"] == knockout_truth["final"]["champion"] else ""
        print(f"  * {row['name']:20} Final: {row['prob_final']*100:5.1f}% | Champ: {row['prob_champion']*100:5.1f}%{actual_mark}")

    # Save complete backtest output
    results_output = {
        "season": "2024/25",
        "description": "Full backtest comparing CL Tracker model vs Opta Supercomputer and naive baseline on completed 2024/25 Champions League season",
        "macro_league_phase_evaluation": macro_eval,
        "preseason_monte_carlo_table": preseason_sim,
        "step_up_micro_evaluation": {
            "standard_variant": {
                "mean_log_loss": step_up_standard["mean_log_loss"],
                "mean_brier_score": step_up_standard["mean_brier_score"],
                "outcome_accuracy": step_up_standard["outcome_accuracy"],
            },
            "goal_margin_variant": {
                "mean_log_loss": step_up_margin["mean_log_loss"],
                "mean_brier_score": step_up_margin["mean_brier_score"],
                "outcome_accuracy": step_up_margin["outcome_accuracy"],
            }
        },
        "knockout_stage_predictions": knockout_sim,
        "actual_ground_truth": {
            "league_phase_standings": actual_standings,
            "knockout_results": knockout_truth,
        }
    }

    out_file = HISTORICAL_DIR / "backtest_results.json"
    out_file.write_text(json.dumps(results_output, indent=2), encoding="utf-8")
    print(f"\nSaved complete results payload to: {out_file.resolve()}")


if __name__ == "__main__":
    main()
