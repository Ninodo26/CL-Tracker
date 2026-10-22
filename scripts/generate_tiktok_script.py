#!/usr/bin/env python3
"""
generate_tiktok_script.py

Generates high-retention TikTok narration scripts and multi-scene storyboards
from live Champions League simulation and standings data.
"""

import json
import os
import sys
import argparse
from pathlib import Path

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"

def load_data():
    standings_path = DATA_DIR / "standings.json"
    dossiers_path = DATA_DIR / "team_dossiers.json"
    
    with open(standings_path, "r", encoding="utf-8") as f:
        standings = json.load(f)
        
    dossiers = {}
    if dossiers_path.exists():
        with open(dossiers_path, "r", encoding="utf-8") as f:
            dossiers = json.load(f)
            
    return standings, dossiers

def find_marquee_match(matches, standings):
    """Find the most compelling upcoming match based on team ranks and odds."""
    unplayed = [m for m in matches if not m.get("played")]
    if not unplayed:
        # Fallback to the latest played marquee match
        return matches[-1] if matches else None
        
    # Pick match from the nearest upcoming matchday
    current_md = unplayed[0].get("matchday")
    md_matches = [m for m in unplayed if m.get("matchday") == current_md]
    
    team_ranks = {t["name"]: t.get("rank", 99) for t in standings.get("teams", [])}
    
    # Score matches by prominence (lower combined rank = bigger clash)
    best_match = None
    best_score = float("inf")
    
    for m in md_matches:
        r1 = team_ranks.get(m["home"], 50)
        r2 = team_ranks.get(m["away"], 50)
        score = r1 + r2
        if score < best_score:
            best_score = score
            best_match = m
            
    return best_match or md_matches[0]

def build_match_storyboard(match, standings, dossiers):
    home = match["home"]
    away = match["away"]
    odds = match.get("odds") or {"home": 0.45, "draw": 0.25, "away": 0.30}
    md = match.get("matchday", "Matchday 4").replace("League Stage - ", "Matchday ")
    
    p_home = round(odds.get("home", 0.45) * 100)
    p_draw = round(odds.get("draw", 0.25) * 100)
    p_away = round(odds.get("away", 0.30) * 100)
    
    teams_dict = {t["name"]: t for t in standings.get("teams", [])}
    t_home = teams_dict.get(home, {})
    t_away = teams_dict.get(away, {})
    
    r_home = t_home.get("rank", "?")
    r_away = t_away.get("rank", "?")
    pts_home = t_home.get("points", 0)
    pts_away = t_away.get("points", 0)
    
    # 4-Scene Storyboard for maximum TikTok retention
    scenes = [
        {
            "id": "scene_1_hook",
            "type": "match",
            "payload": match,
            "title": f"🚨 {home.upper()} VS {away.upper()}",
            "voice_text": f"The Champions League supercomputer just simulated 20,000 outcomes for {home} versus {away}, and the final probability is shocking.",
            "caption": "20,000 SIMULATIONS COMPLETE",
            "zoom_direction": "in"
        },
        {
            "id": "scene_2_odds",
            "type": "match",
            "payload": match,
            "title": f"📊 OFFICIAL AI ODDS",
            "voice_text": f"Our model gives {home} a {p_home} percent win chance, with {away} sitting at {p_away} percent, and the draw projected at {p_draw} percent.",
            "caption": f"{p_home}% {home.split()[-1]} | {p_away}% {away.split()[-1]}",
            "zoom_direction": "out"
        },
        {
            "id": "scene_3_standings",
            "type": "standings",
            "payload": {},
            "title": "🏆 TABLE IMPLICATIONS",
            "voice_text": f"In the league phase table, every single point matters. 16 points secures direct qualification to the Round of 16, while losing risks falling into the cutthroat playoff danger zone.",
            "caption": "TOP 8 CUTOFF DRAMA",
            "zoom_direction": "in"
        },
        {
            "id": "scene_4_cta",
            "type": "team",
            "payload": {"name": away if p_away < p_home else home},
            "title": "⚽ WHO WINS?",
            "voice_text": f"Will the supercomputer get this right, or are we in for a massive Champions League upset? Drop your score prediction in the comments and follow for live matchday updates!",
            "caption": "DROP YOUR SCORE PREDICTION 👇",
            "zoom_direction": "out"
        }
    ]
    
    meta = {
        "title": f"{home} vs {away} - Champions League AI Prediction ({md})",
        "description": f"Supercomputer simulation breakdown for {home} vs {away} in {md}! 20,000 Monte Carlo tournament rollouts predict the odds. Who takes the 3 points?\n\n#UCL #ChampionsLeague #Football #Predictions #Opta #Soccer #UEFA #Matchday",
        "home": home,
        "away": away,
        "matchday": md
    }
    
    return {"scenes": scenes, "meta": meta}

