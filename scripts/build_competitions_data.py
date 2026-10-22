import json

COMPETITIONS = {
    "ucl": {
        "id": "ucl",
        "name": "UEFA Champions League",
        "badge": "🏆",
        "tagline": "Europe's Premier Club Competition",
        "format": "36-Club Swiss Model (8 Matchdays) · Top 8 to Round of 16 · 9-24 to Play-offs",
        "matchdays": 8
    },
    "uel": {
        "id": "uel",
        "name": "UEFA Europa League",
        "badge": "🥈",
        "tagline": "The Battle for European Glory & Champions League Direct Qualification",
        "format": "36-Club Swiss Model (8 Matchdays) · Top 8 to Round of 16 · 9-24 to Play-offs",
        "matchdays": 8,
        "table": [
            {"rank": 1, "name": "Tottenham Hotspur", "country": "ENG", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "p": 3, "w": 3, "d": 0, "l": 0, "gf": 8, "ga": 1, "gd": 7, "pts": 9, "prob_top8": 0.94, "prob_top24": 1.0, "status": "Leader"},
            {"rank": 2, "name": "Lazio", "country": "ITA", "flag": "🇮🇹", "p": 3, "w": 3, "d": 0, "l": 0, "gf": 9, "ga": 1, "gd": 8, "pts": 9, "prob_top8": 0.92, "prob_top24": 1.0, "status": "Top 8 Track"},
            {"rank": 3, "name": "Athletic Club", "country": "ESP", "flag": "🇪🇸", "p": 3, "w": 2, "d": 1, "l": 0, "gf": 6, "ga": 1, "gd": 5, "pts": 7, "prob_top8": 0.86, "prob_top24": 0.99, "status": "Top 8 Track"},
            {"rank": 4, "name": "Anderlecht", "country": "BEL", "flag": "🇧🇪", "p": 3, "w": 2, "d": 1, "l": 0, "gf": 6, "ga": 2, "gd": 4, "pts": 7, "prob_top8": 0.76, "prob_top24": 0.98, "status": "Top 8 Track"},
            {"rank": 5, "name": "Ajax", "country": "NED", "flag": "🇳🇱", "p": 3, "w": 2, "d": 1, "l": 0, "gf": 8, "ga": 1, "gd": 7, "pts": 7, "prob_top8": 0.74, "prob_top24": 0.98, "status": "Top 8 Track"},
            {"rank": 6, "name": "Galatasaray", "country": "TUR", "flag": "🇹🇷", "p": 3, "w": 2, "d": 1, "l": 0, "gf": 9, "ga": 6, "gd": 3, "pts": 7, "prob_top8": 0.71, "prob_top24": 0.97, "status": "Top 8 Track"},
            {"rank": 7, "name": "Eintracht Frankfurt", "country": "GER", "flag": "🇩🇪", "p": 3, "w": 2, "d": 1, "l": 0, "gf": 7, "ga": 4, "gd": 3, "pts": 7, "prob_top8": 0.69, "prob_top24": 0.96, "status": "Top 8 Track"},
            {"rank": 8, "name": "Midtjylland", "country": "DEN", "flag": "🇩🇰", "p": 3, "w": 2, "d": 1, "l": 0, "gf": 4, "ga": 1, "gd": 3, "pts": 7, "prob_top8": 0.64, "prob_top24": 0.95, "status": "Cutoff Spot"},
            {"rank": 9, "name": "Bodø/Glimt", "country": "NOR", "flag": "🇳🇴", "p": 3, "w": 2, "d": 1, "l": 0, "gf": 5, "ga": 3, "gd": 2, "pts": 7, "prob_top8": 0.58, "prob_top24": 0.94, "status": "Play-off Seed"},
            {"rank": 10, "name": "Lyon", "country": "FRA", "flag": "🇫🇷", "p": 3, "w": 2, "d": 0, "l": 1, "gf": 6, "ga": 2, "gd": 4, "pts": 6, "prob_top8": 0.52, "prob_top24": 0.93, "status": "Play-off Seed"},
            {"rank": 11, "name": "Rangers", "country": "SCO", "flag": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "p": 3, "w": 2, "d": 0, "l": 1, "gf": 6, "ga": 4, "gd": 2, "pts": 6, "prob_top8": 0.46, "prob_top24": 0.91, "status": "Play-off Seed"},
            {"rank": 12, "name": "Olympiacos", "country": "GRE", "flag": "🇬🇷", "p": 3, "w": 2, "d": 0, "l": 1, "gf": 4, "ga": 2, "gd": 2, "pts": 6, "prob_top8": 0.44, "prob_top24": 0.90, "status": "Play-off Seed"},
            {"rank": 13, "name": "FCSB", "country": "ROU", "flag": "🇷🇴", "p": 3, "w": 2, "d": 0, "l": 1, "gf": 5, "ga": 5, "gd": 0, "pts": 6, "prob_top8": 0.38, "prob_top24": 0.88, "status": "Play-off Seed"},
            {"rank": 14, "name": "Slavia Praha", "country": "CZE", "flag": "🇨🇿", "p": 3, "w": 1, "d": 1, "l": 1, "gf": 3, "ga": 2, "gd": 1, "pts": 4, "prob_top8": 0.28, "prob_top24": 0.84, "status": "In Play-off"},
            {"rank": 15, "name": "Real Sociedad", "country": "ESP", "flag": "🇪🇸", "p": 3, "w": 1, "d": 1, "l": 1, "gf": 3, "ga": 3, "gd": 0, "pts": 4, "prob_top8": 0.26, "prob_top24": 0.82, "status": "In Play-off"},
            {"rank": 16, "name": "Hoffenheim", "country": "GER", "flag": "🇩🇪", "p": 3, "w": 1, "d": 1, "l": 1, "gf": 4, "ga": 4, "gd": 0, "pts": 4, "prob_top8": 0.24, "prob_top24": 0.80, "status": "In Play-off"},
            {"rank": 17, "name": "Roma", "country": "ITA", "flag": "🇮🇹", "p": 3, "w": 1, "d": 1, "l": 1, "gf": 2, "ga": 2, "gd": 0, "pts": 4, "prob_top8": 0.22, "prob_top24": 0.79, "status": "In Play-off"},
            {"rank": 18, "name": "Fenerbahce", "country": "TUR", "flag": "🇹🇷", "p": 3, "w": 1, "d": 1, "l": 1, "gf": 4, "ga": 5, "gd": -1, "pts": 4, "prob_top8": 0.18, "prob_top24": 0.75, "status": "In Play-off"},
            {"rank": 19, "name": "Porto", "country": "POR", "flag": "🇵🇹", "p": 3, "w": 1, "d": 1, "l": 1, "gf": 7, "ga": 6, "gd": 1, "pts": 4, "prob_top8": 0.16, "prob_top24": 0.72, "status": "In Play-off"},
            {"rank": 20, "name": "AZ Alkmaar", "country": "NED", "flag": "🇳🇱", "p": 3, "w": 1, "d": 0, "l": 2, "gf": 3, "ga": 5, "gd": -2, "pts": 3, "prob_top8": 0.11, "prob_top24": 0.64, "status": "Bubble"},
            {"rank": 21, "name": "Malmö FF", "country": "SWE", "flag": "🇸🇪", "p": 3, "w": 1, "d": 0, "l": 2, "gf": 2, "ga": 4, "gd": -2, "pts": 3, "prob_top8": 0.08, "prob_top24": 0.59, "status": "Bubble"},
            {"rank": 22, "name": "Braga", "country": "POR", "flag": "🇵🇹", "p": 3, "w": 1, "d": 0, "l": 2, "gf": 3, "ga": 6, "gd": -3, "pts": 3, "prob_top8": 0.07, "prob_top24": 0.57, "status": "Bubble"},
            {"rank": 23, "name": "Manchester United", "country": "ENG", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "p": 3, "w": 0, "d": 3, "l": 0, "gf": 5, "ga": 5, "gd": 0, "pts": 3, "prob_top8": 0.14, "prob_top24": 0.70, "status": "Bubble"},
            {"rank": 24, "name": "Elfsborg", "country": "SWE", "flag": "🇸🇪", "p": 3, "w": 1, "d": 0, "l": 2, "gf": 5, "ga": 6, "gd": -1, "pts": 3, "prob_top8": 0.05, "prob_top24": 0.50, "status": "Last Cutoff"}
        ],
        "key_fixtures": [
            {"home": "Tottenham Hotspur", "away": "Roma", "date": "Nov 28, 2026", "prob_home": 0.56, "prob_draw": 0.23, "prob_away": 0.21},
            {"home": "Manchester United", "away": "Bodø/Glimt", "date": "Nov 28, 2026", "prob_home": 0.62, "prob_draw": 0.22, "prob_away": 0.16},
            {"home": "Athletic Club", "away": "Elfsborg", "date": "Nov 28, 2026", "prob_home": 0.78, "prob_draw": 0.14, "prob_away": 0.08},
            {"home": "Lazio", "away": "Ludogorets", "date": "Nov 28, 2026", "prob_home": 0.75, "prob_draw": 0.16, "prob_away": 0.09}
        ]
    },
    "uecl": {
        "id": "uecl",
        "name": "UEFA Conference League",
        "badge": "🥉",
        "tagline": "The Modern Tournament of European Dreams & Diverse Continental Drama",
        "format": "36-Club Swiss Model (6 Matchdays) · Top 8 to Round of 16 · 9-24 to Play-offs",
        "matchdays": 6,
        "table": [
            {"rank": 1, "name": "Chelsea", "country": "ENG", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "p": 2, "w": 2, "d": 0, "l": 0, "gf": 8, "ga": 3, "gd": 5, "pts": 6, "prob_top8": 0.98, "prob_top24": 1.0, "status": "Heavy Favorite"},
            {"rank": 2, "name": "Fiorentina", "country": "ITA", "flag": "🇮🇹", "p": 2, "w": 2, "d": 0, "l": 0, "gf": 6, "ga": 2, "gd": 4, "pts": 6, "prob_top8": 0.94, "prob_top24": 1.0, "status": "Finalist Pedigree"},
            {"rank": 3, "name": "Legia Warsaw", "country": "POL", "flag": "🇵🇱", "p": 2, "w": 2, "d": 0, "l": 0, "gf": 4, "ga": 0, "gd": 4, "pts": 6, "prob_top8": 0.88, "prob_top24": 0.99, "status": "Top 8 Track"},
            {"rank": 4, "name": "Lugano", "country": "SUI", "flag": "🇨🇭", "p": 2, "w": 2, "d": 0, "l": 0, "gf": 4, "ga": 0, "gd": 4, "pts": 6, "prob_top8": 0.85, "prob_top24": 0.99, "status": "Top 8 Track"},
            {"rank": 5, "name": "Vitória de Guimarães", "country": "POR", "flag": "🇵🇹", "p": 2, "w": 2, "d": 0, "l": 0, "gf": 5, "ga": 2, "gd": 3, "pts": 6, "prob_top8": 0.84, "prob_top24": 0.98, "status": "Top 8 Track"},
            {"rank": 6, "name": "Heart of Midlothian", "country": "SCO", "flag": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "p": 2, "w": 2, "d": 0, "l": 0, "gf": 4, "ga": 1, "gd": 3, "pts": 6, "prob_top8": 0.81, "prob_top24": 0.98, "status": "Top 8 Track"},
            {"rank": 7, "name": "Jagiellonia Białystok", "country": "POL", "flag": "🇵🇱", "p": 2, "w": 2, "d": 0, "l": 0, "gf": 4, "ga": 1, "gd": 3, "pts": 6, "prob_top8": 0.79, "prob_top24": 0.97, "status": "Top 8 Track"},
            {"rank": 8, "name": "Rapid Wien", "country": "AUT", "flag": "🇦🇹", "p": 2, "w": 2, "d": 0, "l": 0, "gf": 3, "ga": 1, "gd": 2, "pts": 6, "prob_top8": 0.76, "prob_top24": 0.96, "status": "Cutoff Spot"},
            {"rank": 9, "name": "Gent", "country": "BEL", "flag": "🇧🇪", "p": 2, "w": 1, "d": 0, "l": 1, "gf": 4, "ga": 5, "gd": -1, "pts": 3, "prob_top8": 0.55, "prob_top24": 0.91, "status": "Play-off Seed"},
            {"rank": 10, "name": "Panathinaikos", "country": "GRE", "flag": "🇬🇷", "p": 2, "w": 0, "d": 1, "l": 1, "gf": 2, "ga": 5, "gd": -3, "pts": 1, "prob_top8": 0.35, "prob_top24": 0.80, "status": "Contender"},
            {"rank": 11, "name": "Real Betis", "country": "ESP", "flag": "🇪🇸", "p": 2, "w": 0, "d": 1, "l": 1, "gf": 1, "ga": 2, "gd": -1, "pts": 1, "prob_top8": 0.42, "prob_top24": 0.85, "status": "Contender"},
            {"rank": 12, "name": "Copenhagen", "country": "DEN", "flag": "🇩🇰", "p": 2, "w": 0, "d": 1, "l": 1, "gf": 2, "ga": 3, "gd": -1, "pts": 1, "prob_top8": 0.38, "prob_top24": 0.82, "status": "Contender"}
        ],
        "key_fixtures": [
            {"home": "Chelsea", "away": "Noah", "date": "Nov 7, 2026", "prob_home": 0.92, "prob_draw": 0.06, "prob_away": 0.02},
            {"home": "APOEL", "away": "Fiorentina", "date": "Nov 7, 2026", "prob_home": 0.18, "prob_draw": 0.24, "prob_away": 0.58},
            {"home": "Real Betis", "away": "Celje", "date": "Nov 7, 2026", "prob_home": 0.82, "prob_draw": 0.12, "prob_away": 0.06}
        ]
    }
}

with open("data/competitions_data.json", "w", encoding="utf-8") as f:
    json.dump(COMPETITIONS, f, indent=2, ensure_ascii=False)

print("Generated data/competitions_data.json successfully!")
