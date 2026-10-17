"""
CL Tracker — Historical Model Backtesting & Calibration Suite.

Evaluates prospective pre-match probability predictions against verified
match outcomes without data leakage. Computes multi-class Brier score,
multi-class log loss, pick accuracy, probability calibration, and baseline
comparisons.

Runs completely offline without external network or API calls.
"""

import argparse
import json
import math
from pathlib import Path
import sys
import types

# Ensure repo root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Pure offline execution: stub requests if not installed locally
if "requests" not in sys.modules:
    requests_stub = types.ModuleType("requests")
    requests_stub.RequestException = Exception
    requests_stub.get = lambda *args, **kwargs: None
    sys.modules["requests"] = requests_stub

import scripts.fetch_and_compute as model

DEFAULT_FIXTURE_PATH = REPO_ROOT / "tests" / "fixtures" / "backtest_2026_md1_md2.json"

# Standard long-term Champions League empirical base rates
EMPIRICAL_BASE_RATES = {"home": 0.45, "draw": 0.24, "away": 0.31}
UNIFORM_BASE_RATES = {"home": 1.0 / 3.0, "draw": 1.0 / 3.0, "away": 1.0 / 3.0}


def brier_score(preds, actual):
    """Multi-class Brier score: sum_{k in {H,D,A}} (p_k - o_k)^2. Lower is better."""
    o_h = 1.0 if actual == "home" else 0.0
    o_d = 1.0 if actual == "draw" else 0.0
    o_a = 1.0 if actual == "away" else 0.0
    return (preds["home"] - o_h) ** 2 + (preds["draw"] - o_d) ** 2 + (preds["away"] - o_a) ** 2


def log_loss(preds, actual, eps=1e-15):
    """Multi-class logarithmic loss (cross-entropy). Lower is better."""
    p = max(eps, min(1.0 - eps, preds[actual]))
    return -math.log(p)


def evaluate_predictions(fixtures, predict_fn=None, apply_market_values=True):
    """
    Evaluate match predictions across a list of fixture records.

    Each fixture record must contain:
      - elo_home, elo_away: pre-match Elo ratings
      - actual: 'home', 'draw', or 'away'
      - published_odds: optional dict with 'home', 'draw', 'away'
      - matchday: int
    """
    if predict_fn is None:
        def predict_fn(elo_h, elo_a):
            h, d, a = model.outcome_probabilities(elo_h, elo_a)
            return {"home": round(h, 3), "draw": round(d, 3), "away": round(a, 3)}

    n = len(fixtures)
    if n == 0:
        raise ValueError("Cannot evaluate an empty fixture set")

    outcomes = {"home": 0, "draw": 0, "away": 0}
    brier_model, ll_model = [], []
    brier_pre_mv, ll_pre_mv = [], []
    brier_pub, ll_pub = [], []
    brier_emp, ll_emp = [], []
    brier_unif, ll_unif = [], []
    correct_model, correct_pre_mv, correct_pub, correct_emp = 0, 0, 0, 0

    sum_pred_h, sum_pred_d, sum_pred_a = 0.0, 0.0, 0.0
    by_matchday = {}

    for fx in fixtures:
        actual = fx["actual"]
        outcomes[actual] += 1
        md = fx.get("matchday", 1)
        if md not in by_matchday:
            by_matchday[md] = {"n": 0, "brier_model": [], "brier_pub": [], "brier_emp": []}

        # Calibrated model prediction (incorporating squad market values if enabled)
        if apply_market_values:
            mv_h = model.market_value_adjustment(fx.get("home", ""))
            mv_a = model.market_value_adjustment(fx.get("away", ""))
            elo_h = fx["elo_home"] + mv_h
            elo_a = fx["elo_away"] + mv_a
        else:
            elo_h = fx["elo_home"]
            elo_a = fx["elo_away"]

        p_model = predict_fn(elo_h, elo_a)
        bm = brier_score(p_model, actual)
        lm = log_loss(p_model, actual)
        brier_model.append(bm)
        ll_model.append(lm)
        sum_pred_h += p_model["home"]
        sum_pred_d += p_model["draw"]
        sum_pred_a += p_model["away"]
        if max(p_model, key=p_model.get) == actual:
            correct_model += 1

        # Pre-calibration (pure coefficient/form Elo without market values)
        p_pre_mv = predict_fn(fx["elo_home"], fx["elo_away"])
        bpmv = brier_score(p_pre_mv, actual)
        lpmv = log_loss(p_pre_mv, actual)
        brier_pre_mv.append(bpmv)
        ll_pre_mv.append(lpmv)
        if max(p_pre_mv, key=p_pre_mv.get) == actual:
            correct_pre_mv += 1

        # Published odds (historical pre-fix odds, if present)
        p_pub = fx.get("published_odds")
        if p_pub:
            bp = brier_score(p_pub, actual)
            lp = log_loss(p_pub, actual)
            brier_pub.append(bp)
            ll_pub.append(lp)
            if max(p_pub, key=p_pub.get) == actual:
                correct_pub += 1
            by_matchday[md]["brier_pub"].append(bp)

        # Baselines
        be = brier_score(EMPIRICAL_BASE_RATES, actual)
        le = log_loss(EMPIRICAL_BASE_RATES, actual)
        brier_emp.append(be)
        ll_emp.append(le)
        if max(EMPIRICAL_BASE_RATES, key=EMPIRICAL_BASE_RATES.get) == actual:
            correct_emp += 1

        bu = brier_score(UNIFORM_BASE_RATES, actual)
        lu = log_loss(UNIFORM_BASE_RATES, actual)
        brier_unif.append(bu)
        ll_unif.append(lu)

        by_matchday[md]["n"] += 1
        by_matchday[md]["brier_model"].append(bm)
        by_matchday[md]["brier_emp"].append(be)

    matchday_summary = {}
    for md, val in sorted(by_matchday.items()):
        matchday_summary[md] = {
            "n": val["n"],
            "brier_model": sum(val["brier_model"]) / val["n"],
            "brier_pub": (sum(val["brier_pub"]) / len(val["brier_pub"])) if val["brier_pub"] else None,
            "brier_emp": sum(val["brier_emp"]) / val["n"],
        }

    return {
        "n_matches": n,
        "observed_counts": outcomes,
        "observed_rates": {k: v / n for k, v in outcomes.items()},
        "model": {
            "brier": sum(brier_model) / n,
            "log_loss": sum(ll_model) / n,
            "accuracy": correct_model / n,
            "avg_predicted": {
                "home": sum_pred_h / n,
                "draw": sum_pred_d / n,
                "away": sum_pred_a / n,
            },
        },
        "pre_market_value": {
            "brier": sum(brier_pre_mv) / n,
            "log_loss": sum(ll_pre_mv) / n,
            "accuracy": correct_pre_mv / n,
        },
        "published": {
            "brier": (sum(brier_pub) / len(brier_pub)) if brier_pub else None,
            "log_loss": (sum(ll_pub) / len(ll_pub)) if ll_pub else None,
            "accuracy": (correct_pub / len(brier_pub)) if brier_pub else None,
        },
        "baseline_empirical": {
            "brier": sum(brier_emp) / n,
            "log_loss": sum(ll_emp) / n,
            "accuracy": correct_emp / n,
        },
        "baseline_uniform": {
            "brier": sum(brier_unif) / n,
            "log_loss": sum(ll_unif) / n,
            "accuracy": None,
        },
        "matchday_breakdown": matchday_summary,
    }


