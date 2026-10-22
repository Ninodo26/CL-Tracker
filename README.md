# CL League Phase Tracker

Live table + clinch/elimination scenario tracking for the 2026/27
Champions League league phase, updating itself via GitHub Actions.

## Setup (do this before Matchday 1, 8 Sept 2026)

### 1. Get a football-data.org key
- Sign up free at https://www.football-data.org/client/register
- Free tier: 10 requests/minute (a rate limit, not a daily cap), covers
  12 competitions including the Champions League. This project makes
  up to 15 calls per run (1 for CL fixtures plus up to 7 domestic leagues
  across the current and previous seasons), throttled by the script.

### 1b. (Optional) Get an API-Football key too
Covers domestic form for the 4 leagues football-data.org's free tier
doesn't include — Belgium (Club Brugge), Turkey (Galatasaray), Ukraine
(Shakhtar Donetsk), Czechia (Slavia Praha). Skip this entirely and those
4 clubs just get coefficient-only Elo, same as before this existed —
nothing else breaks.
- Sign up free at https://www.api-football.com — free tier is 100
  requests/day, this adds ~8 calls per run (2 per league × 4 leagues)
- Add it as a repo secret named `API_FOOTBALL_KEY` alongside
  `FOOTBALL_DATA_KEY` in step 4 below. The workflow passes both secrets.

### 2. Confirm the league-phase stage name
The script assumes matches use `"stage": "LEAGUE_STAGE"` for the 36-team
format. Confirm it once you have a key:

    curl -H "X-Auth-Token: YOUR_KEY" \
      "https://api.football-data.org/v4/competitions/CL/matches?season=2026" \
      | python3 -c "import json,sys; print(set(m['stage'] for m in json.load(sys.stdin)['matches']))"

If `LEAGUE_STAGE` isn't in that set, update `LEAGUE_PHASE_STAGE` in
`scripts/fetch_and_compute.py` to whatever value actually appears.

### 3. Create the GitHub repo
- Push this folder as a new repo (public, since GitHub Pages needs that
  on the free tier — or use a private repo + Pro if you want it private)

### 4. Add the API key as a secret
Repo → Settings → Secrets and variables → Actions → New repository secret
- Name: `FOOTBALL_DATA_KEY`
- Value: your key

### 5. Enable GitHub Pages
Repo → Settings → Pages → Source: Deploy from branch → `main` / root

### 6. Test it manually
Repo → Actions → "Update standings" → Run workflow (the `workflow_dispatch`
trigger lets you fire it on demand instead of waiting for the cron).
Check that `data/standings.json` gets committed with real data once
matches exist.

## How the scenario logic works

For each team, every remaining game is assumed either won (ceiling) or
lost (floor). A team is:

- **Clinched** for a cutoff (top 8 or top 24) if fewer than that many
  other teams could possibly reach or beat its guaranteed floor
- **Eliminated** if that many other teams have already guaranteed more
  points than this team could possibly reach
- **Alive** otherwise

This is a mathematical floor/ceiling check on points only — it does not
model the full official UEFA tiebreak order (goal difference, goals
scored, disciplinary points, coefficient), so treat borderline calls
near a cutoff as "close" rather than definitive until points alone
settle it.

## Adjusting the update frequency

The cron in `.github/workflows/update.yml` runs every 3 hours. Champions
League league-phase matchdays land on Tuesdays and Wednesdays almost
always — if you want fresher same-night updates, tighten the cron on
those days specifically, e.g. hourly 18:00–23:00 CET on Tue/Wed with a
second, sparser cron for the rest of the week.

## Site Structure & Capabilities

Six comprehensive sections designed to compete with world-class sports analytics platforms (FotMob, SofaScore, Opta Analyst):

1. **Standings** — Live 36-club league-phase table, clinch and elimination scenario tracking, one-click single season Monte Carlo simulation rollout, and instant **TikTok / Social Story Card Export**. Clicking any club opens their tactical dossier.
2. **Matches** — Complete 144-match league-phase fixtures with the current active round displayed at the top, past matchdays accessible by scrolling up, quick-nav jump pills, and **2D Tactical Pitch Lineup Views** with Starting XIs, formations, managers, and injury watches.
3. **Power Rankings** — Multi-tier power rankings balancing title odds, automatic Round of 16 qualification, playoff survival, and underlying Elo strength (with non-100% probabilistic bounds).
4. **Stats & Leaders** — Comprehensive tournament leaderboards:
   - **Golden Boot**: Top scorers, assists, minutes, xG (Expected Goals), and Goals/90
   - **Playmaking Masters**: Top assists, big chances created, and key passes
   - **Golden Glove**: Clean sheets, saves made, save %, and goals conceded
   - **Power Movers**: Biggest Elo rating swings and momentum shifts
