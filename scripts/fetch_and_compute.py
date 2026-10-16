"""
Fetches 2026/27 Champions League league phase results from football-data.org,
computes the live table, works out mathematical clinch/elimination status,
and runs a probability model (Elo + Monte Carlo) for each team's chance of
finishing top 8 (auto Round of 16) or top 24 (play-off round).

Writes the result to data/standings.json for the static site to read.

Requires an env var FOOTBALL_DATA_KEY (set as a GitHub Actions secret).
Free tier: 10 requests/minute, includes the Champions League (competition
code "CL") — sign up at https://www.football-data.org/client/register
"""

import json
import math
import os
import random
import sys
import time
import re
import unicodedata
import warnings
from pathlib import Path

import requests

API_KEY = os.environ.get("FOOTBALL_DATA_KEY")

BASE_URL = "https://api.football-data.org/v4"
HEADERS = {"X-Auth-Token": API_KEY}

# football-data.org's free tier is 10 requests/minute. Domestic form now
# pulls two seasons (current + last) across 7 leagues, plus the CL fixtures
# call itself — that's ~15 calls a run, comfortably over 10/min if fired
# back-to-back, which is exactly what caused real 429 crashes in
# production. FD_REQUEST_DELAY throttles every call below that limit;
# fd_get() also retries once on a 429 rather than crashing the run.
FD_REQUEST_DELAY = 6.5  # seconds between calls — keeps us under 10/min with margin


def fd_get(url, params, timeout=30):
    """Wraps requests.get for football-data.org with rate-limit throttling
    and one retry on a 429, so a burst of calls degrades gracefully
    instead of crashing main()."""
    time.sleep(FD_REQUEST_DELAY)
    resp = requests.get(url, headers=HEADERS, params=params, timeout=timeout)
    if resp.status_code == 429:
        print(f"WARNING: rate limited on {url} — waiting 60s and retrying once")
        time.sleep(60)
        resp = requests.get(url, headers=HEADERS, params=params, timeout=timeout)
    return resp
COMPETITION_CODE = "CL"  # a stable short code, not a numeric ID to verify

# Optional second source, only for the 4 domestic leagues football-data.org's
# free tier doesn't cover (Belgium, Turkey, Ukraine, Czechia). Entirely
# opt-in — if disabled, those 4 clubs receive no supplemental form adjustment.
API_FOOTBALL_KEY = os.environ.get("API_FOOTBALL_KEY")
API_FOOTBALL_BASE_URL = "https://v3.football.api-sports.io"


def api_football_enabled():
    """API-Football is opt-in; a configured key alone never triggers calls."""
    return os.environ.get("ENABLE_API_FOOTBALL", "").strip().casefold() in {"1", "true", "yes"}

# (league search name, country name) -> confirmed clubs playing in it.
# Unlike football-data.org's competition codes, API-Football uses numeric
# league IDs that aren't documented anywhere stable enough to hardcode with
# confidence — so these are looked up by name at runtime via /leagues when
# explicitly enabled. The full optional path makes 16 calls per generation.
SUPPLEMENTAL_LEAGUES = {
    ("Jupiler Pro League", "Belgium"): ["Club Brugge"],
    ("Super Lig", "Turkey"): ["Galatasaray"],
    ("Premier League", "Ukraine"): ["Shakhtar Donetsk"],
    ("Czech Liga", "Czech-Republic"): ["Slavia Praha"],
}

SEASON = 2026
LEAGUE_PHASE_MATCHDAYS = 8
TOP_AUTO_R16 = 8
TOP_PLAYOFF_CUTOFF = 24

# --- CONFIRM THIS before first real run ---
# football-data.org's stage value for the 36-team league phase, introduced
# for the 2024/25 reformat. "LEAGUE_STAGE" is the expected value based on
# their public documentation, but confirm it against a real response —
# print(set(m["stage"] for m in matches)) after your first fetch and check
# it matches what's used below.
LEAGUE_PHASE_STAGE = "LEAGUE_STAGE"

# --- Elo / probability model settings ---
# These are real modeling choices, not implementation details — see the
# project README for the reasoning behind each default.
ELO_BASE = 1500
ELO_COEF_SCALE = 4.0       # how many Elo points per coefficient point at kickoff
ELO_K_FACTOR = 22          # how much a single result moves a rating
HOME_ADVANTAGE = 70        # Elo points added to the home side pre-match
BASE_DRAW_PROB = 0.24      # rough historical CL draw rate
DRAW_CLOSENESS_BONUS = 0.06  # extra draw chance when teams are near-even
MONTE_CARLO_SIMULATIONS = 20000  # ~4s at this count on typical GitHub Actions hardware — see README for the tradeoff against 1,000,000

# --- Domestic form settings ---
# Coefficient alone is a 5-year lagging average — it can't see that a team's
# actual current squad is stronger or weaker than their CL history implies.
# This blends in current-season domestic league form as a second signal.
FORM_ELO_SCALE = 90      # Elo points per 1 standard deviation of domestic form
FORM_ELO_CAP = 250       # maximum adjustment in either direction, regardless of z-score
FORM_MIN_GAMES = 3       # don't trust a form signal from fewer than this many domestic games played