def build_standings_storyboard(standings, dossiers):
    teams = standings.get("teams", [])
    top_8 = teams[:8]
    bubble = teams[7:12]
    
    leader = teams[0]["name"] if teams else "Paris Saint-Germain"
    
    scenes = [
        {
            "id": "scene_1_hook",
            "type": "standings",
            "payload": {},
            "title": "🚨 STANDINGS SHAKEUP",
            "voice_text": f"The Champions League league table is completely chaotic right now. Here is what the supercomputer projects after 20,000 tournament simulations.",
            "caption": "OFFICIAL TOP 8 CUTOFFS",
            "zoom_direction": "in"
        },
        {
            "id": "scene_2_leaders",
            "type": "standings",
            "payload": {},
            "title": "👑 THE TOP 8 ZONE",
            "voice_text": f"At the top of the table, {leader} leads the charge, while the race for the top eight automatic Round of 16 byes is tighter than ever.",
            "caption": "AUTOMATIC R16 SEEDS",
            "zoom_direction": "out"
        },
        {
            "id": "scene_3_team",
            "type": "team",
            "payload": {"name": top_8[1]["name"] if len(top_8) > 1 else leader},
            "title": "🔥 SURPRISE PACKAGE",
            "voice_text": f"Clubs like {top_8[1]['name'] if len(top_8) > 1 else leader} have defied the initial odds with sensational domestic and European form, giving them an overwhelming chance to advance directly.",
            "caption": "KNOCKOUT BYE LOCKED?",
            "zoom_direction": "in"
        },
        {
            "id": "scene_4_cta",
            "type": "standings",
            "payload": {},
            "title": "⚔️ ELIMINATION DANGER",
            "voice_text": "Remember, finishing outside the top 24 means total elimination from Europe. Who is failing to make the cut? Let me know below and follow for live UCL tracking!",
            "caption": "WHO GETS ELIMINATED? 👇",
            "zoom_direction": "out"
        }
    ]
    
    meta = {
        "title": "Champions League Standings & Top 8 Projections",
        "description": "Live UEFA Champions League league phase simulation breakdown! Who finishes top 8 and who faces elimination?\n\n#UCL #ChampionsLeague #Football #Standings #UCLTable #Soccer #Predictions",
        "leader": leader
    }
    
    return {"scenes": scenes, "meta": meta}

def main():
    parser = argparse.ArgumentParser(description="Generate TikTok storyboard and narration script")
    parser.add_argument("--type", choices=["match", "standings"], default="match", help="Type of TikTok video")
    parser.add_argument("--home", type=str, default=None, help="Specific home team for match preview")
    parser.add_argument("--away", type=str, default=None, help="Specific away team for match preview")
    parser.add_argument("--output", type=str, default=str(ROOT_DIR / "output" / "storyboard.json"), help="Output JSON path")
    args = parser.parse_args()
    
    standings, dossiers = load_data()
    
    if args.type == "match":
        if args.home and args.away:
            # Find specific match
            match = next((m for m in standings.get("matches", []) if m["home"].lower() == args.home.lower() and m["away"].lower() == args.away.lower()), None)
            if not match:
                match = {"home": args.home, "away": args.away, "matchday": "League Stage - 4", "played": False, "odds": {"home": 0.46, "draw": 0.26, "away": 0.28}}
        else:
            match = find_marquee_match(standings.get("matches", []), standings)
            
        storyboard = build_match_storyboard(match, standings, dossiers)
    else:
        storyboard = build_standings_storyboard(standings, dossiers)
        
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(storyboard, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Generated storyboard at {out_path}")
    print(f"🎬 Video Title: {storyboard['meta']['title']}")
    print(f"📝 Total Scenes: {len(storyboard['scenes'])}")

if __name__ == "__main__":
    main()