5. **5th Spot Race (EPS)** — Tracking the UEFA European Performance Spots battle (England, Italy, Spain, Germany, France) for the two additional automatic Champions League berths in 2027/28.
6. **Model Accuracy & Backtest** — Empirical validation scorecard comparing CL Tracker against the Opta Supercomputer and ground truth from the completed 2024/25 season.

### 📱 TikTok & Social Media Card Generator
- Client-side high-resolution HTML5 Canvas rendering engine.
- Formats: **9:16 Vertical (1080×1920)** for TikTok / Instagram Stories / Reels and **1:1 Square (1080×1080)** for Twitter/X / Instagram feed posts.
- Features: Real-time visual preview, one-click high-res PNG download, and direct system clipboard copy (`navigator.clipboard.write`) for instant viral posting.
- Export cards available for:
  - Any Match (Odds, Predicted Result, Key Player Showdown, Stakes)
  - Standings (Top 8 Qualifiers, Cutoff Thresholds, Bubble Teams)
  - Any Club (Tactical DNA, Key Players, Advancement Outlook)

### 📋 2D Tactical Pitch & Lineup Engine
- Authentic formations (4-3-3, 4-2-3-1, 3-5-2, 3-4-2-1, 4-4-2) for all 36 participating clubs.
- Interactive grass pitch rendering with touchlines, penalty boxes, center circle, and player jersey nodes with squad numbers and surnames.
- Manager profiles, tactical directives, substitute benches, and injury updates.

## The probability model (Power Rankings & Knockout Engine)

Real modeling choices, empirically validated through backtesting:

- **Calibrated Starting Elo**: Each team's Elo rating is initialized from three blended signals:
  1. 5-year UEFA club coefficient (`STARTING_COEFFICIENTS`)
  2. Squad market valuation (`SQUAD_VALUATIONS`)
  3. Domestic league strength tiering (`DOMESTIC_LEAGUE_TIERS`)
  This directly overcomes the historical hysteresis of UEFA coefficients alone, properly valuing clubs like Aston Villa (€615M Premier League squad in Pot 4) and recalibrating transitioning clubs like RB Leipzig.
- **Domestic Form Integration**: In-season league form is z-scored against the club's domestic competition and blended with previous-season baselines cached locally (`data/cache/prior_season_form.json`) to minimize live API consumption.
- **Goal Margin Elo Scaling**: Match updates scale $K$-factor by victory margin (`1.0 + (margin - 1) * 0.35`), rewarding dominant performances and improving match-level predictive log loss.
- **Expected-Score-Preserving Draw Curve**: Win/draw/loss probabilities are converted from Elo differences using a closeness-dependent draw distribution that rigorously preserves expected score:
  $$P(\text{win}) + 0.5 \times P(\text{draw}) = E$$
- **Full Tournament Monte Carlo (20,000 Runs)**: Each run simulates all remaining league-phase fixtures and executes the entire knockout ladder:
  - Seeds 1–8: Automatic Round of 16 entry
  - Seeds 9–24: Two-legged Playoff round (9 vs 24, 10 vs 23, etc.)
  - Round of 16, Quarter-finals, and Semi-finals (two legs each)
  - Neutral single-leg Final (Munich 2025 / Budapest 2026)
  The simulation produces `prob_top8`, `prob_top24`, `prob_final`, and `prob_champion` for every club.

## Historical Backtesting & Validation (2024/25 Benchmark)

The model was comprehensively backtested against the complete 2024/25 UEFA Champions League season (144 league phase fixtures + 16-team knockout bracket) without data leakage:

| Metric | CL Tracker | Opta Supercomputer | Naive UEFA Seed |
| :--- | :---: | :---: | :---: |
| **Spearman Rank Correlation ($\rho$)** | **0.7165** | 0.7287 | 0.5359 |
| **Top-8 Brier Score** (Lower is better) | **0.1873** | 0.1561 | 0.3333 |
| **Top-24 Brier Score** (Lower is better) | **0.1210** | 0.0898 | 0.1654 |
| **Match Direction Accuracy (144/144)** | **64.58%** (93/144) | — | 33.33% |
| **Match Log Loss** | **0.9448** | — | 1.0986 |

To re-run the historical benchmark and generate the validation report:

```bash
python scripts/build_historical_dataset.py
python scripts/backtest.py
```

To run the unit test suite:

```bash
python -m unittest discover tests
```