# Domestic league competition codes available on football-data.org's free
# tier, mapped to the confirmed clubs playing in each. Covers 7 of the ~11
# countries represented by confirmed clubs — Belgium, Turkey, Ukraine and
# Czechia can receive supplemental form only when API-Football is explicitly
# enabled through ENABLE_API_FOOTBALL.
DOMESTIC_LEAGUES = {
    "PL": ["Arsenal", "Manchester City", "Manchester United", "Aston Villa", "Liverpool"],
    "PD": ["Barcelona", "Real Madrid", "Villarreal", "Atletico Madrid", "Real Betis"],
    "BL1": ["Bayern Munich", "Borussia Dortmund", "RB Leipzig", "VfB Stuttgart"],
    "SA": ["Napoli", "Inter", "Roma", "Como"],
    "FL1": ["Paris Saint-Germain", "Lille", "Lens"],
    "DED": ["PSV Eindhoven", "Feyenoord"],
    "PPL": ["Porto", "Sporting CP"],
}

OUT_PATH = Path(__file__).resolve().parent.parent / "data" / "standings.json"

# 2026 UEFA club coefficients for the 29 confirmed teams, used to seed each
# team's starting Elo rating before any league-phase match has been played.
# Source: UEFA coefficient rankings, as of the 2026/27 season. Keep these
# keys canonical; API spellings are normalized through TEAM_ALIASES before
# lookup. A missing coefficient for a confirmed team is an error, not a fallback.
STARTING_COEFFICIENTS = {
    "Paris Saint-Germain": 132.0, "Bayern Munich": 147.5, "Real Madrid": 144.5,
    "Liverpool": 130.0, "Inter": 127.0, "Manchester City": 125.5,
    "Arsenal": 119.0, "Barcelona": 113.25, "Atletico Madrid": 104.75,
    "Borussia Dortmund": 100.75, "Roma": 97.75, "Sporting CP": 84.0,
    "Aston Villa": 83.0, "Porto": 80.75, "Manchester United": 76.5,
    "Club Brugge": 75.25, "Real Betis": 74.5, "PSV Eindhoven": 71.25,
    "Feyenoord": 71.0, "Lille": 68.75, "Napoli": 63.0, "RB Leipzig": 61.0,
    "Villarreal": 59.0, "Shakhtar Donetsk": 56.25, "Slavia Praha": 44.0,
    "VfB Stuttgart": 27.5, "Galatasaray": 46.5, "Como": 19.989, "Lens": 16.699,
}
# Explicit estimate used only for an unconfirmed qualifying opponent with no
# published coefficient. Confirmed league-phase teams never use this value.
DEFAULT_COEFFICIENT = 15.0

# Real 2026 coefficients for teams still in the qualifying rounds, so tie
# odds reflect actual strength gaps instead of defaulting every qualifier
# to the same DEFAULT_COEFFICIENT (which would make every tie ~50/50).
QUALIFYING_COEFFICIENTS = {
    "Celtic": 44.0, "AEK Athens": 24.0, "LASK": 21.0, "Viking": 8.247,
    "Dinamo Zagreb": 46.5, "Kauno Zalgiris": 13.6,
    "Slovan Bratislava": 36.0, "Mjallby AIF": 5.9,
    "Kairat Almaty": 11.0, "Levski Sofia": 7.0,
    "AGF Aarhus": 8.4, "Sabah FK": 6.0,
    "NK Celje": 23.0, "Ararat-Armenia": 7.0,
    "Red Star Belgrade": 46.5, "Vikingur Reykjavik": 11.75,
    "Olympiacos": 62.25, "NEC Nijmegen": 13.6,
    "Bodo/Glimt": 64.0, "Union Saint-Gilloise": 48.0,
    "Fenerbahce": 57.75, "Sturm Graz": 28.0,
    "Lyon": 65.75, "Sparta Prague": 38.25,
}

# The 10 third-qualifying-round ties, from the 20 July draw. Same manual-
# update caveat as the frontend's copy of this data — see README. Kept
# here too because tie-odds need Elo, which only exists on the backend.
QUALIFYING_TIES = [
    {"label": "Champions Path — CP1", "a": "Dinamo Zagreb", "b": "Kauno Zalgiris"},
    {"label": "Champions Path — CP2", "a": "Slovan Bratislava", "b": "Mjallby AIF"},
    {"label": "Champions Path — CP3", "a": "Kairat Almaty", "b": "Levski Sofia"},
    {"label": "Champions Path — CP4", "a": "AGF Aarhus", "b": "Sabah FK"},
    {"label": "Champions Path — CP5", "a": "NK Celje", "b": "Ararat-Armenia"},
    {"label": "Champions Path — CP6", "a": "Red Star Belgrade", "b": "Hapoel Beer Sheva"},
    {"label": "League Path — LP1", "a": "Olympiacos", "b": "NEC Nijmegen"},
    {"label": "League Path — LP2", "a": "Bodo/Glimt", "b": "Union Saint-Gilloise"},
    {"label": "League Path — LP3", "a": "Fenerbahce", "b": "Sturm Graz"},
    {"label": "League Path — LP4", "a": "Lyon", "b": "Sparta Prague"},
]
TIE_SIMULATIONS = 5000  # smaller than the season sim — only 2 matches per tie, not 8

