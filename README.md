# CL League Phase Tracker

Live table + clinch/elimination scenario tracking for the 2026/27
Champions League league phase, updating itself via GitHub Actions.

## Setup (do this before Matchday 1, 8 Sept 2026)

### 1. Get a football-data.org key
- Sign up free at https://www.football-data.org/client/register
- Free tier: 10 requests/minute (a rate limit, not a daily cap), covers
  12 competitions including the Champions League. The generator makes 15
  calls per run (1 for CL fixtures plus 7 domestic leagues across each of
  the current and previous seasons), throttled by the script.

### 1b. (Optional) Enable API-Football domestic form
This optional source covers Belgium (Club Brugge), Turkey (Galatasaray),
Ukraine (Shakhtar Donetsk), and Czechia (Slavia Praha). It is disabled by
default. When disabled, the generator makes zero API-Football requests and
does not need `API_FOOTBALL_KEY`; those clubs receive no domestic-form
adjustment.

If you choose to enable it, configure the repository Actions variable
`ENABLE_API_FOOTBALL` as `true` and add `API_FOOTBALL_KEY` as a repository
secret. The current implementation makes 16 calls per generation (four
leagues × a league lookup and standings request × current and previous
seasons). At the existing eight scheduled runs per day that would be up to
128 API-Football calls/day, so confirm the provider plan supports that budget.
Do not enable it by adding the secret alone.

### Provider request budgets
- **football-data.org:** 15 requests per normal run: one Champions League
  fixture request plus seven domestic league standings requests for each of
  the current and previous seasons. Each initial request waits 6.5 seconds;
  one 429 retry waits 60 seconds. No API-Football calls are part of the
  default run.
- **API-Football:** zero requests by default; 16 per run only when explicitly
  enabled as described above.

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

## Site structure

Four tabs: **Standings** (provisional coefficient ranking pre-season,
real points table once matches exist), **Matches** (every league-phase
fixture, grouped by matchday), **Qualifying** (the third qualifying
round ties for the last 7 spots), **Power Rankings** (Elo + simulated
top-8/top-24 odds).

The favourite-team picker is gated behind `all_teams_confirmed` in the
JSON (true once the API returns 36 distinct teams in league-phase
fixtures, which happens right after the 27 August draw) — before that
it shows a locked message instead of a partial 29-team picker.

## The probability model (Power Rankings)

Real modeling choices, not just implementation details:

- Each team's Elo rating starts from two blended signals: their 2026 UEFA
  coefficient (`STARTING_COEFFICIENTS`) and their current-season domestic
  league form, z-scored against their own league and capped at ±250 Elo
  (`FORM_ELO_SCALE`, `FORM_ELO_CAP`). Coefficient alone is a 5-year
  lagging average — it can't see that a squad has visibly improved or
  declined since. Form alone is noisy over a handful of games. Blending
  both is deliberately closer to how real prediction models handle it
  than either signal on its own.
- API team spellings pass through one canonical alias map before coefficient
  lookup. A confirmed league-phase club without a configured coefficient
  stops the run with a clear error; only unlisted qualifying opponents may
  use the explicitly warned estimate in `DEFAULT_COEFFICIENT`.
- Domestic form only covers 7 of the ~11 countries in the 29 confirmed
  clubs — England, Spain, Germany, Italy, France, Netherlands, Portugal
  (`DOMESTIC_LEAGUES`). Belgium, Turkey, Ukraine, and Czechia aren't on
  football-data.org's free tier, so those clubs get coefficient only, not
  a silently wrong number.
- Every played result updates both teams' Elo, chronologically, with a
  home-advantage bonus baked into the expected-score calculation
- Remaining fixtures are simulated 20,000 times using each team's
  *current* Elo (held fixed across one simulation run — ratings don't
  evolve mid-simulation, that's a deliberate simplification). Benchmarked
  at ~4s on typical hardware; 1,000,000 simulations (closer to what
  commercial models like Opta run) was tested too but costs over 3
  minutes per run — roughly a third of the free monthly GitHub Actions
  budget at this cron schedule, for precision past the point the model's
  other assumptions can really support.
- Draw probability is highest between evenly-matched teams and shrinks
  as the rating gap widens. The win/draw/loss conversion preserves the
  Elo expected score (`P(win) + 0.5 × P(draw)`). It scales the closeness
  curve by the normalized variance of Elo expected score so all three
  outcomes stay feasible as the rating gap grows.
  The curve is not fit to historical CL data.
- The percentage shown is how often a team lands in the top 8 / top 24
  across all 20,000 simulated seasons

The pipeline withholds qualification odds and clinch calls until all 36
distinct clubs and 144 unique fixtures (eight per club, four home and four
away) are present. An
empty API response cannot replace a previously populated snapshot. The
simulation approximates tied positions with points, goal difference, and
simulated goals scored; it does not model the full UEFA tie-break order.
The Elo scale and constants (`ELO_K_FACTOR`, `HOME_ADVANTAGE`,
`BASE_DRAW_PROB`, `FORM_ELO_SCALE`) remain uncalibrated against historical
results and need backtesting before these probabilities should be treated
as well calibrated.

## Qualifying tab — manual for v1

The third qualifying round and play-off round bracket
(`QUALIFYING_PATHS` in `index.html`) is hardcoded from the actual 20
July draw, not pulled from the API. Update it by hand after each round
resolves. Automating this against football-data.org's qualifying-round data
is a reasonable v2 — it wasn't done here to keep the first working
version shippable rather than stalled on edge cases in how the API
represents pre-league-phase rounds.
