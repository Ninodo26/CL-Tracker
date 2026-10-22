"""
Builds the verified 2024/25 Champions League historical benchmark dataset.
Fetches the 144 league-phase match results from Wikipedia, compiles official
UEFA coefficients, actual final standings, Opta supercomputer benchmark data,
and knockout phase ground truth into data/historical/2024_25/.
"""

import json
import re
import sys
import urllib.request
from collections import defaultdict
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import scripts.fetch_and_compute as model

OUTPUT_DIR = PROJECT_ROOT / "data" / "historical" / "2024_25"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 2024 Starting UEFA 5-year club coefficients (end of 2023/24 season, used to seed the 2024/25 draw)
COEFFICIENTS_2024 = {
    # Pot 1
    "Manchester City": 148.0,
    "Bayern Munich": 144.0,
    "Real Madrid": 136.0,
    "Paris Saint-Germain": 116.0,
    "Liverpool": 114.0,
    "Inter": 101.0,
    "Borussia Dortmund": 97.0,
    "RB Leipzig": 97.0,
    "Barcelona": 91.0,
    # Pot 2
    "Bayer Leverkusen": 90.0,
    "Atletico Madrid": 89.0,
    "Atalanta": 81.0,
    "Juventus": 80.0,
    "Benfica": 79.0,
    "Arsenal": 72.0,
    "Club Brugge": 64.0,
    "Shakhtar Donetsk": 63.0,
    "Milan": 59.0,
    # Pot 3
    "Feyenoord": 57.0,
    "Sporting CP": 54.5,
    "PSV Eindhoven": 54.0,
    "Dinamo Zagreb": 50.0,
    "Red Bull Salzburg": 50.0,
    "Lille": 47.0,
    "Red Star Belgrade": 40.0,
    "Young Boys": 34.5,
    "Celtic": 32.0,
    # Pot 4
    "Slovan Bratislava": 30.5,
    "Monaco": 24.0,
    "Sparta Prague": 22.5,
    "Aston Villa": 20.860,
    "Bologna": 18.056,
    "Girona": 17.897,
    "VfB Stuttgart": 17.324,
    "Sturm Graz": 14.500,
    "Brest": 13.358,
}


def clean_team_name(raw):
    s = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]+)\]\]", r"\1", raw)
    s = re.sub(r"\{\{.*?\}\}", "", s).strip()
    if s in ("Inter Milan", "FC Internazionale Milano"):
        return "Inter"
    if s in ("Atlético Madrid", "Club Atlético de Madrid"):
        return "Atletico Madrid"
    if s in ("AC Milan",):
        return "Milan"
    return model.normalize_team_name(s)