# First-leg results, third qualifying round, 4-5 Aug 2026. Manually
# entered (same "manual for v1" caveat as QUALIFYING_TIES itself) —
# needs updating again after second legs (11 Aug). margin_for_a is the
# current aggregate goal difference in team "a"'s favor from legs played
# so far; positive means a is ahead, negative means b is ahead.
KNOWN_LEG_RESULTS = {
    "Champions Path — CP1": {"margin_for_a": 5, "note": "Dinamo Zagreb 5-0 Kauno Zalgiris"},
    "Champions Path — CP2": {"margin_for_a": 1, "note": "Slovan Bratislava 2-1 Mjallby AIF"},
    "Champions Path — CP3": {"margin_for_a": -1, "note": "Levski Sofia 1-0 Kairat Almaty"},
    "Champions Path — CP5": {"margin_for_a": -1, "note": "Ararat-Armenia 2-1 NK Celje"},
    "League Path — LP1": {"margin_for_a": 0, "note": "Olympiacos 0-0 NEC Nijmegen"},
    "League Path — LP2": {"margin_for_a": 0, "note": "Bodo/Glimt 3-3 Union Saint-Gilloise"},
    "League Path — LP3": {"margin_for_a": 0, "note": "Fenerbahce 0-0 Sturm Graz"},
}

# Ties with a confirmed final winner (round is fully over for these three —
# the other 7 only have a first-leg result, see KNOWN_LEG_RESULTS above;
# second legs were played 11 Aug but not all 10 final aggregates have been
# tracked down yet, so those 7 still show a live-simulated estimate rather
# than a confirmed final outcome). "winner" is "a" or "b" per QUALIFYING_TIES.
RESOLVED_TIES = {
    "Champions Path — CP4": {"winner": "b", "note": "Final: Sabah FK won 5-2 on aggregate"},
    "Champions Path — CP6": {"winner": "b", "note": "Final: Hapoel Beer Sheva won 3-0 on aggregate"},
    "League Path — LP4": {"winner": "a", "note": "Final: Lyon won 4-2 on aggregate"},
}


FD_FINISHED_STATUSES = {"FINISHED", "AWARDED"}
FD_CANCELLED_STATUSES = {"CANCELLED"}

# Normalize spelling/diacritics at every boundary. Explicit aliases cover
# common API naming variants that are not simple accent/punctuation changes.
TEAM_ALIASES = {
    "1 fc union berlin": "Union Berlin",
    "arsenal fc": "Arsenal",
    "aston villa fc": "Aston Villa",
    "atletico": "Atletico Madrid",
    "atletico de madrid": "Atletico Madrid",
    "atletico madrid cf": "Atletico Madrid",
    "as roma": "Roma",
    "bayern munchen": "Bayern Munich",
    "bodo glimt": "Bodo/Glimt",
    "borussia dortmund": "Borussia Dortmund",
    "bvb": "Borussia Dortmund",
    "club atletico de madrid": "Atletico Madrid",
    "club brugge kv": "Club Brugge",
    "como 1907": "Como",
    "fc barcelona": "Barcelona",
    "fc bayern munchen": "Bayern Munich",
    "fc inter milan": "Inter",
    "fc internazionale milano": "Inter",
    "fc porto": "Porto",
    "fc shakhtar donetsk": "Shakhtar Donetsk",
    "fenerbahce sk": "Fenerbahce",
    "feyenoord rotterdam": "Feyenoord",
    "fk bodo glimt": "Bodo/Glimt",
    "fk shakhtar donetsk": "Shakhtar Donetsk",
    "galatasaray sk": "Galatasaray",
    "internazionale": "Inter",
    "lask linz": "LASK",
    "liverpool fc": "Liverpool",
    "lille osc": "Lille",
    "losc lille": "Lille",
    "manchester city fc": "Manchester City",
    "manchester united fc": "Manchester United",
    "pae aek": "AEK Athens",
    "paris saint germain": "Paris Saint-Germain",
    "paris saint germain fc": "Paris Saint-Germain",
    "psg": "Paris Saint-Germain",
    "psv": "PSV Eindhoven",
    "racing club de lens": "Lens",
    "rc lens": "Lens",
    "real betis balompie": "Real Betis",
    "real madrid cf": "Real Madrid",
    "sk slavia praha": "Slavia Praha",
    "sk slovan bratislava": "Slovan Bratislava",
    "sporting clube de portugal": "Sporting CP",
    "sporting lisbon": "Sporting CP",
    "ssc napoli": "Napoli",
    "viking fk": "Viking",
    "villarreal cf": "Villarreal",
}


