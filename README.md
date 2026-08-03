# CL League Phase Tracker

Live table + clinch/elimination scenario tracking for the 2026/27
Champions League league phase, updating itself via GitHub Actions.

## Setup (do this before Matchday 1, 8 Sept 2026)

### 1. Get a football-data.org key
- Sign up free at https://www.football-data.org/client/register
- Free tier: 10 requests/minute (a rate limit, not a daily cap), covers
  12 competitions including the Champions League. This project makes
  about 8 calls per run (1 for CL fixtures, up to 7 for domestic league
  standings used in the form model below) — comfortably under the limit.

### 1b. (Optional) Get an API-Football key too
Covers domestic form for the 4 leagues football-data.org's free tier
doesn't include — Belgium (Club Brugge), Turkey (Galatasaray), Ukraine
(Shakhtar Donetsk), Czechia (Slavia Praha). Skip this entirely and those
4 clubs just get coefficient-only Elo, same as before this existed —
nothing else breaks.
- Sign up free at https://www.api-football.com — free tier is 100
  requests/day, this adds ~8 calls per run (2 per league × 4 leagues)
- Add it as a repo secret named `API_FOOTBALL_KEY` alongside
  `FOOTBALL_DATA_KEY` in step 4 below

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
  league form, z-scored against their own league and capped at ±150 Elo
  (`FORM_ELO_SCALE`, `FORM_ELO_CAP`). Coefficient alone is a 5-year
  lagging average — it can't see that a squad has visibly improved or
  declined since. Form alone is noisy over a handful of games. Blending
  both is deliberately closer to how real prediction models handle it
  than either signal on its own.
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
  as the rating gap widens — not fit to real historical CL data, just a
  reasonable curve
- The percentage shown is how often a team lands in the top 8 / top 24
  across all 20,000 simulated seasons

None of the constants (`ELO_K_FACTOR`, `HOME_ADVANTAGE`, `BASE_DRAW_PROB`,
`FORM_ELO_SCALE`) are tuned against real results — they're reasonable
starting values. If the model's predictions look consistently off once
real results come in, that's the first place to adjust, not a sign the
whole approach is broken.

## Qualifying tab — manual for v1

The third qualifying round and play-off round bracket
(`QUALIFYING_PATHS` in `index.html`) is hardcoded from the actual 20
July draw, not pulled from the API. Update it by hand after each round
resolves. Automating this against football-data.org's qualifying-round data
is a reasonable v2 — it wasn't done here to keep the first working
version shippable rather than stalled on edge cases in how the API
represents pre-league-phase rounds.

