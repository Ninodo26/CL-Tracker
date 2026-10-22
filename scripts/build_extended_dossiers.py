import json

EXTENDED_DOSSIERS = {
    "Real Madrid": {
        "league": "La Liga",
        "manager": "José Mourinho",
        "formation": "4-3-3 Pragmatic Transition",
        "why_good": "Real Madrid combine the world's most devastating transition trident with ruthless tournament maturity. Under José Mourinho, Los Blancos have structured a bulletproof mid-block that lures opponents into committing bodies forward before unleashing Vinícius Júnior and Kylian Mbappé into yawning acres of space behind high defensive lines.\n\nIn possession, the midfield balances tactical discipline with elite technical composure. Federico Valverde and Aurélien Tchouaméni form a physically suffocating defensive screen, while Jude Bellingham operates as a dynamic hybrid box-to-box facilitator, timing his late box arrivals to devastating effect. Full-backs tuck into a rigid three-man rest defense to eliminate opponent counter-attacks before they start.\n\nWhat sets Madrid apart on European nights is their unprecedented psychological composure. Regardless of scoreboard deficits or territorial pressure, Madrid's players exhibit an unflappable belief in high-leverage moments, consistently finding game-breaking individual magic when ties tighten into the final 20 minutes.",
        "key_strengths": [
            "Devastating vertical transition speed with Vinícius Jr and Kylian Mbappé",
            "Suffocating athletic midfield dominance and late box arriving runs from Jude Bellingham",
            "Unrivaled tournament psychology, clutch goalscoring, and European pedigree"
        ],
        "known_vulnerabilities": [
            "Vulnerable to sustained low-block frustration when opponents refuse to concede space behind",
            "Full-back depth tested against elite 1v1 wingers when Dani Carvajal is sidelined"
        ],
        "key_players": [
            {"name": "Vinícius Júnior", "role": "World-Class Left-Wing Isolator & Dribbler", "impact": "Averages 4.2 completed take-ons per 90 and commands double-teams that collapse entire defensive structures."},
            {"name": "Kylian Mbappé", "role": "Elite Vertical Striker & Box Finisher", "impact": "Generates 1.15 xG+xA per 90, terrorizing center-backs with unmatched burst and ruthless near-post finishing."},
            {"name": "Jude Bellingham", "role": "Box-to-Box Midfield Talisman", "impact": "Wins 68% of his ground duels while leading Madrid in progressive third entries and clutch match-winning interventions."},
            {"name": "Federico Valverde", "role": "Tactical Engine & Rest-Defense Anchor", "impact": "Tireless runner who covers 11.8 km per 90, shutting down wide transitions and possessing a lethal long-range shooting cannon."}
        ],
        "fan_perspective": "The Santiago Bernabéu demands nothing less than the trophy. Under European floodlights, Madridistas view the Champions League not merely as a tournament, but as their sacred birthright. Following the arrival of Mbappé and the return of Mourinho, expectations are sky-high for a record-extending European coronation.\n\nHowever, supporters remain vigilant regarding defensive consistency and the midfield's creative balance following the retirement of legendary playmakers. The atmosphere at the Bernabéu is electric, with fans confident that this star-studded squad has the firepower to blow past any heavyweight on the continent.",
        "needs_to_advance": "With 9 points banked from their first three fixtures, Real Madrid need approximately 6 to 7 more points from their remaining 5 fixtures to guarantee a top-8 automatic bye to the Round of 16. Winning their home clashes against European rivals will cement a top-4 tournament seeding."
    },
    "Paris Saint-Germain": {
        "league": "Ligue 1",
        "manager": "Luis Enrique",
        "formation": "4-3-3 High Possession Overload",
        "why_good": "Luis Enrique has completely transformed Paris Saint-Germain into a synchronized, unselfish collective pressing machine. Departing from the superstar-centric models of past eras, this PSG side suffocates opponents with 65%+ possession, extreme counter-pressing within 5 seconds of ball turnover, and blistering wing overloads.\n\nVitinha operates as the heartbeat of the team in the deep-lying pivot, distributing with 94%+ pass accuracy while resisting the most aggressive pressing schemes. Flanking him, Warren Zaïre-Emery and João Neves provide relentless ground coverage, repeatedly winning secondary balls and recycling possession before opponents can exit their defensive third.\n\nOut wide, PSG isolate full-backs through Ousmane Dembélé and Bradley Barcola, who lead Europe in 1v1 take-on volume. Combined with Achraf Hakimi's devastating overlapping and underlapping runs, PSG create overwhelming numerical superiorities in the half-spaces that systematically dismantle low blocks.",
        "key_strengths": [
            "Territorial strangulation and relentless 5-second counter-pressing traps",
            "Elite wide 1v1 dribbling with Ousmane Dembélé and Bradley Barcola",
            "Fluid midfield tempo control through Vitinha and João Neves"
        ],
        "known_vulnerabilities": [
            "Susceptible to rapid diagonal counter-attacks when both full-backs are caught high upfield",
            "Lack of a traditional aerially dominant target striker against packed penalty boxes"
        ],
        "key_players": [
            {"name": "Ousmane Dembélé", "role": "Primary Chance Creator & Wing Magician", "impact": "Leads all of Europe in expected assists (xA) and shot-creating actions from wide isolations."},
            {"name": "Bradley Barcola", "role": "Direct Transitional Left Winger", "impact": "Blistering acceleration allows him to exploit the space between opposing right-backs and center-backs with lethal finishing."},
            {"name": "Vitinha", "role": "Metronomic Midfield Conductor", "impact": "Averages 92 passes per match at 94.2% completion, dictating European match rhythm with surgical precision."},
            {"name": "Achraf Hakimi", "role": "Explosive Overlapping Full-Back", "impact": "Functions essentially as a second winger, generating 5.2 crosses and cutbacks into the box per match."}
        ],
        "fan_perspective": "The atmosphere at the Parc des Princes has shifted from anxious expectation to genuine pride. Supporters embrace this hungry, youthful, and tactically cohesive side far more than the star-heavy squads of years past. Having taken 9 points from their opening 3 matchdays with +9 goal differential, the Collectif Ultras Paris believe this is the most complete team PSG have ever fielded.\n\nFans acknowledge that defensive composure in hostile away environments will define their destiny, but the feeling across Paris is that PSG fear nobody in Europe.",
        "needs_to_advance": "Sitting in 1st place on 9 points, PSG have virtually locked up playoff survival. To secure the coveted automatic Round of 16 top-8 bye and avoid the grueling two-legged playoff, they need roughly 6 points from their remaining 5 ties, with home clashes offering the perfect path."
    },
    "Liverpool": {
        "league": "Premier League",
        "manager": "Andoni Iraola",
        "formation": "4-2-3-1 Heavy-Metal Press",
        "why_good": "Liverpool play with a ferocity and directness that overwhelms opposing buildup structures. Under Andoni Iraola, the Reds have elevated their trademark pressing intensity into a hyper-synchronized trap, forcing turnovers inside the opposition half at Europe's highest rate.\n\nRyan Gravenberch and Alexis Mac Allister form an exceptionally balanced double pivot—Gravenberch provides line-breaking ball carries and tackling range, while Mac Allister distributes surgically under pressure. Behind them, Virgil van Dijk commands the backline with peerless aerial supremacy and 60-yard diagonal switches that instantly unlock wide spaces.\n\nIn the final third, Mohamed Salah remains Europe's most consistent offensive dynamo, cutting inside onto his favored left foot while Luis Díaz stretches defenses with explosive direct running. The combination of rapid transitional pace and Anfield's suffocating energy makes Liverpool a nightmare opponent.",
        "key_strengths": [
            "Europe's most aggressive attacking-third turnover generator",
            "Virgil van Dijk's aerial dominance and long-range diagonal distribution",
            "Mohamed Salah's world-class output in goals, assists, and progressive play"
        ],
        "known_vulnerabilities": [
            "High defensive line leaves space over the top when midfielders fail to pressure the passer",
            "Goalkeeping depth under scrutiny when Alisson Becker experiences muscle fatigue"
        ],
        "key_players": [
            {"name": "Mohamed Salah", "role": "Right-Wing Talisman & Elite Scorer", "impact": "Directly involved in over 60% of Liverpool's European goals through lethal scoring and pinpoint cutbacks."},
            {"name": "Virgil van Dijk", "role": "Colossal Center-Back & On-Pitch Captain", "impact": "Wins 78% of aerial duels and neutralizes opposing counter-attacks with unmatched spatial awareness."},
            {"name": "Ryan Gravenberch", "role": "Dynamic Line-Breaking Pivot", "impact": "Boasts an 89% duel success rate while driving the ball 25+ meters through the center of the pitch."},
            {"name": "Luis Díaz", "role": "Electric 1v1 Left-Wing Dribbler", "impact": "Relentless pressing hound who forces opposing full-backs into panic clearances and errors."}
        ],
        "fan_perspective": "European nights under the Anfield lights remain unmatched in world football. The Kop roars with the conviction that six European Cups instill, and supporters have fully bought into Iraola's relentless tactical energy.\n\nAfter storming to 9 points with impressive away victories, fans feel this squad is primed for a deep run to the final. The primary anxiety among supporters is squad fatigue during the congested winter schedule, but the belief on Merseyside is absolute.",
        "needs_to_advance": "With 9 points banked and strong goal difference, Liverpool require 6 to 7 more points from fixtures against Spanish and German opposition to guarantee an automatic top-8 finish and skip the playoff round entirely."
    },
    "Manchester City": {
        "league": "Premier League",
        "manager": "Enzo Maresca",
        "formation": "3-2-4-1 Positional Mastery",
        "why_good": "Manchester City operate like an algorithmic machine, wearing opponents down through calculated positional dominance. Under Enzo Maresca, City have retained their signature rest-defense and 3-2-4-1 buildup structure while infusing quicker vertical releases into the penalty box for Erling Haaland.\n\nJoško Gvardiol inverts from left-back to join Mateo Kovačić in the central double pivot, creating an overload that forces opposing midfields into narrow blocks. This opens up vast channels for Kevin De Bruyne and Phil Foden to operate between the lines, sliding defense-splitting through-balls into the channels.\n\nAt the focal point is Erling Haaland—the sport's most lethal penalty-box predator. Haaland's physical presence pins both opposing center-backs, opening space for Bernardo Silva and Jérémy Doku to manipulate 1v1 match-ups on the perimeter.",
        "key_strengths": [
            "Unrivaled territorial control and numerical overloads in the half-spaces",
            "Erling Haaland's generational box finishing and physical gravity",
            "Defensive organization that suppresses opponent shots inside the penalty box"
        ],
        "known_vulnerabilities": [
            "Absence of Rodri removes their primary defensive transition insurance policy",
            "Susceptible to rapid counter-attacks if possession is surrendered in central areas"
        ],
        "key_players": [
            {"name": "Erling Haaland", "role": "Generational Goalscoring Machine", "impact": "Averages 1.28 goals per 90 in Champions League history with unmatched aerial conversion."},
            {"name": "Kevin De Bruyne", "role": "Master Playmaker & Visionary", "impact": "Averages 3.8 key passes per game with the world's most dangerous crossing delivery."},
            {"name": "Phil Foden", "role": "Half-Space Magician & Dribbler", "impact": "Flourishes in tight central pockets with lightning turns and lethal edge-of-box shooting."},
            {"name": "Joško Gvardiol", "role": "Inverted Left-Back & Progressive Passer", "impact": "Provides defensive power combined with elite ball-carrying and long-range shooting threat."}
        ],
        "fan_perspective": "City supporters have grown accustomed to European supremacy following their historic Istanbul triumph. Under Maresca, fans expect the club to challenge for the title every single season. While the loss of Rodri to injury created mid-season nervousness, the Etihad faithful believe their firepower is simply too formidable for any defense over 90 minutes.",
        "needs_to_advance": "Holding 7 points, Manchester City are firmly on course. They need roughly 8 points from their final 5 fixtures to seal an automatic top-8 seed and secure home-field advantage in the Round of 16."
    },
    "Barcelona": {
        "league": "La Liga",
        "manager": "Hansi Flick",
        "formation": "4-2-3-1 Vertical Heavy-Metal",
        "why_good": "Hansi Flick has revitalized Barcelona with an aggressive, vertical German blueprint that has taken Europe by storm. Gone are the days of sterile lateral possession—Flick's Barça attacks with explosive verticality, utilizing an audacious high defensive line that suffocates opposing attacks in their own half.\n\nAt the center of this revolution is 17-year-old phenom Lamine Yamal and a regenerated Raphinha. Yamal's supernatural spatial awareness and curling deliveries from the right flank create instant panic, while Raphinha leads Europe in sprints, pressing actions, and transition goals.\n\nMarc Casadó and Pedri form a brilliant double pivot that combines tactical intelligence with laser-sharp forward passing. Ahead of them, Robert Lewandowski continues to execute clinical box movement, feasting on the endless supply of crosses and cutbacks generated by Yamal and Balde.",
        "key_strengths": [
            "Relentless forward momentum and overwhelming chance-creation volume",
            "Lamine Yamal's game-breaking 1v1 dribbling and visionary passing",
            "Raphinha's explosive transitional pressing and clinical box conversion"
        ],
        "known_vulnerabilities": [
            "Extremely high defensive line is vulnerable to perfectly timed long balls from deep",
            "Goalkeeping adjustments following Marc-André ter Stegen's extended injury absence"
        ],
        "key_players": [
            {"name": "Lamine Yamal", "role": "Generational Right-Wing Creator", "impact": "Completed 14 key dribbles and averages 3.1 chances created per 90, drawing triple-coverage."},
            {"name": "Raphinha", "role": "Pressing Monster & Left-Wing Finisher", "impact": "Directly involved in 7 European goals already, combining blistering speed with work-rate."},
            {"name": "Pedri", "role": "Press-Resistant Midfield Maestro", "impact": "Controls game tempo with 91% pass accuracy and exceptional disguised line-breaking passes."},
            {"name": "Robert Lewandowski", "role": "Master Striker & Box Predator", "impact": "Veteran scoring acumen ensures half-chances are ruthlessly dispatched inside the 6-yard box."}
        ],
        "fan_perspective": "Culés are walking on air. The Montjuïc stadium is buzzing with the feeling that the golden era of La Masia has returned with an added dose of physical intensity. Watching Lamine Yamal dismantle European powerhouses alongside Raphinha has restored Barcelona's pride on the continental stage.\n\nFans know that Flick's daring high line brings heart-stopping moments against pacey strikers, but the attacking joy has made Barcelona the most thrilling watch in Europe.",
        "needs_to_advance": "With 6 points and a soaring +7 goal differential, Barcelona need 9 to 10 more points from their remaining matches to punch their ticket straight to the Round of 16."
    },
    "Bayern Munich": {
        "league": "Bundesliga",
        "manager": "Vincent Kompany",
        "formation": "4-2-3-1 Dominant Front-Foot",
        "why_good": "Vincent Kompany has brought relentless forward energy back to the Allianz Arena. Bayern attack in waves, utilizing an aggressive 3-1-5-1 shape in possession where Joshua Kimmich orchestrates from deep while full-backs push high to pin opposing wide players.\n\nHarry Kane operates as the world's most complete center-forward—dropping deep into the number 10 pocket to pick out surging runs from Michael Olise, Serge Gnabry, and Jamal Musiala. This dynamic creates an impossible dilemma for opposing central defenders: follow Kane and vacate the center, or drop off and allow Kane to shoot from 25 yards.\n\nOut wide, Michael Olise has added a dazzling new dimension with his ability to beat defenders inside and outside, while Musiala's snake-like dribbling through crowded penalty areas unlocks the stubbornest low blocks in Europe.",
        "key_strengths": [
            "Harry Kane's peerless playmaking vision combined with world-class finishing",
            "Michael Olise and Jamal Musiala's unstoppable half-space combinations",
            "Physical dominance on offensive set-pieces and counter-pressing recoveries"
        ],
        "known_vulnerabilities": [
            "Center-backs can be isolated in footraces when opponents break through the initial counter-press",
            "Over-reliance on Joshua Kimmich as the sole tempo controller under heavy pressure"
        ],
        "key_players": [
            {"name": "Harry Kane", "role": "Complete World-Class Center-Forward", "impact": "Leads the competition with 5 goals and a 1.79 G/90 rate, while serving as primary playmaker."},
            {"name": "Jamal Musiala", "role": "Virtuoso Central Attacking Midfielder", "impact": "Averages 5.1 successful dribbles per game, threading passes through impenetrable defenses."},
            {"name": "Michael Olise", "role": "Explosive Right-Wing Playmaker", "impact": "Delivers pinpoint dead-balls and curls dangerous cutbacks from the right half-space."},
            {"name": "Joshua Kimmich", "role": "Deep-Lying Tactical Orchestrator", "impact": "Directs possession with 100+ touches per match and pinpoint diagonal switches."}
        ],
        "fan_perspective": "Bayern supporters demand European supremacy every spring. After undergoing tactical adjustments, fans have rallied behind Kompany's positive, high-intensity attacking football. Harry Kane's goalscoring exploits have made him an instant Allianz Arena icon.\n\nSupporters remain demanding about defensive resilience against top-tier transition sides like Real Madrid and Manchester City, but the belief is that Bayern have the firepower to outscore anyone.",
        "needs_to_advance": "On 6 points, Bayern are well on pace. Winning three of their remaining 5 fixtures (reaching 15-16 points) will guarantee an automatic Round of 16 bye."
    },
    "Arsenal": {
        "league": "Premier League",
        "manager": "Mikel Arteta",
        "formation": "4-3-3 Complete Control",
        "why_good": "Arsenal boast Europe's most suffocating defensive foundation. Under Mikel Arteta, the Gunners have assembled a near-impenetrable defensive wall anchored by William Saliba and Gabriel Magalhães, backed by David Raya's elite aerial command and sweeping range.\n\nIn midfield, Declan Rice provides extraordinary ground coverage and ball recoveries, allowing Martin Ødegaard and Bukayo Saka to operate with complete creative freedom on the right flank. Arsenal's right-sided triangle of White, Ødegaard, and Saka is one of the most rehearsed and devastating offensive units in modern football.\n\nFurthermore, Arsenal are the undisputed kings of set-pieces. Set-piece coach Nicolas Jover has turned every corner kick and wide free-kick into a high-percentage scoring opportunity through ingenious blocking schemes and Gabriel's aerial dominance.",
        "key_strengths": [
            "Europe's most disciplined and physically commanding central defense (Saliba & Gabriel)",
            "World's most lethal set-piece routines and near-post corner deliveries",
            "Bukayo Saka's reliable 1v1 creation and pinpoint crossing consistency"
        ],
        "known_vulnerabilities": [
            "Can lack central vertical penetration when Martin Ødegaard is heavily man-marked",
            "Reluctance to take early transition risks can allow defenses to reset into low blocks"
        ],
        "key_players": [
            {"name": "Bukayo Saka", "role": "World-Class Right Winger & Creator", "impact": "Averages 3.0 chances created per 90 and delivers pinpoint crosses to the back post."},
            {"name": "William Saliba", "role": "Flawless Central Defender", "impact": "Has not been dribbled past in 12 consecutive European matches, dominating ground duels."},
            {"name": "Declan Rice", "role": "Powerhouse Midfield Destroyer & Ball Carrier", "impact": "Wins 74% of loose ball duels and provides dangerous out-swinging corner deliveries."},
            {"name": "David Raya", "role": "Sweeper-Keeper & Golden Glove Leader", "impact": "Maintains a 91.7% save percentage with elite penalty-box command."}
        ],
        "fan_perspective": "The Emirates Stadium is rocking with genuine European ambition. Arsenal supporters feel this team is finally mature enough to conquer the Champions League after years of rebuilding. The defensive solidity gives fans tremendous confidence that Arsenal will never be blown away in knockout ties.\n\nThe only debate in North London pubs is whether the attack possesses the ruthless killer instinct required to dismantle European royalty, but confidence is at an all-time high.",
        "needs_to_advance": "Holding 7 points without conceding a goal from open play, Arsenal need roughly 8 more points from 5 matches to lock in an automatic top-8 seed."
    },
    "Inter": {
        "league": "Serie A",
        "manager": "Simone Inzaghi",
        "formation": "3-5-2 Fluid Rotational System",
        "why_good": "Inter play the most tactically sophisticated 3-5-2 system in global football. Simone Inzaghi has perfected a style characterized by fluid interchanging roles: central defenders Alessandro Bastoni and Benjamin Pavard regularly overlap into the attacking third, creating bewildering numerical advantages that confound standard defensive structures.\n\nHakan Çalhanoğlu is the team's deep-lying quarterback, directing traffic under immense pressure and launching 50-yard laser diagonals to wing-backs Federico Dimarco and Denzel Dumfries. Dimarco's left-footed crossing is arguably the finest in Europe.\n\nUp front, Lautaro Martínez and Marcus Thuram form a telepathic strike partnership. Lautaro's pressing intensity, close-control dribbling, and ruthless penalty-box instincts complement Thuram's explosive pace and physical channel running, giving Inter the ability to dominate via possession or lethal counter-attacks.",
        "key_strengths": [
            "World's most fluid overlapping center-back system through Alessandro Bastoni",
            "Federico Dimarco's extraordinary left-footed crossing delivery",
            "Lautaro Martínez and Marcus Thuram's lethal two-striker synergy"
        ],
        "known_vulnerabilities": [
            "Space left behind advancing center-backs can be exploited by pacey wingers",
            "Aging squad core can experience physical drop-offs in high-tempo final 20 minutes"
        ],
        "key_players": [
            {"name": "Lautaro Martínez", "role": "Talismanic Striker & Captain", "impact": "Scores in high-pressure moments and leads Inter's forward pressing with relentless determination."},
            {"name": "Hakan Çalhanoğlu", "role": "Master Regista & Set-Piece Specialist", "impact": "Dictates tempo with 93% passing accuracy and converts penalties with a 100% record."},
            {"name": "Federico Dimarco", "role": "Elite Crosser & Left Wing-Back", "impact": "Leads Serie A in open-play crosses and expected assists from wide positions."},
            {"name": "Alessandro Bastoni", "role": "Playmaking Central Defender", "impact": "Advances with the ball into the final third like an attacking midfielder, delivering pinpoint crosses."}
        ],
        "fan_perspective": "The Curva Nord at San Siro expects another march to the European final. Having established domestic dominance, Interisti believe Inzaghi's tactical system is tailor-made for two-legged European knockout ties.\n\nFans take tremendous pride in their defensive identity and tactical maturity, viewing Inter as Italy's undisputed standard-bearer on the European stage.",
        "needs_to_advance": "Sitting on 7 points with two clean sheets, Inter need 8 more points to lock down an automatic Round of 16 bye and bypass the playoff round."
    },
    "Aston Villa": {
        "league": "Premier League",
        "manager": "Unai Emery",
        "formation": "4-2-3-1 High-Line Masterclass",
        "why_good": "Aston Villa are the breakout sensation of the Champions League league phase. Unai Emery—a four-time European trophy winner—has engineered a meticulously coached tactical unit that executes one of football's most disciplined offside traps while devastating opponents in transition.\n\nPau Torres acts as a playmaking center-back, drawing opposing pressers before slicing balls through midfield into Morgan Rogers. Rogers's explosive ball-carrying through central zones shatters defensive lines, feeding Ollie Watkins's intelligent channel runs.\n\nIn goal, Emiliano 'Dibu' Martínez provides world-class shot-stopping and unmatched psychological presence, leading Europe with a 93.3% save rate. Combined with Amadou Onana and Youri Tielemans controlling the midfield engine room, Villa play with the swagger of a seasoned European heavyweight.",
        "key_strengths": [
            "Emiliano Martínez's elite shot-stopping and tournament psychological edge",
            "Morgan Rogers's unstoppable central ball progression and physical acceleration",
            "Unai Emery's peerless European game preparation and tactical flexibility"
        ],
        "known_vulnerabilities": [
            "High offside line requires split-second coordination; any mistiming creates 1v1 chances",
            "Squad rotation challenged by intense Premier League weekend fixtures"
        ],
        "key_players": [
            {"name": "Emiliano Martínez", "role": "World-Class Goalkeeper & Leader", "impact": "Has kept 2 clean sheets with 14 saves, denying opponents high-probability xG chances."},
            {"name": "Morgan Rogers", "role": "Explosive Central Attacking Midfielder", "impact": "Averages 4.4 progressive carries per 90, breaking lines with raw power and vision."},
            {"name": "Ollie Watkins", "role": "Relentless Pressing Striker", "impact": "Scores from half-chances and stretches defenses with tireless diagonal runs."},
            {"name": "Youri Tielemans", "role": "Deep Midfield Distributor", "impact": "Picks out runners with pinpoint 40-yard passes while controlling game tempo."}
        ],
        "fan_perspective": "Villa Park is living a dream that supporters waited over four decades to experience. The roar that greeted Bayern Munich's defeat echoed back to the legendary 1982 European Cup triumph. The Holte End is electric with belief that Unai Emery is building something historic in Birmingham.\n\nSupporters know they are outspending nobody in this tournament, but with Emery's European pedigree, Villa fans fear no badge in Europe.",
        "needs_to_advance": "With a perfect 9 points from 3 matches, Aston Villa have already secured their playoff floor and need just 6 points from their remaining 5 fixtures to seal an automatic Round of 16 bye."
    },
    "Atletico Madrid": {
        "league": "La Liga",
        "manager": "Diego Simeone",
        "formation": "5-3-2 Resilient Block & Strike",
        "why_good": "Diego Simeone's Atletico Madrid combine their legendary defensive grit with exciting new offensive dimensions. The summer additions of Julián Alvarez and Conor Gallagher have added relentless pressing energy and box-to-box dynamism to an already battle-hardened squad.\n\nJan Oblak remains an elite brick wall between the posts, shielded by Giménez and Le Normand in a compact low-to-mid block that denies opponents central shooting angles. In midfield, Rodrigo De Paul and Koke dictate possession while Conor Gallagher disrupts opposition playmakers.\n\nThe key to Atletico's attacking threat is Antoine Griezmann—one of the most intelligent footballers of his generation. Griezmann drops into midfield pockets to orchestrate play before threading killer passes for Julián Alvarez's explosive runs.",
        "key_strengths": [
            "Antoine Griezmann's transcendent tactical intelligence and playmaking vision",
            "Jan Oblak's commanding shot-stopping and experienced backline resilience",
            "Relentless physical duel success and defensive compactness in knockout scenarios"
        ],
        "known_vulnerabilities": [
            "Can become overly passive when holding one-goal leads against high-tempo opponents",
            "Susceptible to wide crosses when wing-backs are pinned back into a flat back five"
        ],
        "key_players": [
            {"name": "Antoine Griezmann", "role": "Genius Playmaker & Forward", "impact": "The brain of the team, leading Atletico in chances created, assists, and defensive recoveries."},
            {"name": "Julián Alvarez", "role": "High-Energy Pressing Striker", "impact": "Combines relentless defensive pressing with clinical edge-of-box shooting accuracy."},
            {"name": "Jan Oblak", "role": "World-Class Shot-Stopper", "impact": "Maintains an 81.8% save percentage and commands the penalty area with authority."},
            {"name": "Rodrigo De Paul", "role": "Midfield Enforcer & Long-Range Passer", "impact": "Brings competitive bite, progressive passing, and aggressive duel-winning presence."}
        ],
        "fan_perspective": "The Metropolitano is an intimidating cauldron of noise and passion. Colchoneros live and die with Simeone's 'cholismo' philosophy. Fans are thrilled by the arrival of Julián Alvarez and believe this squad has the tactical balance to avenge past heartbreaks and bring European glory to the red-and-white half of Madrid.",
        "needs_to_advance": "Holding 6 points, Atletico Madrid are targeting 9 more points from their remaining 5 fixtures to clinch an automatic top-8 seed and avoid the perilous playoff round."
    },
    "Borussia Dortmund": {
        "league": "Bundesliga",
        "manager": "Nuri Şahin",
        "formation": "4-2-3-1 Dynamic Transition",
        "why_good": "Borussia Dortmund possess one of the most explosive transition attacks on the continent. Under Nuri Şahin, BVB look to bait opponents forward before hitting them with blistering wide pace through Jamie Bynoe-Gittens and Donyell Malen.\n\nAt the focal point of the attack is Serhou Guirassy—a physical monster in the penalty box whose hold-up play and aerial prowess bring Dortmund's attacking midfielders into scoring positions. Julian Brandt pulls the creative strings as the number 10, delivering threaded through-balls into the half-spaces.\n\nIn goal, Gregor Kobel is arguably Europe's most athletic shot-stopper, capable of single-handedly keeping Dortmund in matches against high-xG European powerhouses.",
        "key_strengths": [
            "Jamie Bynoe-Gittens's lethal 1v1 dribbling and explosive wing acceleration",
            "Serhou Guirassy's elite box hold-up play and aerial goal threat",
            "Gregor Kobel's heroic shot-stopping ability in high-leverage knockout ties"
        ],
        "known_vulnerabilities": [
            "Defensive transitions can be disjointed when the double pivot is bypassed",
            "Inconsistency in maintaining defensive focus across full 90-minute stretches"
        ],
        "key_players": [
            {"name": "Serhou Guirassy", "role": "Target Striker & Clinical Box Finisher", "impact": "Averages 0.85 goals per 90 and anchors forward attacks with physical strength."},
            {"name": "Jamie Bynoe-Gittens", "role": "Dynamic Left-Wing Dribbler", "impact": "Completed 18 progressive carries, scoring spectacular goals cutting inside onto his right foot."},
            {"name": "Julian Brandt", "role": "Creative Number 10 & Playmaker", "impact": "Leads Dortmund in key passes and switches play with pinpoint vision."},
            {"name": "Gregor Kobel", "role": "Elite Goalkeeper & Leader", "impact": "Averaging 4.2 saves per match with outstanding reflex stops on close-range attempts."}
        ],
        "fan_perspective": "The Yellow Wall at the Westfalenstadion is football's most iconic cathedral. Dortmund supporters carry the pride of last season's run to the Wembley final, and the 80,000-strong crowd expects nothing less than another deep European crusade.\n\nWhile fans scrutinize away consistency, the belief at home is that Dortmund can overwhelm any opponent on earth with the roar of the Südtribüne at their backs.",
        "needs_to_advance": "With 6 points on the board, Dortmund need approximately 9 more points from their remaining fixtures to secure an automatic top-8 bye."
    },
    "Sporting CP": {
        "league": "Primeira Liga",
        "manager": "Rui Borges",
        "formation": "3-4-2-1 High-Intensity Press",
        "why_good": "Sporting CP are Portugal's dominant force and a genuine European dark horse. Built around a fluid, aggressive 3-4-2-1 structure, Sporting overwhelm opponents with high-tempo pressing, synchronized wing-back rotations, and the most devastating striker in Portuguese football history.\n\nViktor Gyökeres is an absolute force of nature—a 6'2\" physical powerhouse who combines the sprint speed of a winger with the finishing ruthlessness of a classic number 9. Gyökeres bullies entire defensive lines on his own, forcing opponents to commit double-coverage and opening space for Trincão and Pedro Gonçalves.\n\nMorten Hjulmand is the tactical general in midfield, winning second balls and orchestrating distribution alongside Hidemasa Morita, while Inácio and Diomande provide athletic recovery pace in defense.",
        "key_strengths": [
            "Viktor Gyökeres's unstoppable physical power, pace, and clinical scoring (4 UCL goals)",
            "Morten Hjulmand's midfield bite, leadership, and pressing coordination",
            "Defensive athleticism and recovery speed of Gonçalo Inácio and Ousmane Diomande"
        ],
        "known_vulnerabilities": [
            "Squad depth is tested when key starters face physical fatigue in congested weeks",
            "High wing-backs leave spaces on the flanks against elite counter-attacking wingers"
        ],
        "key_players": [
            {"name": "Viktor Gyökeres", "role": "Generational Power Striker", "impact": "Has 4 goals in 3 European games, terrorizing defenses with raw power and relentless running."},
            {"name": "Morten Hjulmand", "role": "Midfield Captain & Ball Winner", "impact": "Wins 72% of midfield duels and dictates tempo with pinpoint passing."},
            {"name": "Francisco Trincão", "role": "Inverted Attacking Playmaker", "impact": "Dribbles past defenders with silky close control, generating high-quality half-space entries."},
            {"name": "Gonçalo Inácio", "role": "Ball-Playing Left Center-Back", "impact": "Initiates attacks with 60-yard pinpoint passes and provides crucial aerial clearances."}
        ],
        "fan_perspective": "The Estádio José Alvalade is euphoric. Sporting fans feel they are witnessing a generational team that can challenge the traditional European aristocracy. The love for Gyökeres is bordering on religious devotion across Lisbon.\n\nSupporters believe that with their tactical discipline and Gyökeres firing on all cylinders, no team in the draw wants to face Sporting over two legs.",
        "needs_to_advance": "Sitting on 7 points with a strong +4 goal differential, Sporting need roughly 8 points from their remaining 5 fixtures to lock in a historic automatic top-8 seed."
    },
    "Real Betis": {
        "league": "La Liga",
        "manager": "Manuel Pellegrini",
        "formation": "4-2-3-1 Pure Spanish Elegance",
        "why_good": "Manuel Pellegrini's Real Betis are pure footballing art. Operating in a fluid 4-2-3-1, Los Verdiblancos dominate matches through intricate short-passing triangles, positional rotations, and technical excellence between the lines.\n\nGiovani Lo Celso has enjoyed a sensational campaign as the creative heart of the team, floating between lines with total freedom and unlocking defensive blocks with disguised reverse passes. Alongside him, Pablo Fornals and Abde Ezzalzouli provide contrasting wide threats—Fornals with vision, Abde with blistering 1v1 dribbling.\n\nUp front, young Brazilian striker Vitor Roque provides electric pressing energy and sharp near-post runs, while Marc Roca and Sergi Altimira anchor the midfield with composure and defensive awareness.",
        "key_strengths": [
            "Giovani Lo Celso's transcendent creative form and vision between the lines",
            "Technical short-passing mastery that neutralizes aggressive pressing teams",
            "Pellegrini's calm tournament management and experienced game management"
        ],
        "known_vulnerabilities": [
            "Lack of aerial height in central defense against physical set-piece specialists",
            "Can struggle to convert overwhelming possession dominance into high-volume shots"
        ],
        "key_players": [
            {"name": "Giovani Lo Celso", "role": "Talismanic Number 10 & Playmaker", "impact": "The creative maestro of Betis, leading La Liga in forward passes and goal involvements."},
            {"name": "Vitor Roque", "role": "Dynamic Brazilian Striker", "impact": "Relentless worker who presses backlines and finishes with sharp instincts in the box."},
            {"name": "Abde Ezzalzouli", "role": "Explosive 1v1 Left Winger", "impact": "Averages 4.8 dribbles per match, stretching defenses with raw pace and unpredictability."},
            {"name": "Marc Roca", "role": "Deep Midfield Distributor & Anchor", "impact": "Recycles possession with 90% accuracy and breaks up opposition transitional attacks."}
        ],
        "fan_perspective": "The Benito Villamarín is one of the most vibrant, emotionally charged stadiums in world football. Béticos have embraced this European adventure with unmatched passion, turning every home match into a green-and-white carnival.\n\nSupporters revere 'El Ingeniero' Pellegrini and believe that their technical brilliance can carry them to the knockout rounds, creating memories that will be sung about in Seville for generations.",
        "needs_to_advance": "Sitting on a remarkable 9 points, Real Betis have already established a near-certain playoff floor. 6 more points from their remaining 5 ties will cement an unforgettable automatic top-8 Round of 16 bye."
    },
    "VfB Stuttgart": {
        "league": "Bundesliga",
        "manager": "Sebastian Hoeneß",
        "formation": "4-4-2 Fluid Modern Buildup",
        "why_good": "Sebastian Hoeneß has constructed one of the most aesthetically pleasing and tactically advanced teams in Europe. Stuttgart build out from the back with breathtaking composure, baiting opponents into pressing before dissecting them through central combinations.\n\nAngelo Stiller is the conductor of this orchestra—a deep-lying midfield technician whose press-resistance and vision rival the finest pivots on the continent. Ahead of him, Enzo Millot drifts inside from the wing to create overloads, while Maximilian Mittelstädt delivers pinpoint crosses from left-back.\n\nIn the attack, Deniz Undav acts as the ultimate connector and finisher. Undav drops into midfield pockets to create numerical superiorities before spinning into the penalty box to dispatch chances with predatory instincts.",
        "key_strengths": [
            "Angelo Stiller's world-class press-resistant buildup and line-breaking passing",
            "Deniz Undav's deceptive movement, playmaking vision, and clinical finishing",
            "Intricate half-space combinations orchestrated by Sebastian Hoeneß"
        ],
        "known_vulnerabilities": [
            "High defensive line can be exploited by elite counter-attacking sprinters",
            "Relatively inexperienced squad at the highest level of European competition"
        ],
        "key_players": [
            {"name": "Deniz Undav", "role": "Complete Forward & Master Connector", "impact": "Scored in consecutive European ties while creating 2.8 chances per 90 for teammates."},
            {"name": "Angelo Stiller", "role": "Deep-Lying Midfield Maestro", "impact": "Directs possession with 92% pass accuracy and exceptional disguised through-balls."},
            {"name": "Enzo Millot", "role": "Dynamic Attacking Midfielder", "impact": "Operates between lines with quick-turn dribbling and creative vision."},
            {"name": "Maximilian Mittelstädt", "role": "High-Output Overlapping Left-Back", "impact": "Delivers 6.2 crosses into the box per match, providing consistent wide width."}
        ],
        "fan_perspective": "The MHPArena in Stuttgart is experiencing a footballing renaissance. After years in the Bundesliga wilderness, supporters are pinching themselves as they watch Stuttgart outplay European royalty with fearless attacking football. The connection between Hoeneß and the fans is unbreakable.\n\nFans view every Champions League fixture as a celebration, but they genuinely believe their collective tactical coherence can shock any giant in the tournament.",
        "needs_to_advance": "With 7 points from their first three fixtures, Stuttgart are in prime position. 8 more points from their remaining fixtures will secure an automatic Round of 16 bye."
    },
    "Como": {
        "league": "Serie A",
        "manager": "Cesc Fàbregas",
        "formation": "4-2-3-1 Spanish Possession Revival",
        "why_good": "Cesc Fàbregas has turned Como into the most fascinating tactical project in Italian football. Playing with the elegance and brave possession philosophy of prime Spanish football, Como dominate the ball with intricate 4-2-3-1 structures that completely disorient standard Serie A mid-blocks.\n\nNico Paz is the crown jewel of this side—a sensational attacking midfielder on loan from Real Madrid who plays with breathtaking vision, silky dribbling, and a venomous left-footed strike. Alongside him, Sergi Roberto and Máximo Perrone bring elite technical pedigree in the double pivot, dictating tempo with composure.\n\nWide men Gabriel Strefezza and Alieu Fadera provide electric 1v1 threat on the wings, creating high-quality cutback opportunities for Patrick Cutrone's energetic penalty-box movement.",
        "key_strengths": [
            "Nico Paz's extraordinary creative vision, technical dribbling, and shooting",
            "Midfield composure and tempo regulation under Fàbregas's modern tactical scheme",
            "Patrick Cutrone's relentless pressing energy and box poaching instincts"
        ],
        "known_vulnerabilities": [
            "Defensive line lacks elite recovery sprint pace against world-class counter-attacks",
            "First European campaign in club history brings unavoidable tactical learning curves"
        ],
        "key_players": [
            {"name": "Nico Paz", "role": "Generational Attacking Midfielder & Creator", "impact": "Averages 3.8 completed dribbles and 3.2 key passes per match, dominating European highlights."},
            {"name": "Patrick Cutrone", "role": "Hard-Working Poacher & Captain", "impact": "Tireless worker who leads Como's pressing and finishes half-chances in the box."},
            {"name": "Sergi Roberto", "role": "Experienced Midfield Orchestrator", "impact": "Brings multiple Champions League-winning experience and composure under pressure."},
            {"name": "Gabriel Strefezza", "role": "Direct 1v1 Right Winger", "impact": "Beats defenders on the outside to whip dangerous deliveries into the 6-yard box."}
        ],
        "fan_perspective": "Stadio Giuseppe Sinigaglia, sitting on the picturesque shores of Lake Como, is experiencing pure fairy-tale football. The local supporters, backed by global celebrity owners, are living through the greatest era in the club's 117-year history.\n\nFans adore Fàbregas's brave, attacking philosophy and roar behind Nico Paz's brilliance, confident that Como are not just tourists in Europe, but a revolutionary tactical force.",
        "needs_to_advance": "Holding 6 points, Como need approximately 4 more points to secure their top-24 playoff spot, while 9 points from remaining fixtures could push them into shocking top-8 contention."
    },
    "Club Brugge": {
        "league": "Belgian Pro League",
        "manager": "Nicky Hayen",
        "formation": "4-3-3 Physically Imposing Direct Attack",
        "why_good": "Club Brugge are Belgium's standard-bearers in European football, combining physical power with technical incision. Under Nicky Hayen, Brugge execute a disciplined 4-3-3 system that thrives on rapid wing transitions and imposing aerial dominance.\n\nHans Vanaken is the heartbeat of this team—a 6'5\" midfield playmaker whose spatial intelligence, deceptive technical touch, and late box arrivals make him virtually impossible to mark for standard midfields. Beside him, Raphael Onyedika provides an aggressive ball-winning shield in front of the back four.\n\nOn the wings, Christos Tzolis and Andreas Skov Olsen provide explosive 1v1 threat, stretching defensive lines and supplying pinpoint service for Ferran Jutglà in the penalty area.",
        "key_strengths": [
            "Hans Vanaken's towering presence, vision, and late box arrival scoring threat",
            "Christos Tzolis's electric wing pace and direct shooting ability",
            "Exceptional European home fortress atmosphere at Jan Breydelstadion"
        ],
        "known_vulnerabilities": [
            "Central defense can be troubled by agile, quick-turning center-forwards",
            "Can struggle to maintain defensive intensity when forced into extended low blocks"
        ],
        "key_players": [
            {"name": "Hans Vanaken", "role": "Towering Playmaker & Team Captain", "impact": "Club legend who has scored 15+ European goals while leading Brugge in progressive passes."},
            {"name": "Christos Tzolis", "role": "Dynamic Left Winger & Finisher", "impact": "Averages 3.4 shots per game with explosive acceleration cutting inside."},
            {"name": "Raphael Onyedika", "role": "Dominant Defensive Midfield Destroyer", "impact": "Wins 70% of ground duels and protects the backline with relentless tackling."},
            {"name": "Joel Ordóñez", "role": "Young Athletic Center-Back", "impact": "Provides crucial recovery pace and aerial clearance numbers against European forwards."}
        ],
        "fan_perspective": "The Jan Breydel Stadium is one of the most intimidating away grounds in Northern Europe. Brugge supporters expect their club to advance past the league phase and reach the knockout rounds, having done so consistently in recent campaigns.\n\nThe blue-and-black faithful believe their physical power and home atmosphere make them a terrifying draw for any seeded club.",
        "needs_to_advance": "With 6 points banked, Club Brugge need roughly 4 to 5 more points from their remaining 5 fixtures to guarantee a top-24 playoff berth, while 10 points would put them in contention for an automatic top-8 seed."
    },
    "Roma": {
        "league": "Serie A",
        "manager": "Gian Piero Gasperini",
        "formation": "3-4-2-1 Relentless Man-to-Man Press",
        "why_good": "Under Gian Piero Gasperini, AS Roma have adopted one of the most suffocating tactical approaches in world football. Gasperini's signature full-pitch man-to-man pressing forces opponents into hurried long clearances, allowing Roma's back three to dominate aerial duels and instantly reset attacking waves.\n\nPaulo Dybala is the genius who brings magic to this demanding physical system. Dybala operates with total creative freedom in the attacking half-space, delivering world-class set-pieces, visionary reverse passes, and curling strikes from distance.\n\nUp front, Ukrainian powerhouse Artem Dovbyk acts as the ultimate focal point—pinning center-backs, winning physical battles, and converting crosses delivered by aggressive wing-backs Angeliño and Zeki Çelik. Manu Koné provides immense engine room power in midfield, shutting down opponent breaks with ease.",
        "key_strengths": [
            "Paulo Dybala's world-class individual brilliance, set-pieces, and final-third vision",
            "Artem Dovbyk's physical penalty-box dominance and aerial hold-up play",
            "Gasperini's suffocating man-to-man pressing traps that disrupt opposition rhythm"
        ],
        "known_vulnerabilities": [
            "Man-marking system leaves massive 1v1 spaces behind if a pressing duel is lost",
            "Paulo Dybala's physical durability requires careful minute management"
        ],
        "key_players": [
            {"name": "Paulo Dybala", "role": "World-Class Playmaker & Forward", "impact": "Averages 3.5 shot-creating actions per 90 and scores spectacular free-kicks."},
            {"name": "Artem Dovbyk", "role": "Powerhouse Target Striker", "impact": "Wins 65% of aerial duels and finishes with lethal power inside the penalty box."},
            {"name": "Manu Koné", "role": "Athletic Midfield Destroyer", "impact": "Ranks in the 95th percentile for progressive ball carries and midfield tackle success."},
            {"name": "Gianluca Mancini", "role": "Aggressive Center-Back & Leader", "impact": "Brings ferocious competitive intensity and dominant aerial presence on set-pieces."}
        ],
        "fan_perspective": "The Stadio Olimpico is a cauldron of Roman passion. The Curva Sud sings with deafening intensity from kickoff to the final whistle. Romanisti have embraced Gasperini's aggressive European style, believing this squad has the blend of Dybala's genius and Dovbyk's muscle to make a serious continental run.\n\nFans crave a return to the Champions League quarterfinals, and the belief in the capital is that Roma can dismantle anyone at the Olimpico.",
        "needs_to_advance": "Holding 4 points from three matchdays, Roma need approximately 6 more points to secure their playoff spot (10-point cutoff), with home matches against mid-tier clubs representing essential must-win opportunities."
    },
    "Fenerbahce": {
        "league": "Süper Lig",
        "manager": "İsmail Kartal",
        "formation": "4-2-3-1 High-Energy Wide Overload",
        "why_good": "Fenerbahçe play with an intensity and passion that mirrors the roaring atmosphere of Istanbul. Under İsmail Kartal, the Yellow Canaries deploy an aggressive 4-2-3-1 system that utilizes the physical midfield dominance of Sofyan Amrabat and Fred to control the center of the pitch.\n\nIn the attacking third, veteran maestro Dušan Tadić directs play with supreme intelligence, cutting inside from the right to pick out the explosive 1v1 runs of Allan Saint-Maximin. Saint-Maximin is a terrifying prospect for opposing full-backs, leading the competition in successful take-on percentage.\n\nInside the box, veteran striker Edin Džeko continues to deliver masterclasses in center-forward play—using his 6'4\" frame to bring midfielders into play before arriving at the back post to convert crosses with lethal precision.",
        "key_strengths": [
            "Dušan Tadić's supreme footballing IQ and pinpoint chance delivery",
            "Allan Saint-Maximin's unplayable 1v1 dribbling and explosive acceleration",
            "Sofyan Amrabat and Fred's aggressive midfield ball-winning foundation"
        ],
        "known_vulnerabilities": [
            "Center-back pairing can be troubled by elite sprint pace on counter-attacks",
            "Tendency to commit emotional fouls in hostile European away environments"
        ],
        "key_players": [
            {"name": "Edin Džeko", "role": "Legendary Center-Forward & Captain", "impact": "Over 40 European career goals; provides world-class hold-up play and penalty-box finishing."},
            {"name": "Dušan Tadić", "role": "Master Playmaker & Wing Creator", "impact": "Delivers 3.2 key passes per match and orchestrates Fenerbahçe's final-third attacking rotations."},
            {"name": "Allan Saint-Maximin", "role": "Electric 1v1 Left Winger", "impact": "Averages 5.4 completed dribbles per match, terrorizing opposing full-backs."},
            {"name": "Sofyan Amrabat", "role": "Midfield Destroyer & Shield", "impact": "Wins 74% of physical challenges and breaks up opposition transitional attacks."}
        ],
        "fan_perspective": "The Şükrü Saracoğlu Stadium in Kadıköy is widely regarded as one of the most intimidating sporting arenas on earth. The deafening whistles, flares, and non-stop chanting push the players to extraordinary physical limits. Fener fans have waited years for a statement Champions League campaign.\n\nThe supporters believe that with Džeko, Tadić, and Saint-Maximin, they have the star quality to beat any visiting European giant in Istanbul.",
        "needs_to_advance": "Currently on 4 points, Fenerbahçe's mathematical objective is reaching 10 points to clinch a top-24 playoff spot. Winning their remaining home fixtures in Istanbul is the critical foundation for their qualification campaign."
    },
    "Galatasaray": {
        "league": "Süper Lig",
        "manager": "Okan Buruk",
        "formation": "3-4-1-2 Blockbuster Twin-Striker Blitz",
        "why_good": "Galatasaray boast one of the most terrifying forward partnerships in European football: Victor Osimhen and Mauro Icardi. Okan Buruk has crafted an aggressive 3-4-1-2 system designed entirely around feeding this world-class strike duo.\n\nVictor Osimhen brings peerless athletic power, sprint speed, and aerial leaps that overwhelm center-backs, while Mauro Icardi provides masterclass penalty-box finishing and positional poaching. When both strikers are on the pitch, opposing defenses are simply unable to cope with the dual threat.\n\nIn midfield, Lucas Torreira is an indefatigable terrier, leading the team in tackles and interceptions, while Gabriel Sara delivers laser-sharp through-balls into the channels. Behind them, Davinson Sánchez provides elite recovery speed in a three-man defense.",
        "key_strengths": [
            "Victor Osimhen and Mauro Icardi: Europe's most feared twin-striker partnership",
            "Lucas Torreira's relentless ball-winning engine in central midfield",
            "RAMS Park's deafening stadium atmosphere that routinely overwhelms visiting giants"
        ],
        "known_vulnerabilities": [
            "Ultra-attacking lineup can leave wide spaces behind aggressive wing-backs",
            "Emotional discipline in volatile high-intensity European ties"
        ],
        "key_players": [
            {"name": "Victor Osimhen", "role": "World-Class Powerhouse Striker", "impact": "A physical nightmare for defenders; averages 1.12 xG per 90 with elite aerial conversion."},
            {"name": "Mauro Icardi", "role": "Clinical Box Predator", "impact": "Requires only half a yard of space to convert half-chances inside the 18-yard box."},
            {"name": "Lucas Torreira", "role": "Midfield Pitbull & Ball Recoverer", "impact": "Wins 4.2 tackles per 90, shutting down opponent transitions instantly."},
            {"name": "Gabriel Sara", "role": "Visionary Midfield Playmaker", "impact": "Supplies defense-splitting through-balls and delivers dangerous set-pieces."}
        ],
        "fan_perspective": "RAMS Park is pure footballing thunder. The 'Welcome to Hell' banners and 130+ decibel roar create an atmosphere that visiting European managers openly acknowledge as terrifying. Cimbom supporters are ecstatic with Osimhen and Icardi leading the line.\n\nFans firmly believe that Galatasaray are good enough not just to make the playoffs, but to take down anyone in the knockout stages with their ferocious home support.",
        "needs_to_advance": "With 7 points from three fixtures, Galatasaray are on the verge of securing a playoff spot. Two more victories (reaching 13-14 points) could see them sensationally challenge for an automatic top-8 bye."
    },
    "RB Leipzig": {
        "league": "Bundesliga",
        "manager": "Marco Rose",
        "formation": "4-2-2-2 High-Octane Red Bull Press",
        "why_good": "RB Leipzig represent the purest expression of the high-octane Red Bull pressing philosophy. Under Marco Rose, Leipzig attack at breakneck speed, using a narrow 4-2-2-2 formation to trap opponents inside their own half before executing lightning-fast vertical combinations.\n\nXavi Simons is the superstar catalyst of this side—a technical wizard whose close-control dribbling, explosive changes of direction, and vision between the lines unlock defenses in a split second. Flanking him, Christoph Baumgartner provides tireless running and late box arrivals.\n\nUp front, Loïs Openda and Benjamin Šeško form a terrifying striker duo. Openda possesses blistering sprint speed that exploits high lines, while Šeško combines a 6'5\" aerial frame with a thunderous long-range shooting technique.",
        "key_strengths": [
            "Xavi Simons's world-class 1v1 dribbling and half-space playmaking brilliance",
            "Loïs Openda and Benjamin Šeško's devastating combination of pace and power",
            "Fierce central counter-pressing that forces high-turnover scoring opportunities"
        ],
        "known_vulnerabilities": [
            "Tactical struggles when forced to break down disciplined, deep low blocks",
            "Defensive lapses on set-pieces and wide diagonal cross deliveries"
        ],
        "key_players": [
            {"name": "Xavi Simons", "role": "Superstar Playmaker & Dribbler", "impact": "Averages 4.2 shot-creating actions per 90 and dictates Leipzig's attacking tempo."},
            {"name": "Loïs Openda", "role": "Electric Breakaway Striker", "impact": "Top sprinter in the Bundesliga; averages 0.88 goals per 90 on counter-attacks."},
            {"name": "Benjamin Šeško", "role": "Towering Modern Number 9", "impact": "Scores spectacular goals from distance and provides crucial aerial presence."},
            {"name": "Willi Orbán", "role": "Veteran Defensive Rock & Captain", "impact": "Commands the backline with aerial strength and disciplined positioning."}
        ],
        "fan_perspective": "Red Bull Arena expects exciting, vertical football. Leipzig supporters know the club's model is built on youthful dynamism and fearlessness. After a challenging start to the league phase, fans are rallying behind Rose and Simons to turn the campaign around.\n\nThe feeling in Saxony is that when Leipzig's press clicks, they can blow any defense away within a 15-minute blitz.",
        "needs_to_advance": "Currently fighting on 3 points, Leipzig face an uphill battle. They must target at least 7 to 8 points from their remaining 5 fixtures to reach the 10-point cutoff required for playoff survival."
    },
    "Shakhtar Donetsk": {
        "league": "Ukrainian Premier League",
        "manager": "Marino Pušić",
        "formation": "4-3-3 Technical Courage & Fluid Build",
        "why_good": "Shakhtar Donetsk are the symbol of extraordinary resilience and technical bravery in European football. Despite playing all European 'home' fixtures on neutral turf in Germany, Marino Pušić's squad plays with stunning technical composure, refusing to abandon their fluid passing philosophy.\n\nGeorgiy Sudakov is Europe's most coveted young midfield playmaker—a press-resistant technician whose spatial awareness, disguise passes, and line-breaking carries make him the heartbeat of the Ukrainian champions. Alongside him, veteran Taras Stepanenko provides defensive discipline and leadership.\n\nOn the wings, Shakhtar blend Ukrainian grit with Brazilian flair through Newertton, Kevin, and Oleksandr Zubkov, creating quick 1v1 overloads that catch over-extended European defenses off-guard.",
        "key_strengths": [
            "Georgiy Sudakov's elite press-resistant playmaking and visionary passing",
            "Extraordinary psychological resilience and collective spirit under adversity",
            "Lightning wide wing transitions through Zubkov and Brazilian talents"
        ],
        "known_vulnerabilities": [
            "Lack of a genuine permanent home stadium atmosphere due to displacement",
            "Can be physically overpowered by aerially dominant European giants on set-pieces"
        ],
        "key_players": [
            {"name": "Georgiy Sudakov", "role": "Elite Midfield Playmaker", "impact": "Leads Shakhtar in progressive passes and key chances created, drawing massive European interest."},
            {"name": "Oleksandr Zubkov", "role": "Direct Right Winger & Finisher", "impact": "Delivers dangerous curling crosses and possesses a lethal left-footed strike."},
            {"name": "Mykola Matviyenko", "role": "Ball-Playing Center-Back & Leader", "impact": "Initiates buildup with laser precision and commands the defensive line."},
            {"name": "Dmytro Riznyk", "role": "Reflex Shot-Stopper", "impact": "Averages 4.5 saves per European match, keeping Shakhtar in tight contests."}
        ],
        "fan_perspective": "Shakhtar represent an entire nation fighting for pride on the global stage. Ukrainian supporters across Europe pack the Volksparkstadion in Hamburg to create a deeply moving, passionate atmosphere. Fans take immense pride in seeing homegrown stars like Sudakov and Matviyenko showcase their courage against the wealthiest clubs on earth.",
        "needs_to_advance": "With 4 points secured, Shakhtar are targeting two wins from their final 5 fixtures to reach the magic 10-point mark and qualify for the knockout playoffs."
    },
    "PSV Eindhoven": {
        "league": "Eredivisie",
        "manager": "Peter Bosz",
        "formation": "4-3-3 Total Attacking Frenzy",
        "why_good": "Peter Bosz's PSV Eindhoven are the most uncompromising attacking team in Northern Europe. PSV commit huge numbers forward, pressing high up the pitch and flooding the penalty area with dynamic runners from all angles.\n\nJohan Bakayoko and Noa Lang provide sensational wing trickery and pace, relentlessly isolating full-backs and delivering whipped crosses into the 6-yard box. In the center of the box, veteran striker Luuk de Jong remains the undisputed aerial king of European football—winning towering headers over any defender in the tournament.\n\nIn midfield, Jerdy Schouten and Guus Til offer the perfect balance of defensive screening and aggressive penalty-box arrivals, ensuring PSV sustain relentless pressure throughout the 90 minutes.",
        "key_strengths": [
            "Luuk de Jong's unmatched aerial dominance and header conversion",
            "Johan Bakayoko and Noa Lang's electric 1v1 wide dribbling threat",
            "Peter Bosz's high-octane attacking philosophy and chance-creation volume"
        ],
        "known_vulnerabilities": [
            "Extreme attacking commitment leaves huge spaces behind for counter-attacking wingers",
            "Defensive transitions can be chaotic when the initial high press is bypassed"
        ],
        "key_players": [
            {"name": "Luuk de Jong", "role": "Towering Striker & Aerial Master", "impact": "Wins 76% of aerial duels inside the 18-yard box, scoring crucial headers."},
            {"name": "Johan Bakayoko", "role": "Explosive Right Winger", "impact": "Averages 4.1 completed dribbles per match with a wicked curling left-footed strike."},
            {"name": "Jerdy Schouten", "role": "Tactical Anchor & Deep Pivot", "impact": "Maintains 92% pass accuracy while intercepting dangerous opponent counter-attacks."},
            {"name": "Noa Lang", "role": "Unpredictable Left-Wing Creator", "impact": "Brings swagger, audacity, and vision to break down compact European mid-blocks."}
        ],
        "fan_perspective": "The Philips Stadion in Eindhoven is bouncing. PSV supporters love Bosz's fearless, attack-minded brand of football. While fans acknowledge that playing so openly can lead to wild, high-scoring shootouts, the belief in Eindhoven is that PSV can score against any defense in Europe.",
        "needs_to_advance": "Holding 5 points, PSV need approximately 5 more points from their remaining 5 fixtures to secure a playoff berth, with home games offering prime opportunities to bank victories."
    },
    "Villarreal": {
        "league": "La Liga",
        "manager": "Marcelino",
        "formation": "4-4-2 Compact Counter-Attacking Mastery",
        "why_good": "Marcelino's Villarreal are masters of tournament football. Operating in an impeccably disciplined 4-4-2 shape, the 'Yellow Submarine' absorb pressure in a tight mid-block before executing lethal counter-attacks with surgical efficiency.\n\nÁlex Baena is the creative heartbeat of this team—a visionary playmaker who leads Europe in open-play key passes, finding teammates through the tightest defensive corridors. Beside him, Dani Parejo provides veteran tempo control and dead-ball perfection.\n\nUp front, Ayoze Pérez and Thierno Barry form a dynamic strike partnership: Ayoze brings silky close-control and clinical poaching, while Barry offers raw physical power and relentless channel running.",
        "key_strengths": [
            "Álex Baena's world-class vision, assists, and open-play chance creation",
            "Marcelino's compact, disciplined 4-4-2 defensive block that frustrates possession sides",
            "Lethal transition efficiency through Ayoze Pérez and Thierno Barry"
        ],
        "known_vulnerabilities": [
            "Can lack top-end sprint pace in central defense when pushed deep into their box",
            "Relies heavily on Álex Baena for creative inspiration against deep blocks"
        ],
        "key_players": [
            {"name": "Álex Baena", "role": "Master Playmaker & Assist Leader", "impact": "Leads the Champions League with 3 assists and 10 key passes from wide-left."},
            {"name": "Ayoze Pérez", "role": "Clinical Second Striker", "impact": "Has scored in consecutive European matches with intelligent near-post movement."},
            {"name": "Dani Parejo", "role": "Veteran Midfield Quarterback", "impact": "Controls game tempo and delivers dangerous set-pieces from all angles."},
            {"name": "Raúl Albiol", "role": "Veteran Defensive Leader & Captain", "impact": "Commands the backline with positional wisdom and aerial strength."}
        ],
        "fan_perspective": "The Estadio de la Cerámica is a proud fortress for a town of just 50,000 people that continually punches above its weight on the global stage. Groguets fans know their club has a proud history of European knockout heroics, including their 2021 Europa League triumph and 2022 Champions League semifinal run. The belief in Marcelino is total.",
        "needs_to_advance": "Sitting on 5 points, Villarreal need 5 more points from their final 5 fixtures to clinch a top-24 playoff spot, while 10 points would give them an outside shot at an automatic top-8 seed."
    },
    "Manchester United": {
        "league": "Premier League",
        "manager": "Michael Carrick",
        "formation": "4-2-3-1 Pragmatic Direct Attack",
        "why_good": "Manchester United possess extraordinary individual match-winners capable of blowing ties open in seconds. Under Michael Carrick, the Red Devils have prioritized defensive compactness and rapid vertical transitions to unleash the pace of Alejandro Garnacho and the playmaking brilliance of Bruno Fernandes.\n\nBruno Fernandes is the team's undisputed creative engine, leading Europe in progressive passes and dangerous crosses into the box. Flanking him, Garnacho and Amad Diallo provide dynamic 1v1 threat on the wings, stretching defenses and creating space for Rasmus Højlund in the box.\n\nIn midfield, Kobbie Mainoo and Casemiro provide a balanced double pivot—Mainoo brings press-resistant composure and ball retention, while Casemiro offers physical aerial authority and defensive protection.",
        "key_strengths": [
            "Bruno Fernandes's world-class defense-splitting passing and talismanic leadership",
            "Alejandro Garnacho's electric transitional speed and direct running at full-backs",
            "Old Trafford European night atmosphere and historic tournament pedigree"
        ],
        "known_vulnerabilities": [
            "Inconsistency in maintaining defensive structure over full 90-minute stretches",
            "Can struggle when opponents force them to build slowly through crowded central midfields"
        ],
        "key_players": [
            {"name": "Bruno Fernandes", "role": "Talismanic Captain & Primary Creator", "impact": "Directly involved in 65% of United's European chances through pinpoint through-balls."},
            {"name": "Alejandro Garnacho", "role": "Explosive Left Winger & Match-Winner", "impact": "Averages 4.2 progressive runs per match, cutting inside to unleash lethal shots."},
            {"name": "Kobbie Mainoo", "role": "Silky Press-Resistant Midfield Prodigy", "impact": "Glides past pressure with exceptional body feints and 89% pass accuracy."},
            {"name": "André Onana", "role": "Aggressive Sweeper-Keeper", "impact": "Provides long-range distribution and reflex saves in high-pressure European moments."}
        ],
        "fan_perspective": "The Stretford End demands European glory. While United have experienced a turbulent transition period, European nights under the Old Trafford floodlights still hold mystical power. Supporters are eager to see this young, fast team establish a new identity on the continental stage.\n\nFans know defensive concentration must improve, but with Fernandes and Garnacho, supporters believe United can score against any team on the continent.",
        "needs_to_advance": "Sitting on 4 points, Manchester United's primary target is reaching 10 points to secure safe passage into the knockout playoff round, with upcoming home fixtures at Old Trafford being non-negotiable must-wins."
    },
    "Napoli": {
        "league": "Serie A",
        "manager": "Antonio Conte",
        "formation": "4-3-3 Intense Physical Dominance",
        "why_good": "Antonio Conte has forged Napoli into a physically punishing, tactically relentless machine. Napoli play with unmatched defensive discipline, suffocating opponents with ferocious mid-block pressing and quick vertical releases into their devastating forward line.\n\nRomelu Lukaku is the ultimate focal point of Conte's attack—a physical colossus who holds off defenders with his back to goal before spinning into space or laying off passes for Scott McTominay's thundering box arrivals. McTominay has become a sensation in Naples, dominating aerial duels and scoring clutch goals.\n\nOn the left wing, Khvicha Kvaratskhelia is pure magic—a dribbler who can beat three defenders in a phone booth before curling strikes into the top corner. In defense, Alessandro Buongiorno and Giovanni Di Lorenzo anchor a backline that concedes virtually nothing in the box.",
        "key_strengths": [
            "Khvicha Kvaratskhelia's unplayable 1v1 dribbling and solo goal threat",
            "Romelu Lukaku's immense physical hold-up play and penalty-box gravity",
            "Scott McTominay's box-to-box power, late runs, and aerial goalscoring"
        ],
        "known_vulnerabilities": [
            "Midfield can lack lateral speed against rapid counter-attacking wing overloads",
            "Tactical rigidity under Conte can struggle when trailing in the final 15 minutes"
        ],
        "key_players": [
            {"name": "Khvicha Kvaratskhelia", "role": "Virtuoso Left Winger & Game-Changer", "impact": "Averages 4.8 completed take-ons per 90 and creates chances out of nothing."},
            {"name": "Romelu Lukaku", "role": "Colossal Target Striker", "impact": "Pins center-backs and creates space for late midfield runners with supreme hold-up play."},
            {"name": "Scott McTominay", "role": "Box-to-Box Midfield Enforcer", "impact": "Tireless runner who leads Napoli in second-ball recoveries and late box-entry goals."},
            {"name": "Alessandro Buongiorno", "role": "Commanding Central Defender", "impact": "Wins 75% of ground duels and neutralizes opposing center-forwards with physical strength."}
        ],
        "fan_perspective": "The Stadio Diego Armando Maradona is rocking with Neapolitan fury and passion. Partenopei supporters adore Antonio Conte's relentless work-ethic and fight. The city believes this team has the grit, character, and individual genius to make a deep statement run in the Champions League.\n\nVisiting teams dread the hostile atmosphere at the Maradona, where Napoli play with ferocious intensity.",
        "needs_to_advance": "Holding 5 points, Napoli need approximately 5 more points from their remaining 5 fixtures to seal a playoff berth, while targeting home wins to push for an outside top-8 bye."
    },
    "Lille": {
        "league": "Ligue 1",
        "manager": "Bruno Génésio",
        "formation": "4-2-3-1 Giant-Killing Precision",
        "why_good": "Bruno Génésio's Lille have earned a reputation as Europe's premier giant-killers. Having claimed famous victories against both Real Madrid and Atletico Madrid, LOSC play with remarkable tactical intelligence, blending compact defensive organization with lightning transition speed.\n\nJonathan David is Europe's most underrated striker—a clinical Canadian international whose movement off the shoulder of defenders and calm box finishing punish the slightest defensive errors. Behind him, Angel Gomes orchestrates play with press-resistant elegance and vision.\n\nOn the right flank, Edon Zhegrova is an unpredictable wizard, cutting inside onto his wicked left foot to unleash curling strikes and dangerous cutbacks. In goal, Lucas Chevalier has emerged as one of the finest young shot-stoppers in world football.",
        "key_strengths": [
            "Jonathan David's world-class penalty-box finishing and intelligent movement",
            "Edon Zhegrova's electrifying 1v1 dribbling and unpredictability on the wing",
            "Lucas Chevalier's heroic shot-stopping and calm command of his penalty box"
        ],
        "known_vulnerabilities": [
            "Can struggle to break down low blocks when forced to dominate 65%+ possession",
            "Thin squad depth tested when multiple key players face muscle injuries"
        ],
        "key_players": [
            {"name": "Jonathan David", "role": "Clinical Center-Forward & Top Scorer", "impact": "Averages 0.82 goals per 90 in Europe with ruthless near-post conversion."},
            {"name": "Edon Zhegrova", "role": "Dazzling Right-Wing Dribbler", "impact": "Averages 4.5 successful take-ons per 90, terrorizing full-backs across Europe."},
            {"name": "Lucas Chevalier", "role": "Elite Goalkeeper & Shot-Stopper", "impact": "Single-handedly preserved wins against Madrid clubs with extraordinary reflex stops."},
            {"name": "Benjamin André", "role": "Veteran Midfield Captain & Destroyer", "impact": "The defensive anchor who leads Ligue 1 in tackles and loose ball recoveries."}
        ],
        "fan_perspective": "The Stade Pierre-Mauroy is roaring with historic pride. Lille supporters have witnessed their club topple the giants of Madrid in unforgettable fashion, proving that teamwork, tactical execution, and fearlessness can conquer astronomical payrolls.\n\nFans believe this squad has the defensive composure and counter-attacking punch to shock anyone over a two-legged knockout tie.",
        "needs_to_advance": "With 6 points banked from tough fixtures, Lille need 4 more points to guarantee a top-24 playoff spot, while 9 points could see them challenge for an automatic top-8 seed."
    },
    "Porto": {
        "league": "Primeira Liga",
        "manager": "Vítor Bruno",
        "formation": "4-2-3-1 Aggressive Pressing Block",
        "why_good": "FC Porto embody the fierce competitive spirit and tactical aggression of Portuguese football. Under Vítor Bruno, the Dragões play with intense pressing, physical duel-dominance, and devastating vertical speed through wide channels.\n\nDiogo Costa is arguably the best goalkeeper in Europe under 26—a commanding sweeper-keeper with world-class penalty-stopping ability and laser-guided distribution. Shielding him, Alan Varela provides an elite defensive screen, breaking up opposition play with relentless tenacity.\n\nIn attack, Samu Omorodion has emerged as a terrifying physical specimen—a 6'4\" powerhouse who combines sprinter speed with brute strength, bullying center-backs and scoring at a prolific rate. Alongside him, Galeno and Pepê provide non-stop running and 1v1 trickery.",
        "key_strengths": [
            "Samu Omorodion's terrifying physical power, pace, and penalty-box goal threat",
            "Diogo Costa's world-class shot-stopping, penalty-saving, and long distribution",
            "Alan Varela's defensive midfield tenacity and positional discipline"
        ],
        "known_vulnerabilities": [
            "Emotional volatility in hostile European environments leading to unnecessary cards",
            "Vulnerable to sophisticated technical midfields that bypass their initial aggressive press"
        ],
        "key_players": [
            {"name": "Samu Omorodion", "role": "Explosive Physical Striker", "impact": "Bulldozes defensive lines with raw strength, scoring 5 goals in his first European ties."},
            {"name": "Diogo Costa", "role": "World-Class Goalkeeper & Leader", "impact": "Commands the backline with an 84% save percentage and elite penalty-saving record."},
            {"name": "Alan Varela", "role": "Midfield Pitbull & Tactical Shield", "impact": "Wins 70% of central duels and dictates Porto's tempo with calm distribution."},
            {"name": "Galeno", "role": "Dynamic Left Winger & Runner", "impact": "Stretches defenses with electric speed and dangerous diagonal runs into the box."}
        ],
        "fan_perspective": "The Estádio do Dragão is a fortress built on passion and European heritage. Portistas expect their club to fight like warriors in every match, carrying two European Cup triumphs as their eternal standard. Fans adore Samu Omorodion's explosive arrival and believe Porto's trademark intensity makes them a nightmare opponent.",
        "needs_to_advance": "Currently on 4 points after narrow defeats, Porto need 6 more points from their remaining 5 fixtures to reach the 10-point playoff safety mark, with home matches at the Dragão being absolute must-win clashes."
    },
    "Feyenoord": {
        "league": "Eredivisie",
        "manager": "Brian Priske",
        "formation": "4-3-3 High-Intensity Rotations",
        "why_good": "Feyenoord play with an electric intensity and ferocious pressing that turns European matches into chaotic, high-tempo battles. Under Brian Priske, the Rotterdam giants deploy an aggressive 4-3-3 system that hunts the ball relentlessly in the opposition half.\n\nQuinten Timber is the dynamic powerhouse in midfield—a box-to-box engine who drives the ball forward through sheer strength and skill. Flanking him, In-beom Hwang provides surgical distribution and tactical balance, allowing Antoni Milambo to make dangerous late runs into the penalty box.\n\nOn the wings, Igor Paixão and Ibrahim Osman terrorize defenders with blistering speed and relentless pressing, creating high-quality scoring chances for Ayase Ueda.",
        "key_strengths": [
            "Quinten Timber's physical dynamism and line-breaking midfield ball carries",
            "De Kuip's legendary stadium atmosphere that overwhelms visiting clubs",
            "Igor Paixão's explosive pace and unpredictable 1v1 dribbling on the left"
        ],
        "known_vulnerabilities": [
            "High defensive line can be caught out by precise diagonal balls over the top",
            "Injury absences to key center-forward Santiago Giménez tested finishing depth"
        ],
        "key_players": [
            {"name": "Quinten Timber", "role": "Powerhouse Box-to-Box Midfielder", "impact": "Leads Feyenoord in duels won, tackles, and progressive carries into the final third."},
            {"name": "Igor Paixão", "role": "Dynamic Brazilian Left Winger", "impact": "Averages 3.8 dribbles per match, cutting inside to unleash dangerous strikes."},
            {"name": "Dávid Hancko", "role": "Elite Ball-Playing Center-Back", "impact": "Commands the defense with aerial strength and precise 50-yard passes."},
            {"name": "In-beom Hwang", "role": "Midfield Conductor & Anchor", "impact": "Completes 88% of passes under pressure, providing stability in transition."}
        ],
        "fan_perspective": "De Kuip (The Tub) is widely considered one of the loudest and most intimidating cauldrons in world football. The stadium literally shakes when Feyenoord score. The Rotterdam faithful pride themselves on working-class grit and passion, demanding non-stop commitment from their players.\n\nFans believe that under the lights of De Kuip, Feyenoord can dismantle any visiting giant.",
        "needs_to_advance": "Holding 6 points with two impressive victories, Feyenoord need roughly 4 to 5 more points from their remaining 5 fixtures to secure their spot in the knockout playoffs."
    },
    "Bodo/Glimt": {
        "league": "Eliteserien",
        "manager": "Kjetil Knutsen",
        "formation": "4-3-3 Synchronized Arctic Storm",
        "why_good": "FK Bodø/Glimt are Europe's most miraculous tactical project. Hailing from inside the Arctic Circle, Kjetil Knutsen's side plays a brand of synchronized, lightning-fast attacking football that has humbled some of the continent's wealthiest clubs.\n\nOperating in a seamless 4-3-3, Bodø/Glimt play with telepathic understanding. Captain Patrick Berg directs traffic from the deep pivot with metronomic passing, while Håkon Evjen and Ulrik Saltnes execute coordinated third-man runs that dismantle mid-blocks.\n\nOn the left wing, Jens Petter Hauge is in dazzling form—cutting inside with quick acceleration and curling unstoppable strikes into the far corner. Combined with their artificial turf and Arctic winds, Bodø/Glimt are a terrifying away trip for any team in Europe.",
        "key_strengths": [
            "Kjetil Knutsen's telepathic tactical coordination and synchronized passing",
            "Jens Petter Hauge's world-class 1v1 dribbling and decisive finishing",
            "Aspmyra Stadion's freezing Arctic conditions and fast artificial turf"
        ],
        "known_vulnerabilities": [
            "Away form can drop in warmer, grass-pitch stadiums against physical giants",
            "Lack of aerial height in central defense against dominant set-piece teams"
        ],
        "key_players": [
            {"name": "Jens Petter Hauge", "role": "Talismanic Left Winger & Scorer", "impact": "Has scored spectacular European goals and completed 4.2 take-ons per 90."},
            {"name": "Patrick Berg", "role": "Midfield General & Captain", "impact": "Averages 88 passes per match at 91% accuracy, dictating the tempo of the team."},
            {"name": "Håkon Evjen", "role": "Dynamic Box-to-Box Midfielder", "impact": "Tireless runner who penetrates half-spaces and forces high-turnover errors."},
            {"name": "Nikita Haikin", "role": "Experienced European Goalkeeper", "impact": "Calm distributor from the back with outstanding close-range reflex stops."}
        ],
        "fan_perspective": "Aspmyra Stadion, with its iconic yellow toothbrushes and freezing Arctic winds, is a place of pure joy. The entire town of Bodø (population 55,000) lives and breathes for Glimt. Having previously thrashed Roma 6-1, supporters genuinely believe that no team on earth can survive their Arctic storm when the yellow shirts start clicking.",
        "needs_to_advance": "Currently on 4 points, Bodø/Glimt need 6 more points from their remaining 5 fixtures to reach the 10-point playoff safety mark, with home fixtures at Aspmyra being crucial."
    },
    "Lens": {
        "league": "Ligue 1",
        "manager": "Will Still",
        "formation": "3-4-1-2 High-Intensity Front-Foot Press",
        "why_good": "RC Lens represent the beating heart of French working-class football. Under the charismatic Will Still, Les Sang et Or play with relentless energy, suffocating opponents with an aggressive 3-4-1-2 pressing shape that never stops hunting the ball.\n\nKevin Danso and Facundo Medina form one of the most physically imposing and aggressive defensive partnerships in Europe, stepping forward into midfield to extinguish counter-attacks before they start. In goal, Brice Samba provides world-class shot-stopping and sensational 70-yard distribution.\n\nOut wide, Przemysław Frankowski and Deiver Machado provide non-stop overlapping running, delivering dangerous crosses for Florian Sotoca and M'Bala Nzola in the penalty box.",
        "key_strengths": [
            "Kevin Danso and Facundo Medina's aggressive, physically dominant central defense",
            "Brice Samba's heroic shot-stopping and pinpoint long-range distribution",
            "Stade Bollaert-Delelis: France's most passionate, vociferous stadium atmosphere"
        ],
        "known_vulnerabilities": [
            "Aggressive high-line pressing can be bypassed by elite technical passers",
            "Can lack a clinical 20-goal-a-season finisher against deep defensive low blocks"
        ],
        "key_players": [
            {"name": "Brice Samba", "role": "Captain & Elite Sweeper-Keeper", "impact": "Commands the box with authority and initiates rapid breaks with pinpoint kicking."},
            {"name": "Kevin Danso", "role": "Colossal Central Defender", "impact": "Wins 76% of ground and aerial duels, physically intimidating opposing strikers."},
            {"name": "Przemysław Frankowski", "role": "Tireless Right Wing-Back", "impact": "Runs 11.5 km per game, delivering pinpoint crosses and tracking back defensively."},
            {"name": "Florian Sotoca", "role": "Workhorse Forward & Connector", "impact": "The tactical glue of the team, winning second balls and linking midfield to attack."}
        ],
        "fan_perspective": "The Stade Bollaert-Delelis holds 38,000 spectators in a town of 31,000 people—meaning the entire town fits inside the stadium. When the anthem 'Les Corons' rings out, the hairs on the back of your neck stand up. Lens supporters adore Will Still's fighting spirit and believe their collective soul can triumph over any billionaire club.",
        "needs_to_advance": "Holding 4 points, Lens must target two victories from their final 5 fixtures to reach the 10-point mark and advance to the Champions League knockout playoffs."
    },
    "Slavia Praha": {
        "league": "Czech First League",
        "manager": "Jindřich Trpišovský",
        "formation": "3-4-2-1 Full-Pitch Running & Pressing",
        "why_good": "Jindřich Trpišovský's Slavia Praha are the marathon runners of European football. Year after year, Slavia lead all UEFA competitions in distance covered and high-intensity sprints, grinding opponents into submission through relentless physical attrition.\n\nOperating in an aggressive 3-4-2-1, Slavia press full-pitch man-to-man. In midfield, Oscar Dorley and Christos Zafeiris cover extraordinary ground, winning second balls and recycling possession with composure.\n\nUp front, Tomáš Chorý is a 6'6\" giant who acts as an unstoppable aerial battering ram. Chorý wins direct goal kicks, holds off multiple defenders, and creates havoc in the penalty box for Lukáš Provod and Mojmír Chytil to exploit.",
        "key_strengths": [
            "Europe's highest running volume and relentless physical pressing stamina",
            "Tomáš Chorý's 6'6\" aerial dominance and physical penalty-box disruption",
            "Fortress Eden Arena atmosphere with non-stop ultra chanting"
        ],
        "known_vulnerabilities": [
            "Can lack technical finesse when forced to break down organized, technical low blocks",
            "High physical exertion can lead to late-game fatigue and defensive errors"
        ],
        "key_players": [
            {"name": "Tomáš Chorý", "role": "6'6\" Aerial Battering Ram & Striker", "impact": "Wins an astonishing 82% of aerial duels, dominating European center-backs."},
            {"name": "Lukáš Provod", "role": "Dynamic Left-Sided Attacking Playmaker", "impact": "Delivers pinpoint crosses and possesses a lethal long-range shot."},
            {"name": "Christos Zafeiris", "role": "Tireless Midfield Dynamo", "impact": "Covers 12+ km per match, breaking up opponent buildup with relentless pressing."},
            {"name": "Tomáš Holeš", "role": "Veteran Center-Back & Leader", "impact": "Commands the defensive line with tactical intelligence and aerial strength."}
        ],
        "fan_perspective": "The Fortuna Arena in Prague is a loud, bouncing fortress of red and white. Slavia supporters demand 100% effort, and Trpišovský's side embodies Czech determination. Having claimed famous European scalps in the past, fans believe their physical running power can overwhelm any complacent foreign giant.",
        "needs_to_advance": "Currently on 3 points, Slavia need at least 7 points from their remaining 5 fixtures to reach the 10-point playoff cutoff, making their home fixtures in Prague essential."
    },
    "AEK Athens": {
        "league": "Super League Greece",
        "manager": "Matías Almeyda",
        "formation": "4-4-2 High-Pressure Intensity",
        "why_good": "Matías Almeyda has instilled his fierce Argentine spirit into AEK Athens. Playing an aggressive, man-oriented pressing scheme, AEK hunt opponents with ferocious intensity across all thirds of the pitch.\n\nIn midfield, Mexican international Orbelín Pineda brings technical brilliance, close control, and line-breaking passes, while Damian Szymański provides physical enforcement. Flanking them, Niclas Eliasson delivers pinpoint crosses from the right wing.\n\nUp front, Frantzdy Pierrot and Levi García form an overwhelmingly physical strike force—Pierrot provides aerial muscle, while García offers explosive sprint speed and power running that terrifies backlines.",
        "key_strengths": [
            "Frantzdy Pierrot and Levi García's overpowering physical and aerial strike partnership",
            "OPAP Arena's deafening, flare-lit Greek fortress atmosphere",
            "Orbelín Pineda's technical composure and playmaking vision in tight spaces"
        ],
        "known_vulnerabilities": [
            "Man-marking pressing scheme can be exploited by world-class quick-passing sides",
            "Tendency to concede counter-attacks when committing numbers forward"
        ],
        "key_players": [
            {"name": "Levi García", "role": "Explosive Powerhouse Forward", "impact": "Combines 36 km/h sprint speed with aerial power, scoring spectacular goals."},
            {"name": "Orbelín Pineda", "role": "Dynamic Mexican Midfield Orchestrator", "impact": "Controls play with 90% passing accuracy and exceptional press resistance."},
            {"name": "Frantzdy Pierrot", "role": "Towering Center-Forward", "impact": "A physical monster in the box who dominates aerial crosses and set-pieces."},
            {"name": "Niclas Eliasson", "role": "Pinpoint Right-Wing Crosser", "impact": "Leads the Greek league in assists, delivering lethal service to the front two."}
        ],
        "fan_perspective": "The OPAP Arena (Agia Sophia) in Nea Filadelfeia is an absolute cauldron. The yellow-and-black faithful create an electric, deafening spectacle with yellow flares, drums, and non-stop chanting. AEK fans have dreamed of Champions League football for years and treat every match as a matter of national and club pride.",
        "needs_to_advance": "Holding 3 points, AEK must target two home victories in Athens to reach the 9-to-10 point mark required to sneak into the Champions League knockout playoffs."
    },
    "Viking": {
        "league": "Eliteserien",
        "manager": "Bjarte Lunde Aarsheim",
        "formation": "4-3-3 High-Tempo Scandinavian Attack",
        "why_good": "Viking FK are the proud dark horses of Norwegian football. Under Bjarte Lunde Aarsheim, the Stavanger side plays an energetic, front-foot 4-3-3 system that thrives on aggressive wing play, direct running, and dangerous set-piece execution.\n\nZlatko Tripić is the undisputed talisman and emotional leader of the club. Operating on the left wing, Tripić possesses exceptional dead-ball delivery, visionary passing, and a fierce competitive drive that rallies his teammates in high-pressure moments.\n\nIn midfield, Australian international Gianni Stensness and Joe Bell provide defensive stability and tactical balance, allowing Lars-Jørgen Salvesen to lead the forward line with physical hold-up play and aerial goal threat.",
        "key_strengths": [
            "Zlatko Tripić's talismanic leadership, clutch goalscoring, and set-piece delivery",
            "High-energy pressing and physical duel strength across the pitch",
            "SR-Bank Arena's passionate, tight-knit Western Norwegian atmosphere"
        ],
        "known_vulnerabilities": [
            "Limited European depth when starters face fatigue against top-five league giants",
            "Defensive organization tested when opponents execute rapid switch passes"
        ],
        "key_players": [
            {"name": "Zlatko Tripić", "role": "Talismanic Left Winger & Captain", "impact": "Directly involved in 70% of Viking's European goals; lethal free-kick taker."},
            {"name": "Lars-Jørgen Salvesen", "role": "Physical Target Striker", "impact": "Wins aerial duels and anchors Viking's forward attacks with tireless running."},
            {"name": "Joe Bell", "role": "Midfield Conductor & Distributor", "impact": "Directs possession with 88% passing accuracy and smart positional play."},
            {"name": "Gianni Stensness", "role": "Imposing Center-Back & Anchor", "impact": "Brings physical authority and aerial dominance inside the penalty box."}
        ],
        "fan_perspective": "The SR-Bank Arena in Stavanger is filled with deep pride. Viking supporters have waited decades to hear the Champions League anthem echo across the fjords of Rogaland. The fans back Tripić and the boys with unconditional passion, treating every point as a monumental victory for Norwegian football.",
        "needs_to_advance": "Sitting on 3 points, Viking need to produce an extraordinary run—securing at least 7 points from their final 5 matches—to reach the 10-point playoff cutoff."
    },
    "Slovan Bratislava": {
        "league": "Slovak First Football League",
        "manager": "Vladimír Weiss",
        "formation": "4-3-3 Veteran Defensive Block",
        "why_good": "Vladimír Weiss has molded Slovan Bratislava into a battle-tested, deeply experienced defensive unit that refuses to yield easy chances to European heavyweights. Playing in a compact 4-3-3, Slovan sit in a disciplined mid-block and rely on tactical organization to frustrate high-powered attacks.\n\nIn midfield, 37-year-old Slovak legend Juraj Kucka provides immense physical power, leadership, and aerial dominance, while Danylo Ihnatenko acts as an aggressive ball-winning anchor. Marko Tolić brings creative flair and vision in the number 8/10 role.\n\nUp front, Tigran Barseghyan and David Strelec provide sharp counter-attacking danger, possessing the technical quality to convert half-chances from set-pieces and quick breaks.",
        "key_strengths": [
            "Juraj Kucka's veteran leadership, physical presence, and aerial dominance",
            "Deep defensive resilience and willingness to suffer without the ball",
            "Tehelné pole's electric, sold-out atmosphere in Bratislava"
        ],
        "known_vulnerabilities": [
            "Aging squad core struggles against high-tempo, continuous 90-minute pressing",
            "Difficulty sustaining prolonged attacking pressure against elite defenses"
        ],
        "key_players": [
            {"name": "Juraj Kucka", "role": "Legendary Midfield General", "impact": "Brings 100+ international caps, winning 70% of physical duels in midfield."},
            {"name": "David Strelec", "role": "Young Dynamic Center-Forward", "impact": "Scores clutch goals with sharp near-post runs and clever link-up play."},
            {"name": "Tigran Barseghyan", "role": "Wicked Left-Footed Right Winger", "impact": "Delivers dangerous curling crosses and possesses a venomous long-range shot."},
            {"name": "Guram Kashia", "role": "Veteran Central Defender & Captain", "impact": "Anchors the backline with aerial strength and disciplined positioning."}
        ],
        "fan_perspective": "Tehelné pole in Bratislava is a sea of sky-blue pride. For Slovak football fans, reaching the 36-club Champions League league phase is already a historic achievement. Supporters celebrate every tackle, block, and goal with immense emotion, proud to represent Slovakia against the giants of Europe.",
        "needs_to_advance": "Currently fighting on 1 point, Slovan's path to qualification requires pulling off monumental upsets in Bratislava to reach the elusive 9-to-10 point playoff threshold."
    },
    "LASK": {
        "league": "Austrian Bundesliga",
        "manager": "Markus Schopp",
        "formation": "3-4-3 High-Pressing Direct Attack",
        "why_good": "LASK play with the characteristic high-octane pressing intensity that defines Austrian football. Under Markus Schopp, the Linz side sets aggressive pressing traps in the middle third, forcing hurried turnovers before launching direct vertical counter-attacks.\n\nRobert Žulj is the technical leader and talisman of this team—a versatile playmaker who dictates tempo, scores spectacular edge-of-box goals, and threads pinpoint passes into the channels. Flanking him, Moses Usor provides explosive pace on the right wing.\n\nIn midfield, Valon Berisha brings experienced European leadership and ball-winning grit, while Philipp Ziereis commands a resilient three-man defense.",
        "key_strengths": [
            "Robert Žulj's technical brilliance, scoring instincts, and set-piece delivery",
            "Aggressive middle-third turnover traps and rapid vertical transitions",
            "Raiffeisen Arena's compact, intense Austrian home atmosphere"
        ],
        "known_vulnerabilities": [
            "Vulnerable to rapid diagonal switches that isolate their wide center-backs",
            "Can concede late goals when high-intensity pressing drops in final 15 minutes"
        ],
        "key_players": [
            {"name": "Robert Žulj", "role": "Talismanic Captain & Playmaker", "impact": "Leads LASK in goals, assists, and chances created; lethal from distance."},
            {"name": "Valon Berisha", "role": "Experienced Midfield Enforcer", "impact": "Wins loose balls and directs young players with veteran composure."},
            {"name": "Moses Usor", "role": "Electric Right Winger", "impact": "Stretches backlines with raw sprint speed and dangerous cutbacks."},
            {"name": "Philipp Ziereis", "role": "Defensive Anchor & Organizer", "impact": "Commands the back three with aerial clearances and calm clearances."}
        ],
        "fan_perspective": "The Raiffeisen Arena in Linz is an intimate, loud black-and-white stronghold. LASK supporters are fiercely proud of their club's European identity, having previously challenged top Premier League and Serie A clubs. Fans back Schopp's pressing style, believing that on their day in Linz, they can shock anyone.",
        "needs_to_advance": "Holding 2 points, LASK must target two victories from their remaining fixtures to enter the conversation for the 10-point playoff safety line."
    },
    "Sabah FK": {
        "league": "Azerbaijan Premier League",
        "manager": "Krunoslav Rendulić",
        "formation": "4-2-3-1 Disciplined Low Block & Break",
        "why_good": "Sabah FK are the fairy-tale qualifiers from Baku. Formed in 2017, the Azerbaijani club has achieved a miraculous rise into Europe's elite competition under Croatian tactician Krunoslav Rendulić.\n\nSabah play with an uncompromisingly disciplined low defensive block, packing the central areas of the pitch with Ivan Lepinjica and Elvin Camalov shielding the back four. In goal, Yusif Imanov has developed into a sensational young shot-stopper, leading the competition in saves.\n\nOn the counter-attack, Jamaican winger Kaheem Parris brings lightning 1v1 pace on the right flank, linking with Slovak striker Pavol Šafranko whose aerial hold-up play provides Sabah with a vital outlet under heavy pressure.",
        "key_strengths": [
            "Yusif Imanov's extraordinary reflex shot-stopping and tournament resilience",
            "Kaheem Parris's blistering sprint speed and dynamic transition running",
            "Fearless underdog mentality with zero pressure on their shoulders"
        ],
        "known_vulnerabilities": [
            "Limited possession against elite midfields forces extended defensive shifts",
            "Susceptible to continuous set-piece pressure from physical heavyweights"
        ],
        "key_players": [
            {"name": "Yusif Imanov", "role": "Heroic Goalkeeper & Shot-Stopper", "impact": "Leads all group stage goalkeepers with 18 saves across three intense ties."},
            {"name": "Kaheem Parris", "role": "Lightning Jamaican Right Winger", "impact": "The primary counter-attacking weapon, capable of out-sprinting European full-backs."},
            {"name": "Pavol Šafranko", "role": "Physical Target Center-Forward", "impact": "Battles against world-class center-backs, winning crucial aerial clearances."},
            {"name": "Ivan Lepinjica", "role": "Midfield Destroyer & Screen", "impact": "Blocks shooting lanes and anchors Sabah's low defensive block with discipline."}
        ],
        "fan_perspective": "Bank Respublika Arena in Masazır is witnessing history. For Sabah's passionate fans, being in the Champions League alongside Real Madrid and Bayern Munich is an unbelievable dream come true. The supporters roar with national pride behind Imanov and the boys, celebrating every tackle and point as a monument to Azerbaijani football.",
        "needs_to_advance": "With 1 point earned through a heroic draw, Sabah are playing with house money. Any additional points earned will be etched in gold in the club's history books."
    }
}

with open("data/team_dossiers.json", "w", encoding="utf-8") as f:
    json.dump(EXTENDED_DOSSIERS, f, indent=2, ensure_ascii=False)

print(f"Generated extended team dossiers for all {len(EXTENDED_DOSSIERS)} clubs!")