def format_report(results):
    n = results["n_matches"]
    obs = results["observed_rates"]
    m = results["model"]
    pmv = results.get("pre_market_value")
    pub = results["published"]
    emp = results["baseline_empirical"]
    unif = results["baseline_uniform"]

    lines = []
    lines.append("=" * 72)
    lines.append("  CL TRACKER — HISTORICAL MODEL BACKTEST & CALIBRATION REPORT")
    lines.append("=" * 72)
    lines.append(f"Sample size: N = {n} matches")
    lines.append(f"Observed outcomes: Home {obs['home']:.1%} | Draw {obs['draw']:.1%} | Away {obs['away']:.1%}")
    lines.append("")
    lines.append(f"{'Model / Baseline':<32} | {'Brier':<10} | {'LogLoss':<10} | {'Accuracy':<10}")
    lines.append("-" * 72)
    lines.append(f"{'Current Model (Calibrated Elo+MV)':<32} | {m['brier']:<10.4f} | {m['log_loss']:<10.4f} | {m['accuracy']:<10.1%}")
    if pmv and pmv["brier"] is not None:
        lines.append(f"{'Pre-Calibration Model (PR #1)':<32} | {pmv['brier']:<10.4f} | {pmv['log_loss']:<10.4f} | {pmv['accuracy']:<10.1%}")
    if pub["brier"] is not None:
        lines.append(f"{'Published Model (Original)':<32} | {pub['brier']:<10.4f} | {pub['log_loss']:<10.4f} | {pub['accuracy']:<10.1%}")
    lines.append(f"{'Empirical Baseline (45/24/31)':<32} | {emp['brier']:<10.4f} | {emp['log_loss']:<10.4f} | {emp['accuracy']:<10.1%}")
    lines.append(f"{'Uniform Baseline (33/33/33)':<32} | {unif['brier']:<10.4f} | {unif['log_loss']:<10.4f} | {'N/A':<10}")
    lines.append("")
    lines.append("--- Matchday Breakdown ---")
    for md, val in results["matchday_breakdown"].items():
        pub_str = f", Published: {val['brier_pub']:.4f}" if val["brier_pub"] is not None else ""
        lines.append(f"Matchday {md} (N={val['n']}): Model Brier = {val['brier_model']:.4f}{pub_str}, Baseline = {val['brier_emp']:.4f}")
    lines.append("")
    lines.append("--- Calibration Check ---")
    for outcome in ["home", "draw", "away"]:
        pred_p = m["avg_predicted"][outcome]
        act_p = obs[outcome]
        bias = pred_p - act_p
        lines.append(f"{outcome.capitalize():<6}: Predicted {pred_p:>5.1%} vs Actual {act_p:>5.1%} (Bias: {bias:>+5.1%})")
    lines.append("=" * 72)
    return "\n".join(lines)


def run(fixture_path=DEFAULT_FIXTURE_PATH):
    path = Path(fixture_path)
    if not path.exists():
        sys.exit(f"Fixture file not found: {path}")

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    matches = data.get("matches", [])
    results = evaluate_predictions(matches)
    return results


def main():
    parser = argparse.ArgumentParser(description="Run historical CL tracker backtest")
    parser.add_argument("--fixture", default=str(DEFAULT_FIXTURE_PATH), help="Path to fixture JSON file")
    parser.add_argument("--json", action="store_true", help="Print output as JSON")
    args = parser.parse_args()

    results = run(args.fixture)
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(format_report(results))


if __name__ == "__main__":
    main()