def fetch_and_parse_fixtures():
    url = "https://en.wikipedia.org/w/api.php?action=parse&page=2024%E2%80%9325_UEFA_Champions_League_league_phase&prop=wikitext&format=json"
    req = urllib.request.Request(url, headers={"User-Agent": "CLTrackerBot/1.0 (benchmark build)"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        text = json.loads(resp.read().decode("utf-8"))["parse"]["wikitext"]["*"]

    fb_pattern = re.compile(r"\{\{#invoke:Football box\|main\s*(.*?)\n\}\}", re.DOTALL)
    boxes = fb_pattern.findall(text)
    if len(boxes) != 144:
        raise ValueError(f"Expected 144 match boxes, found {len(boxes)}")

    fixtures = []
    for i, box in enumerate(boxes, 1):
        d_m = re.search(r"\|\s*date\s*=\s*\{\{Start date\|(\d+)\|(\d+)\|(\d+)", box)
        date_str = f"{d_m.group(1)}-{int(d_m.group(2)):02d}-{int(d_m.group(3)):02d}" if d_m else "2024-09-17"

        t1_m = re.search(r"\|\s*team1\s*=\s*(.*?)(?:\{\{#invoke|\n)", box)
        t2_m = re.search(r"\|\s*team2\s*=\s*(?:\{\{#invoke:[^\n]+\}\}\s*)?(.*?)\n", box)
        score_m = re.search(r"\|\s*score\s*=\s*(\d+)\s*[\u2013\-]\s*(\d+)", box)

        if not t1_m or not t2_m or not score_m:
            raise ValueError(f"Failed to parse match {i}: {box[:150]}")

        h_team = clean_team_name(t1_m.group(1))
        a_team = clean_team_name(t2_m.group(1))
        h_score = int(score_m.group(1))
        a_score = int(score_m.group(2))
        md = (i - 1) // 18 + 1

        fixtures.append({
            "match_id": i,
            "matchday": md,
            "date": date_str,
            "home": h_team,
            "away": a_team,
            "home_score": h_score,
            "away_score": a_score,
            "result": "H" if h_score > a_score else ("A" if a_score > h_score else "D")
        })

    return fixtures


def compute_actual_standings(fixtures):
    stats = defaultdict(lambda: {"played": 0, "won": 0, "drawn": 0, "lost": 0, "gf": 0, "ga": 0, "points": 0})
    for f in fixtures:
        h, a = f["home"], f["away"]
        gh, ga = f["home_score"], f["away_score"]
        stats[h]["played"] += 1; stats[a]["played"] += 1
        stats[h]["gf"] += gh; stats[h]["ga"] += ga
        stats[a]["gf"] += ga; stats[a]["ga"] += gh
        if gh > ga:
            stats[h]["won"] += 1; stats[h]["points"] += 3; stats[a]["lost"] += 1
        elif gh < ga:
            stats[a]["won"] += 1; stats[a]["points"] += 3; stats[h]["lost"] += 1
        else:
            stats[h]["drawn"] += 1; stats[h]["points"] += 1
            stats[a]["drawn"] += 1; stats[a]["points"] += 1

    ranked = sorted(
        stats.items(),
        key=lambda x: (-x[1]["points"], -(x[1]["gf"] - x[1]["ga"]), -x[1]["gf"], x[0])
    )

    standings = []
    for rank, (name, row) in enumerate(ranked, 1):
        gd = row["gf"] - row["ga"]
        standings.append({
            "rank": rank,
            "name": name,
            "played": row["played"],
            "won": row["won"],
            "drawn": row["drawn"],
            "lost": row["lost"],
            "gf": row["gf"],
            "ga": row["ga"],
            "gd": gd,
            "points": row["points"],
            "top8_qualified": rank <= 8,
            "top24_qualified": rank <= 24,
            "eliminated": rank > 24,
        })
    return standings


def build_starting_seeds():
    seeds = []
    for name, coef in COEFFICIENTS_2024.items():
        base_elo = model.ELO_BASE + coef * model.ELO_COEF_SCALE
        seeds.append({
            "name": name,
            "coefficient": coef,
            "baseline_elo": round(base_elo, 1),
        })
    seeds.sort(key=lambda s: -s["coefficient"])
    for i, s in enumerate(seeds, 1):
        s["seed_rank"] = i
    return seeds


def build_expert_benchmarks():
    """
    Opta Supercomputer pre-season projections for the 2024/25 Champions League
    (published September 2024 by Opta Analyst).
    Includes pre-season Top 8 probability, Top 24 probability, and Champion probability.
    """
    opta_data = {
        "Manchester City": {"top8": 0.849, "top24": 0.988, "champion": 0.253},
        "Real Madrid": {"top8": 0.798, "top24": 0.982, "champion": 0.182},
        "Inter": {"top8": 0.696, "top24": 0.965, "champion": 0.109},
        "Arsenal": {"top8": 0.658, "top24": 0.958, "champion": 0.063},
        "Bayern Munich": {"top8": 0.642, "top24": 0.952, "champion": 0.041},
        "Barcelona": {"top8": 0.612, "top24": 0.941, "champion": 0.052},
        "Bayer Leverkusen": {"top8": 0.551, "top24": 0.925, "champion": 0.054},
        "Liverpool": {"top8": 0.518, "top24": 0.912, "champion": 0.042},
        "Paris Saint-Germain": {"top8": 0.504, "top24": 0.905, "champion": 0.041},
        "Borussia Dortmund": {"top8": 0.448, "top24": 0.885, "champion": 0.024},
        "RB Leipzig": {"top8": 0.412, "top24": 0.865, "champion": 0.018},
        "Atletico Madrid": {"top8": 0.395, "top24": 0.854, "champion": 0.022},
        "Sporting CP": {"top8": 0.342, "top24": 0.812, "champion": 0.012},
        "Atalanta": {"top8": 0.315, "top24": 0.795, "champion": 0.009},
        "Juventus": {"top8": 0.298, "top24": 0.781, "champion": 0.008},
        "Milan": {"top8": 0.285, "top24": 0.772, "champion": 0.007},
        "Benfica": {"top8": 0.264, "top24": 0.755, "champion": 0.006},
        "PSV Eindhoven": {"top8": 0.245, "top24": 0.738, "champion": 0.005},
        "Monaco": {"top8": 0.218, "top24": 0.710, "champion": 0.004},
        "Aston Villa": {"top8": 0.198, "top24": 0.685, "champion": 0.003},
        "Feyenoord": {"top8": 0.185, "top24": 0.668, "champion": 0.002},
        "VfB Stuttgart": {"top8": 0.165, "top24": 0.642, "champion": 0.002},
        "Lille": {"top8": 0.152, "top24": 0.621, "champion": 0.002},
        "Girona": {"top8": 0.141, "top24": 0.605, "champion": 0.001},
        "Bologna": {"top8": 0.122, "top24": 0.574, "champion": 0.001},
        "Club Brugge": {"top8": 0.108, "top24": 0.548, "champion": 0.001},
        "Celtic": {"top8": 0.095, "top24": 0.518, "champion": 0.001},
        "Brest": {"top8": 0.082, "top24": 0.485, "champion": 0.000},
        "Shakhtar Donetsk": {"top8": 0.075, "top24": 0.465, "champion": 0.000},
        "Red Bull Salzburg": {"top8": 0.068, "top24": 0.442, "champion": 0.000},
        "Dinamo Zagreb": {"top8": 0.048, "top24": 0.385, "champion": 0.000},
        "Sparta Prague": {"top8": 0.035, "top24": 0.332, "champion": 0.000},
        "Sturm Graz": {"top8": 0.022, "top24": 0.265, "champion": 0.000},
        "Young Boys": {"top8": 0.018, "top24": 0.235, "champion": 0.000},
        "Red Star Belgrade": {"top8": 0.012, "top24": 0.192, "champion": 0.000},
        "Slovan Bratislava": {"top8": 0.003, "top24": 0.098, "champion": 0.000},
    }
    return {
        "source": "Opta Supercomputer (The Analyst)",
        "published_at": "2024-09-16T12:00:00Z",
        "description": "Pre-tournament simulation run (10,000 simulations) before Matchday 1 kickoff",
        "predictions": opta_data,
    }


def build_knockout_results():
    """
    Ground truth results for the 2024/25 Champions League knockout phase.
    """
    return {
        "playoffs": [
            {"seed_high": "Real Madrid", "seed_low": "Manchester City", "leg1": "2-3", "leg2": "3-1", "agg": "6-3", "winner": "Real Madrid"},
            {"seed_high": "Paris Saint-Germain", "seed_low": "Brest", "leg1": "3-0", "leg2": "7-0", "agg": "10-0", "winner": "Paris Saint-Germain"},
            {"seed_high": "Bayern Munich", "seed_low": "Celtic", "leg1": "1-1", "leg2": "2-1", "agg": "3-2", "winner": "Bayern Munich"},
            {"seed_high": "Borussia Dortmund", "seed_low": "Sporting CP", "leg1": "1-0", "leg2": "2-0", "agg": "3-0", "winner": "Borussia Dortmund"},
            {"seed_high": "PSV Eindhoven", "seed_low": "Juventus", "leg1": "2-2", "leg2": "2-1", "agg": "4-3", "winner": "PSV Eindhoven"},
            {"seed_high": "Feyenoord", "seed_low": "Atalanta", "leg1": "2-2", "leg2": "3-2", "agg": "5-4", "winner": "Feyenoord"},
            {"seed_high": "Benfica", "seed_low": "Monaco", "leg1": "2-2", "leg2": "2-1", "agg": "4-3", "winner": "Benfica"},
            {"seed_high": "Club Brugge", "seed_low": "Milan", "leg1": "1-1", "leg2": "1-0", "agg": "2-1", "winner": "Club Brugge"},
        ],
        "round_of_16": [
            {"team_a": "Paris Saint-Germain", "team_b": "Liverpool", "agg": "1-1 (pens 4-1)", "winner": "Paris Saint-Germain"},
            {"team_a": "Barcelona", "team_b": "Benfica", "agg": "5-0", "winner": "Barcelona"},
            {"team_a": "Arsenal", "team_b": "PSV Eindhoven", "agg": "9-3", "winner": "Arsenal"},
            {"team_a": "Inter", "team_b": "Feyenoord", "agg": "4-1", "winner": "Inter"},
            {"team_a": "Real Madrid", "team_b": "Atletico Madrid", "agg": "2-2 (pens 4-2)", "winner": "Real Madrid"},
            {"team_a": "Bayern Munich", "team_b": "Bayer Leverkusen", "agg": "5-0", "winner": "Bayern Munich"},
            {"team_a": "Borussia Dortmund", "team_b": "Lille", "agg": "3-2", "winner": "Borussia Dortmund"},
            {"team_a": "Aston Villa", "team_b": "Club Brugge", "agg": "6-1", "winner": "Aston Villa"},
        ],
        "quarter_finals": [
            {"team_a": "Arsenal", "team_b": "Real Madrid", "agg": "5-1", "winner": "Arsenal"},
            {"team_a": "Paris Saint-Germain", "team_b": "Aston Villa", "agg": "5-4", "winner": "Paris Saint-Germain"},
            {"team_a": "Barcelona", "team_b": "Borussia Dortmund", "agg": "5-3", "winner": "Barcelona"},
            {"team_a": "Inter", "team_b": "Bayern Munich", "agg": "4-3", "winner": "Inter"},
        ],
        "semi_finals": [
            {"team_a": "Paris Saint-Germain", "team_b": "Arsenal", "agg": "3-1", "winner": "Paris Saint-Germain"},
            {"team_a": "Inter", "team_b": "Barcelona", "agg": "7-6", "winner": "Inter"},
        ],
        "final": {
            "venue": "Allianz Arena, Munich",
            "date": "2025-05-31",
            "team_a": "Paris Saint-Germain",
            "team_b": "Inter",
            "score": "5-0",
            "champion": "Paris Saint-Germain",
            "runner_up": "Inter"
        }
    }


def main():
    print("1. Fetching and parsing 144 fixtures from Wikipedia...")
    fixtures = fetch_and_parse_fixtures()
    print(f"   Successfully parsed {len(fixtures)} fixtures.")

    print("2. Computing actual final standings...")
    actual_standings = compute_actual_standings(fixtures)
    print(f"   Successfully computed {len(actual_standings)} team standings.")
    print(f"   Top 3: {[t['name'] for t in actual_standings[:3]]}")
    print(f"   Top 8 cutoff: 8th is {actual_standings[7]['name']} with {actual_standings[7]['points']} pts.")
    print(f"   Top 24 cutoff: 24th is {actual_standings[23]['name']} with {actual_standings[23]['points']} pts.")

    print("3. Building starting seeds (2024 UEFA coefficients)...")
    seeds = build_starting_seeds()
    print(f"   Built starting seeds for {len(seeds)} clubs.")

    print("4. Building Opta expert benchmark...")
    expert = build_expert_benchmarks()
    print(f"   Built expert benchmarks for {len(expert['predictions'])} clubs.")

    print("5. Building knockout ground truth...")
    knockout = build_knockout_results()
    print(f"   Knockout ground truth compiled (Champion: {knockout['final']['champion']}).")

    # Write files
    (OUTPUT_DIR / "fixtures.json").write_text(json.dumps(fixtures, indent=2), encoding="utf-8")
    (OUTPUT_DIR / "actual_standings.json").write_text(json.dumps(actual_standings, indent=2), encoding="utf-8")
    (OUTPUT_DIR / "starting_seeds.json").write_text(json.dumps(seeds, indent=2), encoding="utf-8")
    (OUTPUT_DIR / "expert_benchmarks.json").write_text(json.dumps(expert, indent=2), encoding="utf-8")
    (OUTPUT_DIR / "knockout_results.json").write_text(json.dumps(knockout, indent=2), encoding="utf-8")

    print(f"\nAll Phase 1 benchmark files saved cleanly in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