def normalize_team_name(name):
    """Return a stable canonical team spelling (accents/case/punctuation-insensitive)."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError(f"Invalid team name: {name!r}")
    transliterated = name.translate(str.maketrans({"ø": "o", "Ø": "O", "ł": "l", "Ł": "L", "đ": "d", "Đ": "D"}))
    decomposed = unicodedata.normalize("NFKD", transliterated)
    plain = "".join(c for c in decomposed if not unicodedata.combining(c))
    key = re.sub(r"[^a-z0-9]+", " ", plain.casefold()).strip()
    alias = TEAM_ALIASES.get(key)
    if alias:
        return alias
    # Preserve canonical names from our internal coefficient table.
    for canonical in (*STARTING_COEFFICIENTS.keys(), *QUALIFYING_COEFFICIENTS.keys()):
        ckey = re.sub(r"[^a-z0-9]+", " ", unicodedata.normalize("NFKD", canonical).encode("ascii", "ignore").decode().casefold()).strip()
        if key == ckey:
            return canonical
    return " ".join(word.capitalize() for word in key.split())


def _normalize_adjustments(adjustments):
    return {normalize_team_name(name): value for name, value in adjustments.items()}


def fetch_fixtures():
    """
    Pull all league-phase matches (results + upcoming) for the season from
    football-data.org, and normalize the response into the same shape the
    rest of this script already expects (which was originally shaped
    around API-Football's response) — so build_table() and everything
    downstream needed zero changes when the data source was swapped.

    Before the league phase draw (27 Aug 2026), football-data.org has no
    season object for the CL competition yet, which returns a 404 — that's
    a normal "nothing exists yet" state, not a real failure, so it's
    handled here rather than left to crash the whole script.
    """
    resp = fd_get(
        f"{BASE_URL}/competitions/{COMPETITION_CODE}/matches",
        params={"season": SEASON},
    )
    if resp.status_code == 404:
        print("INFO: no fixtures available yet for this season (expected "
              "before the 27 Aug league phase draw) — writing empty state.")
        return []
    resp.raise_for_status()
    data = resp.json()
    matches = data.get("matches", [])

    stages = {m.get("stage") for m in matches}
    league_phase = [m for m in matches if m.get("stage") == LEAGUE_PHASE_STAGE]
    if matches and not league_phase:
        raise ValueError(f"No {LEAGUE_PHASE_STAGE!r} fixtures found; API stages were {sorted(str(s) for s in stages)}")

    normalized = []
    for m in league_phase:
        if m.get("status") in FD_CANCELLED_STATUSES:
            continue
        finished = m["status"] in FD_FINISHED_STATUSES
        full_time = m.get("score", {}).get("fullTime", {})
        normalized.append({
            "fixture": {
                "date": m["utcDate"],
                "status": {"short": "FT" if finished else "NS"},
            },
            "league": {"round": f"League Stage - {m.get('matchday', '?')}"},
            "teams": {
                "home": {
                    "id": m["homeTeam"]["id"], "name": normalize_team_name(m["homeTeam"]["name"]),
                    "crest": m["homeTeam"].get("crest"),
                },
                "away": {
                    "id": m["awayTeam"]["id"], "name": normalize_team_name(m["awayTeam"]["name"]),
                    "crest": m["awayTeam"].get("crest"),
                },
            },
            "goals": {
                "home": full_time.get("home"),
                "away": full_time.get("away"),
            },
        })

    # Chronological order matters — Elo updates are applied match by match.
    normalized.sort(key=lambda f: f["fixture"]["date"])
    return normalized


def _ppg_to_elo_adjustments(ppg_by_team):
    """
    Shared math for both domestic-form sources: converts a {team: points-
    per-game} dict for one league into z-scored, capped Elo adjustments.
    Requires at least 2 teams with a usable sample to compute a spread.
    """
    if len(ppg_by_team) < 2:
        return {}

    values = list(ppg_by_team.values())
    mean_ppg = sum(values) / len(values)
    variance = sum((v - mean_ppg) ** 2 for v in values) / len(values)
    stdev_ppg = math.sqrt(variance) if variance > 0 else 1.0

    adjustments = {}
    for name, ppg in ppg_by_team.items():
        z = (ppg - mean_ppg) / stdev_ppg
        adjustments[name] = round(max(-FORM_ELO_CAP, min(FORM_ELO_CAP, z * FORM_ELO_SCALE)))
    return adjustments


def fetch_domestic_form(season):
    """
    Pulls standings for the given season for each domestic league on
    football-data.org's free tier, converts each team's points-per-game
    into a within-league z-score (so a good points-per-game in a weaker
    league doesn't get treated the same as one in a stronger league), then
    scales that into an Elo adjustment.

    Returns {team_name: elo_adjustment}. Teams with no coverage, or fewer
    than FORM_MIN_GAMES played, get no entry — callers default missing
    teams to 0, not a guess.
    """
    if api_football_enabled() and not API_FOOTBALL_KEY:
        raise RuntimeError("ENABLE_API_FOOTBALL is enabled but API_FOOTBALL_KEY is not configured")

    adjustments = {}

    for code in DOMESTIC_LEAGUES:
        try:
            resp = fd_get(
                f"{BASE_URL}/competitions/{code}/standings",
                params={"season": season},
            )
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            print(f"WARNING: couldn't fetch domestic standings for {code} "
                  f"(season {season}): {e}")
            continue

        total_table = next(
            (s["table"] for s in data.get("standings", []) if s.get("type") == "TOTAL"),
            [],
        )
        ppg_by_team = {
            row["team"]["name"]: row["points"] / row["playedGames"]
            for row in total_table
            if row.get("playedGames", 0) >= FORM_MIN_GAMES
        }
        adjustments.update(_ppg_to_elo_adjustments({normalize_team_name(n): p for n, p in ppg_by_team.items()}))

    if api_football_enabled():
        adjustments.update(fetch_supplemental_form(season))
    elif season == SEASON:
        print("INFO: API-Football integration disabled; supplemental domestic-form "
              "clubs will use coefficient-only Elo.")

    return adjustments


def fetch_supplemental_form(season):
    """
    Covers the 4 domestic leagues football-data.org's free tier doesn't
    include, via API-Football. League IDs are looked up by name each run
    rather than hardcoded — see the note on SUPPLEMENTAL_LEAGUES for why.
    """
    if not api_football_enabled():
        return {}
    if not API_FOOTBALL_KEY:
        raise RuntimeError("ENABLE_API_FOOTBALL is enabled but API_FOOTBALL_KEY is not configured")

    headers = {"x-apisports-key": API_FOOTBALL_KEY}
    adjustments = {}

    for (league_name, country), club_names in SUPPLEMENTAL_LEAGUES.items():
        try:
            search_resp = requests.get(
                f"{API_FOOTBALL_BASE_URL}/leagues",
                headers=headers,
                params={"name": league_name, "country": country},
                timeout=30,
            )
            search_resp.raise_for_status()
            results = search_resp.json().get("response", [])
            if not results:
                print(f"WARNING: no API-Football league found for "
                      f"{league_name} ({country}) — skipping {club_names}")
                continue
            league_id = results[0]["league"]["id"]

            standings_resp = requests.get(
                f"{API_FOOTBALL_BASE_URL}/standings",
                headers=headers,
                params={"league": league_id, "season": season},
                timeout=30,
            )
            standings_resp.raise_for_status()
            standings_data = standings_resp.json().get("response", [])
            if not standings_data:
                continue
            table = standings_data[0]["league"]["standings"][0]

        except (requests.RequestException, KeyError, IndexError) as e:
            print(f"WARNING: couldn't fetch supplemental standings for "
                  f"{league_name} (season {season}): {e}")
            continue

        ppg_by_team = {
            row["team"]["name"]: row["points"] / row["all"]["played"]
            for row in table
            if row.get("all", {}).get("played", 0) >= FORM_MIN_GAMES
        }
        adjustments.update(_ppg_to_elo_adjustments({normalize_team_name(n): p for n, p in ppg_by_team.items()}))

    return adjustments


def build_table(fixtures, form_adjustments):
    teams = {}
    form_adjustments = _normalize_adjustments(form_adjustments)

    def ensure(team):
        tid = team["id"]
        name = normalize_team_name(team["name"])
        if tid not in teams:
            teams[tid] = {
                "id": tid, "name": name,
                "crest": team.get("crest"),
                "played": 0, "won": 0, "drawn": 0, "lost": 0,
                "gf": 0, "ga": 0, "points": 0, "fixtures": [],
                "elo": seed_elo(name, form_adjustments),
                "form_adjustment": form_adjustments.get(name, 0),
            }
        return teams[tid]

    for fx in fixtures:
        status = fx["fixture"]["status"]["short"]
        home, away = fx["teams"]["home"], fx["teams"]["away"]
        h, a = ensure(home), ensure(away)
        kickoff = fx["fixture"]["date"]
        played = status in ("FT", "AET", "PEN")

        h["fixtures"].append({
            "opponent": away["name"], "venue": "home", "date": kickoff,
            "played": played,
            "score": f"{fx['goals']['home']}-{fx['goals']['away']}" if played else None,
        })
        a["fixtures"].append({
            "opponent": home["name"], "venue": "away", "date": kickoff,
            "played": played,
            "score": f"{fx['goals']['away']}-{fx['goals']['home']}" if played else None,
        })

        if not played:
            continue

        gh = fx["goals"]["home"] or 0
        ga = fx["goals"]["away"] or 0

        h["played"] += 1; a["played"] += 1
        h["gf"] += gh; h["ga"] += ga
        a["gf"] += ga; a["ga"] += gh

        if gh > ga:
            h["won"] += 1; h["points"] += 3; a["lost"] += 1
            result = 1.0
        elif gh < ga:
            a["won"] += 1; a["points"] += 3; h["lost"] += 1
            result = 0.0
        else:
            h["drawn"] += 1; a["drawn"] += 1; h["points"] += 1; a["points"] += 1
            result = 0.5

        # Elo update — chronological, so later matches use updated ratings.
        expected_home = elo_expected(h["elo"], a["elo"], home_bonus=HOME_ADVANTAGE)
        h["elo"] += ELO_K_FACTOR * (result - expected_home)
        a["elo"] += ELO_K_FACTOR * ((1 - result) - (1 - expected_home))

    return teams


def seed_elo(team_name, form_adjustments, *, allow_unlisted=False):
    team_name = normalize_team_name(team_name)
    form_adjustments = _normalize_adjustments(form_adjustments)
    coef = coefficient_for_team(team_name, allow_unlisted=allow_unlisted)
    return ELO_BASE + coef * ELO_COEF_SCALE + form_adjustments.get(team_name, 0)


class MissingCoefficientError(ValueError):
    """Raised when a team has no explicit UEFA coefficient configured."""


def coefficient_for_team(team_name, *, allow_unlisted=False):
    """Resolve a canonical coefficient, refusing silent guesses by default.

    ``allow_unlisted`` is reserved for qualifying-tie opponents that are not
    among the confirmed league-phase clubs. Those estimates emit a warning.
    """
    canonical = normalize_team_name(team_name)
    if canonical in STARTING_COEFFICIENTS:
        return STARTING_COEFFICIENTS[canonical]
    if canonical in QUALIFYING_COEFFICIENTS:
        return QUALIFYING_COEFFICIENTS[canonical]
    if allow_unlisted:
        warnings.warn(
            f"No UEFA coefficient for unlisted qualifying opponent {team_name!r}; "
            f"using explicit estimate {DEFAULT_COEFFICIENT}",
            RuntimeWarning,
            stacklevel=2,
        )
        return DEFAULT_COEFFICIENT
    raise MissingCoefficientError(
        f"No UEFA coefficient configured for {team_name!r} "
        f"(normalized as {canonical!r}); add its canonical coefficient or alias."
    )


def elo_expected(elo_a, elo_b, home_bonus=0):
    """Standard Elo expected-score formula, 0 to 1, for side A."""
    diff = (elo_a + home_bonus) - elo_b
    return 1.0 / (1.0 + 10 ** (-diff / 400.0))


def elo_tiebreak_probability(elo_a, elo_b):
    """Return the bounded, deliberately mild rating tilt for a shootout."""
    return max(0.0, min(1.0, 0.5 + (elo_a - elo_b) / 4000.0))


def outcome_probabilities(elo_home, elo_away, home_bonus=HOME_ADVANTAGE):
    """
    Return home-win, draw, and away-win probabilities.

    Elo's logistic expected score is E = P(win) + 0.5*P(draw), not P(win).
    A hand-designed closeness curve supplies a maximum draw rate; multiplying
    it by 4*E*(1-E), the normalized variance of the decisive Elo expectation,
    makes draw probability fall as one side becomes dominant while keeping
    win and loss probabilities feasible. We then allocate outcomes around E,
    preserving that expected score. These draw assumptions are not calibrated
    to historical CL data.
    """
    expected_home = elo_expected(elo_home, elo_away, home_bonus=home_bonus)
    diff = abs((elo_home + home_bonus) - elo_away)
    closeness = max(0.0, 1 - diff / 800.0)
    maximum_draw_prob = BASE_DRAW_PROB + DRAW_CLOSENESS_BONUS * closeness
    draw_prob = maximum_draw_prob * 4 * expected_home * (1 - expected_home)
    # Elo's expected score is p(win) + 0.5*p(draw). Allocate draw mass
    # symmetrically around that score; the normalized-variance factor above
    # keeps both decisive outcomes non-negative for any finite Elo gap.
    home_win_prob = expected_home - draw_prob / 2
    away_win_prob = 1 - expected_home - draw_prob / 2
    return home_win_prob, draw_prob, away_win_prob


def add_projections(teams):
    for t in teams.values():
        remaining = LEAGUE_PHASE_MATCHDAYS - t["played"]
        t["remaining"] = remaining
        t["max_points"] = t["points"] + remaining * 3
        t["min_points"] = t["points"]
        t["gd"] = t["gf"] - t["ga"]
        t["fixtures"].sort(key=lambda f: f["date"])
        upcoming = [f for f in t["fixtures"] if not f["played"]]
        t["next_fixture"] = upcoming[0] if upcoming else None


def compute_scenarios(teams):
    """Mathematical floor/ceiling clinch-or-eliminated check — see README
    for why this ignores goal-difference tiebreaks at the margin."""
    all_teams = list(teams.values())

    def status_for_cutoff(team, cutoff):
        others = [t for t in all_teams if t["id"] != team["id"]]
        guaranteed_above = sum(1 for o in others if o["min_points"] > team["max_points"])
        if guaranteed_above >= cutoff:
            return "eliminated"
        can_still_overtake = sum(1 for o in others if o["max_points"] > team["min_points"])
        if can_still_overtake < cutoff:
            return "clinched"
        return "alive"

    for t in all_teams:
        t["status_top8"] = status_for_cutoff(t, TOP_AUTO_R16)
        t["status_top24"] = status_for_cutoff(t, TOP_PLAYOFF_CUTOFF)

    all_teams.sort(key=lambda t: (-t["points"], -t["gd"], -t["gf"]))
    for i, t in enumerate(all_teams, start=1):
        t["rank"] = i
    return all_teams


def run_monte_carlo(teams, remaining_fixtures):
    """
    Simulates the rest of the league phase MONTE_CARLO_SIMULATIONS times
    using each team's current Elo rating (held fixed across the whole
    simulation — a simplification; ratings don't evolve mid-simulation the
    way they do with real results). Returns, per team, the fraction of
    simulations landing in the top 8 / top 24 / outside.
    """
    team_ids = list(teams.keys())
    if len(team_ids) != 36:
        raise ValueError("Monte Carlo requires a complete 36-team league-phase dataset")
    top8_count = {tid: 0 for tid in team_ids}
    top24_count = {tid: 0 for tid in team_ids}

    base_points = {tid: teams[tid]["points"] for tid in team_ids}
    base_gf = {tid: teams[tid]["gf"] for tid in team_ids}
    base_ga = {tid: teams[tid]["ga"] for tid in team_ids}

    for _ in range(MONTE_CARLO_SIMULATIONS):
        points = dict(base_points)
        gd = {tid: base_gf[tid] - base_ga[tid] for tid in team_ids}
        gf = dict(base_gf)

        for fx in remaining_fixtures:
            h_id, a_id = fx["home_id"], fx["away_id"]
            if h_id not in teams or a_id not in teams:
                continue
            elo_h, elo_a = teams[h_id]["elo"], teams[a_id]["elo"]
            p_home, p_draw, p_away = outcome_probabilities(elo_h, elo_a)
            roll = random.random()

            if roll < p_home:
                points[h_id] += 3
                margin = random.choice([1, 1, 2, 2, 3])
                gd[h_id] += margin; gd[a_id] -= margin
                gf[h_id] += margin
            elif roll < p_home + p_draw:
                points[h_id] += 1; points[a_id] += 1
                goals = random.choice([0, 1, 1, 2, 2, 3])
                gf[h_id] += goals; gf[a_id] += goals
            else:
                points[a_id] += 3
                margin = random.choice([1, 1, 2, 2, 3])
                gd[a_id] += margin; gd[h_id] -= margin
                gf[a_id] += margin

        ranked = sorted(team_ids, key=lambda tid: (-points[tid], -gd[tid], -gf[tid]))
        for i, tid in enumerate(ranked, start=1):
            if i <= TOP_AUTO_R16:
                top8_count[tid] += 1
            if i <= TOP_PLAYOFF_CUTOFF:
                top24_count[tid] += 1

    for tid in team_ids:
        teams[tid]["prob_top8"] = round(top8_count[tid] / MONTE_CARLO_SIMULATIONS, 3)
        teams[tid]["prob_top24"] = round(top24_count[tid] / MONTE_CARLO_SIMULATIONS, 3)


def simulate_two_legged_tie(name_a, name_b, sims=TIE_SIMULATIONS):
    """
    Monte Carlo simulation of a two-legged qualifying tie: team A hosts
    leg 1, team B hosts leg 2, aggregate score decides it. If level on
    aggregate, extra time/penalties are modeled as a coin flip nudged
    slightly toward the higher-rated side — a simplification, not a real
    penalty-shootout model, since shootouts are close to 50/50 regardless
    of league form.
    """
    if sims <= 0:
        raise ValueError("sims must be a positive integer")
    elo_a = seed_elo(name_a, {}, allow_unlisted=True)
    elo_b = seed_elo(name_b, {}, allow_unlisted=True)
    a_advances = 0

    for _ in range(sims):
        agg = 0  # from team A's perspective

        # Leg 1: A at home
        p_a, p_d, p_b = outcome_probabilities(elo_a, elo_b)
        roll = random.random()
        if roll < p_a:
            agg += random.choice([1, 1, 2, 2, 3])
        elif roll >= p_a + p_d:
            agg -= random.choice([1, 1, 2, 2, 3])

        # Leg 2: B at home (home advantage flips sides)
        p_b2, p_d2, p_a2 = outcome_probabilities(elo_b, elo_a)
        roll = random.random()
        if roll < p_b2:
            agg -= random.choice([1, 1, 2, 2, 3])
        elif roll >= p_b2 + p_d2:
            agg += random.choice([1, 1, 2, 2, 3])

        if agg > 0:
            a_advances += 1
        elif agg < 0:
            pass
        else:
            # Level on aggregate — extra time/penalties, weighted only
            # slightly by rating rather than the full match model, since
            # shootouts are much closer to a coin flip than open play.
            tiebreak_prob_a = elo_tiebreak_probability(elo_a, elo_b)
            if random.random() < tiebreak_prob_a:
                a_advances += 1

    return round(a_advances / sims, 3)


def simulate_remaining_leg(name_a, name_b, margin_for_a, sims=TIE_SIMULATIONS):
    """
    One leg already played — margin_for_a is the current aggregate goal
    difference in team A's favor. Simulates only the remaining leg rather
    than both, since one result is already real, not projected. Venue for
    the remaining leg isn't tracked in our data, so no home advantage is
    applied to either side here — a reasonable simplification given what
    we actually know.
    """
    if sims <= 0:
        raise ValueError("sims must be a positive integer")
    elo_a = seed_elo(name_a, {}, allow_unlisted=True)
    elo_b = seed_elo(name_b, {}, allow_unlisted=True)
    a_advances = 0

    for _ in range(sims):
        agg = margin_for_a
        p_a, p_d, p_b = outcome_probabilities(elo_a, elo_b, home_bonus=0)
        roll = random.random()
        if roll < p_a:
            agg += random.choice([1, 1, 2, 2, 3])
        elif roll >= p_a + p_d:
            agg -= random.choice([1, 1, 2, 2, 3])

        if agg > 0:
            a_advances += 1
        elif agg < 0:
            pass
        else:
            tiebreak_prob_a = elo_tiebreak_probability(elo_a, elo_b)
            if random.random() < tiebreak_prob_a:
                a_advances += 1

    return round(a_advances / sims, 3)


def build_qualifying_odds():
    """Advance probability for each third-qualifying-round tie. Resolved
    ties (RESOLVED_TIES) show the real, final outcome, not a simulation.
    Ties with a known first-leg result (KNOWN_LEG_RESULTS) simulate only
    the remaining leg using the real aggregate. Ties with no result at all
    simulate both legs from scratch. Independent of league-phase
    fixtures — same manual-update caveat as QUALIFYING_TIES itself."""
    odds = []
    for tie in QUALIFYING_TIES:
        resolved = RESOLVED_TIES.get(tie["label"])
        known = KNOWN_LEG_RESULTS.get(tie["label"])

        if resolved:
            prob_a = 1.0 if resolved["winner"] == "a" else 0.0
            leg_note = resolved["note"]
            is_resolved = True
        elif known:
            prob_a = simulate_remaining_leg(tie["a"], tie["b"], known["margin_for_a"])
            leg_note = known["note"]
            is_resolved = False
        else:
            prob_a = simulate_two_legged_tie(tie["a"], tie["b"])
            leg_note = None
            is_resolved = False

        odds.append({
            "label": tie["label"], "a": tie["a"], "b": tie["b"],
            "prob_a": prob_a, "prob_b": round(1 - prob_a, 3),
            "leg_note": leg_note, "resolved": is_resolved,
        })
    return odds


def build_remaining_fixtures(fixtures):
    remaining = []
    for fx in fixtures:
        if fx["fixture"]["status"]["short"] in ("FT", "AET", "PEN"):
            continue
        remaining.append({
            "home_id": fx["teams"]["home"]["id"],
            "away_id": fx["teams"]["away"]["id"],
        })
    return remaining


def league_phase_schedule_is_complete(fixtures, teams):
    """Require all 36 clubs and exactly eight fixtures per club."""
    if len(teams) != 36 or len(fixtures) != 144:
        return False
    if len({normalize_team_name(t["name"]) for t in teams.values()}) != 36:
        return False
    counts = {tid: 0 for tid in teams}
    home_counts = {tid: 0 for tid in teams}
    away_counts = {tid: 0 for tid in teams}
    pairs = set()
    for fx in fixtures:
        home_id = fx["teams"]["home"]["id"]
        away_id = fx["teams"]["away"]["id"]
        if home_id == away_id or home_id not in counts or away_id not in counts:
            return False
        pair = frozenset((home_id, away_id))
        if pair in pairs:
            return False
        pairs.add(pair)
        counts[home_id] += 1
        counts[away_id] += 1
        home_counts[home_id] += 1
        away_counts[away_id] += 1
    return (
        all(count == LEAGUE_PHASE_MATCHDAYS for count in counts.values())
        and all(count == LEAGUE_PHASE_MATCHDAYS // 2 for count in home_counts.values())
        and all(count == LEAGUE_PHASE_MATCHDAYS // 2 for count in away_counts.values())
    )


def build_match_list(fixtures, teams):
    """
    Full match list for the Matches page — every league-phase fixture,
    with win/draw/loss odds attached to unplayed ones. This is a direct
    Elo calculation per match, not a simulation — no Monte Carlo needed
    for a single match's odds, only for something aggregate like season
    standings or a multi-leg tie.
    """
    matches = []
    for fx in fixtures:
        status = fx["fixture"]["status"]["short"]
        played = status in ("FT", "AET", "PEN")
        home_id, away_id = fx["teams"]["home"]["id"], fx["teams"]["away"]["id"]

        odds = None
        if not played and home_id in teams and away_id in teams:
            p_h, p_d, p_a = outcome_probabilities(teams[home_id]["elo"], teams[away_id]["elo"])
            odds = {"home": round(p_h, 3), "draw": round(p_d, 3), "away": round(p_a, 3)}

        matches.append({
            "matchday": fx["league"].get("round", ""),
            "date": fx["fixture"]["date"],
            "home": fx["teams"]["home"]["name"],
            "away": fx["teams"]["away"]["name"],
            "played": played,
            "score": f"{fx['goals']['home']}-{fx['goals']['away']}" if played else None,
            "odds": odds,
        })
    matches.sort(key=lambda m: m["date"])
    return matches


def fetch_combined_form():
    """
    Combines two form signals: this season's in-progress form (only
    non-empty once FORM_MIN_GAMES has been played — mostly not yet) and
    last season's completed final standing (always available now, since
    that season is already over). Current-season data takes priority per
    team once it exists; last season is the fallback, not blended in
    alongside it — a clean handoff rather than a permanent mix, so a
    team's rating isn't perpetually dragged by a season that's over.
    """
    current = fetch_domestic_form(SEASON)
    last_season = fetch_domestic_form(SEASON - 1)
    combined = dict(last_season)
    combined.update(current)  # current season overrides last season per team
    return combined


def build_provisional_standings(form_adjustments):
    """
    A real, data-driven pre-season ranking — coefficient blended with last
    season's actual final domestic position, not just a raw coefficient
    sort. Exists independently of live CL fixtures, so it's meaningful
    immediately rather than waiting for the league phase draw.
    """
    rows = []
    for name, coef in STARTING_COEFFICIENTS.items():
        rows.append({
            "name": name,
            "coefficient": coef,
            "form_adjustment": form_adjustments.get(name, 0),
            "elo": round(seed_elo(name, form_adjustments)),
        })
    rows.sort(key=lambda r: -r["elo"])
    for i, r in enumerate(rows, start=1):
        r["rank"] = i
    return rows


def main():
    if not API_KEY:
        sys.exit("Missing FOOTBALL_DATA_KEY env var")
    form_adjustments = fetch_combined_form()
    provisional_standings = build_provisional_standings(form_adjustments)

    fixtures = fetch_fixtures()
    if not fixtures and OUT_PATH.exists():
        try:
            previous = json.loads(OUT_PATH.read_text())
        except (OSError, json.JSONDecodeError):
            previous = {}
        if previous.get("teams") or previous.get("matches"):
            raise RuntimeError("API returned no league-phase fixtures while published data exists; refusing to replace it with an empty snapshot")
    teams = build_table(fixtures, form_adjustments)
    add_projections(teams)

    remaining_fixtures = build_remaining_fixtures(fixtures)
    schedule_complete = league_phase_schedule_is_complete(fixtures, teams)
    if schedule_complete:
        run_monte_carlo(teams, remaining_fixtures)
    else:
        print(f"WARNING: incomplete league-phase schedule ({len(teams)} teams, {len(fixtures)} fixtures); qualification probabilities withheld")

    ranked = compute_scenarios(teams)
    if not schedule_complete:
        for team in ranked:
            team["status_top8"] = "pending"
            team["status_top24"] = "pending"
            team["prob_top8"] = None
            team["prob_top24"] = None
    matches = build_match_list(fixtures, teams)
    qualifying_odds = build_qualifying_odds()

    for t in ranked:
        t.pop("fixtures", None)  # next_fixture already covers the per-team need
        t.pop("id", None)
        t["elo"] = round(t["elo"])

    output = {
        "generated_at": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "league_phase_matchdays": LEAGUE_PHASE_MATCHDAYS,
        "top_auto_r16": TOP_AUTO_R16,
        "top_playoff_cutoff": TOP_PLAYOFF_CUTOFF,
        "all_teams_confirmed": len({normalize_team_name(t["name"]) for t in ranked}) == 36,
        "schedule_complete": schedule_complete,
        "teams": ranked,
        "matches": matches,
        "qualifying_odds": qualifying_odds,
        "provisional_standings": provisional_standings,
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(output, indent=2))
    print(f"Wrote {len(ranked)} teams, {len(matches)} matches, "
          f"{len(qualifying_odds)} qualifying ties, "
          f"{len(provisional_standings)} provisional standings to {OUT_PATH}")


if __name__ == "__main__":
    main()
