import json

DOSSIERS = {
    "Paris Saint-Germain": {
        "league": "Ligue 1",
        "why_good": "Luis Enrique has forged PSG into a relentless collective pressing machine with electric wing dynamism. They dominate European matches through midfield control, suffocating territorial counter-pressing, and lethal direct incision through the channels.",
        "key_players": [
            {"name": "Ousmane Dembélé", "role": "Explosive 1v1 creator & primary chance generator"},
            {"name": "Bradley Barcola", "role": "Direct left-wing speedster & transition finisher"},
            {"name": "Vitinha", "role": "Metronomic midfield orchestrator & tempo regulator"},
            {"name": "Achraf Hakimi", "role": "Elite overlapping threat & wide playmaker"}
        ],
        "fan_perspective": "Parc des Princes is rocking. Having tasted ultimate European glory, supporters feel this collective, unselfish PSG is more dangerous than the superstar era ever was. Three straight wins have fans dreaming of back-to-back crowns.",
        "needs_to_advance": "Sitting perfect at 9 points (+9 GD), PSG need approximately 6 points from their remaining 5 fixtures to seal an automatic top-8 bye to the Round of 16."
    },
    "Aston Villa": {
        "league": "Premier League",
        "why_good": "Unai Emery's side are a masterclass in tactical discipline and structured transitions. Their synchronized mid-block and compact defensive lines bait opposition presses before springing explosive vertical counters through Watkins and Rogers.",
        "key_players": [
            {"name": "Ollie Watkins", "role": "Lethal direct striker & dynamic pressing focal point"},
            {"name": "Emiliano Martínez", "role": "World-class shot-stopper & penalty intimidating presence"},
            {"name": "Morgan Rogers", "role": "Ball-carrying midfield powerhouse"},
            {"name": "Youri Tielemans", "role": "Deep-lying playmaker with pinpoint line-breaking delivery"}
        ],
        "fan_perspective": "Villa Park is electric on European nights. To sit 2nd with 9 points from 3 games has supporters believing 1982 magic is alive. The belief under Emery is absolute—every match feels like a tactical clinic.",
        "needs_to_advance": "On 9 points (+9 GD), Villa are virtually assured of a playoff spot. Two wins from their remaining 5 games will comfortably lock in an historic automatic top-8 Round of 16 berth."
    },
    "Liverpool": {
        "league": "Premier League",
        "why_good": "Arne Slot's Liverpool blends high-octane Anfield intensity with supreme structural control. They concede few transition chances while retaining elite chance creation through inverted overloads and devastating wide finishing.",
        "key_players": [
            {"name": "Mohamed Salah", "role": "Iconic talisman & world-class decisive finisher"},
            {"name": "Virgil van Dijk", "role": "Commanding captain & peerless aerial defensive colossus"},
            {"name": "Ryan Gravenberch", "role": "Press-resistant midfield pivot & progressive carrier"},
            {"name": "Trent Alexander-Arnold", "role": "Generational passing range & dead-ball maestro"}
        ],
        "fan_perspective": "Anfield knows this competition intimately. With maximum points from the opening rounds, the Kop believes Slot's pragmatic control combined with European pedigree makes them genuine Champions League favorites.",
        "needs_to_advance": "With 9 points on the board, 2 more victories (6 points) will guarantee direct qualification to the Round of 16 and avoid the playoff minefield."
    },
    "Real Madrid": {
        "league": "La Liga",
        "why_good": "Carlo Ancelotti's kings of Europe possess unmatched clutch mentality and game-breaking individual firepower. Capable of soaking up immense pressure, their rapid vertical counters can dismantle any defense in seconds.",
        "key_players": [
            {"name": "Kylian Mbappé", "role": "Game-breaking speed & devastating central goal threat"},
            {"name": "Vinícius Júnior", "role": "World's most dangerous isolated 1v1 left-winger"},
            {"name": "Jude Bellingham", "role": "Box-to-box powerhouse & clutch late-box arrivee"},
            {"name": "Federico Valverde", "role": "Endless engine, tactical cover & long-range cannon"}
        ],
        "fan_perspective": "Madridistas view the Champions League as their birthright. Despite tough spells in games, the Bernabéu never doubts. Sitting on 9 points, the expectation is top seed and marching straight to the Budapest final.",
        "needs_to_advance": "On 9 points with a +5 GD, Real Madrid need 6 points from their remaining 5 fixtures to cement a top-8 finish and home advantage in the knockout rounds."
    },
    "Real Betis": {
        "league": "La Liga",
        "why_good": "Manuel Pellegrini has constructed a delightfully technical, fearless outfit. They play fluid associative football through the midfield pockets, moving opponents side to side before carving openings through intelligent interplay.",
        "key_players": [
            {"name": "Isco", "role": "Magical creative playmaker & tempo dictator"},
            {"name": "Giovani Lo Celso", "role": "Dynamic ball-progressor & clinical late runner"},
            {"name": "Pablo Fornals", "role": "High-workrate attacking midfielder with sharp link-up play"},
            {"name": "Rui Silva", "role": "Steely goalkeeper adept at close-range reaction saves"}
        ],
        "fan_perspective": "The Benito Villamarín is dreaming big. A perfect 9-point start has Béticos euphoric. Supporters know they are underdogs on paper, but their technical courage is proving they belong on Europe's grandest stage.",
        "needs_to_advance": "9 points already puts Betis within touching distance of the playoffs. 5 to 6 more points will remarkably fight for an automatic top-8 Round of 16 ticket."
    },
    "VfB Stuttgart": {
        "league": "Bundesliga",
        "why_good": "Sebastian Hoeneß's Stuttgart play some of the most eye-catching, aggressive positional football in Europe. High pressing, brave rest-defense, and fluid rotations between the lines allow them to overwhelm opponents.",
        "key_players": [
            {"name": "Deniz Undav", "role": "Intelligent space-finder, link striker & clinical finisher"},
            {"name": "Enzo Millot", "role": "Technically gifted attacking midfielder with venomous burst"},
            {"name": "Angelo Stiller", "role": "Precision deep-lying distributor & tactical conductor"},
            {"name": "Alexander Nübel", "role": "Reliable sweeper-keeper with proactive distribution"}
        ],
        "fan_perspective": "After years in the wilderness, Stuttgart supporters are relishing every European minute. 7 points from 3 matches has Cannstatt believing they can upset any European royalty on their day.",
        "needs_to_advance": "Currently on 7 points, Stuttgart require about 8 more points (2 wins, 2 draws) from 5 matches for Top 8, while a single win (3 pts) virtually locks in a top-24 playoff spot."
    },
    "Arsenal": {
        "league": "Premier League",
        "why_good": "Mikel Arteta has built arguably Europe's most suffocating defensive structure alongside set-piece lethality. Arsenal choke opponents in their own half, rarely conceding high-quality xG while controlling territory completely.",
        "key_players": [
            {"name": "Bukayo Saka", "role": "Right-wing talisman with world-class decision making"},
            {"name": "Martin Ødegaard", "role": "Creative orchestrator & premier counter-pressing leader"},
            {"name": "William Saliba", "role": "Flawless recovery defender & elite one-on-one stopper"},
            {"name": "Declan Rice", "role": "Midfield colossus, ball-winner & set-piece delivery master"}
        ],
        "fan_perspective": "Gunners fans believe this is the season to break the European barrier. The squad has matured into hardened European contenders. At 7 points and undefeated, optimism at the Emirates is sky high.",
        "needs_to_advance": "On 7 points with a healthy +4 GD, two wins and a draw (7 points) from the remaining 15 on offer will guarantee top-8 safe passage to the Round of 16."
    },
    "Barcelona": {
        "league": "La Liga",
        "why_good": "Hansi Flick's Barcelona plays daring, aggressive football with a razor-sharp high defensive line and relentless counter-pressing. Their verticality and youthful fearlessness create torrential waves of attacking output.",
        "key_players": [
            {"name": "Lamine Yamal", "role": "Generational 17-year-old winger capable of magic from nothing"},
            {"name": "Robert Lewandowski", "role": "Iconic penalty-box predator & lethal goalscorer"},
            {"name": "Raphinha", "role": "High-intensity pressing dynamo & direct transition goal threat"},
            {"name": "Pedri", "role": "Silky midfield escape artist with pristine vision"}
        ],
        "fan_perspective": "Culés are energized by Flick's dynamic, fast-paced identity. Lamine Yamal's brilliance makes every fixture an event. With 6 points from 3 games, fans are eager to seal a top-8 spot without playoff drama.",
        "needs_to_advance": "On 6 points with a strong +5 GD, Barcelona need roughly 9 points (3 wins) from their remaining 5 fixtures to clinch an automatic Round of 16 seed."
    },
    "Como": {
        "league": "Serie A",
        "why_good": "Cesc Fàbregas has instilled an ultra-brave, proactive possession style reminiscent of modern Spanish sides. Como invite pressure to play through lines with quick short passing and creative third-man runs.",
        "key_players": [
            {"name": "Nico Paz", "role": "Prodigious playmaking prodigy with exceptional technical flair"},
            {"name": "Patrick Cutrone", "role": "Passionate captain & relentless pressing spearhead"},
            {"name": "Sergi Roberto", "role": "Veteran European winner providing midfield composure"},
            {"name": "Gabriel Strefezza", "role": "Tricky wide dribbler with explosive acceleration"}
        ],
        "fan_perspective": "Como's European adventure is pure fairy-tale territory. Overlooking Lake Como, fans can barely believe they sit 9th in the Champions League table with 6 points. Survival was the goal; now playoffs are the target.",
        "needs_to_advance": "Sitting on 6 points, Como need just 4 to 5 more points (1 win, 2 draws) from their final 5 fixtures to achieve an unprecedented top-24 playoff qualification."
    },
    "Manchester City": {
        "league": "Premier League",
        "why_good": "Pep Guardiola's machine remains the benchmark for positional mastery, territorial strangulation, and goal-scoring inevitability. Their ability to pin opponents inside their 18-yard box is unmatched globally.",
        "key_players": [
            {"name": "Erling Haaland", "role": "Unstoppable physical phenomenon & ruthless scoring machine"},
            {"name": "Kevin De Bruyne", "role": "Generational playmaker capable of piercing any defensive block"},
            {"name": "Rodri", "role": "The heartbeat of the team, elite ball-winner & tactical brain"},
            {"name": "Phil Foden", "role": "Incisive pocket player with world-class close control"}
        ],
        "fan_perspective": "City fans take European knockout football for granted. 6 points from 3 matches is considered a solid platform, and supporters fully expect Haaland and company to hit top gear as winter approaches.",
        "needs_to_advance": "On 6 points with +4 GD and an immense 2306 Elo, winning 3 of their final 5 matches will comfortably secure an automatic top-8 bye."
    },
    "Club Brugge": {
        "league": "Belgian Pro League",
        "why_good": "Brugge play an energetic, technically balanced system that thrives when testing bigger European clubs. Their defensive cohesion paired with quick vertical outlets makes them a tricky opponent for any giant.",
        "key_players": [
            {"name": "Hans Vanaken", "role": "Towering midfield general, aerial threat & tactical anchor"},
            {"name": "Andreas Skov Olsen", "role": "Dangerous cutting-in right winger with a wicked left foot"},
            {"name": "Christos Tzolis", "role": "Direct, goal-scoring winger with blistering acceleration"},
            {"name": "Simon Mignolet", "role": "Experienced shot-stopper with big-game European pedigree"}
        ],
        "fan_perspective": "Jan Breydel Stadion is buzzing. Sitting 11th with 6 points from 3 games has Belgian fans dreaming of shocking Europe again. The supporters believe a playoff berth is now firmly in their own hands.",
        "needs_to_advance": "With 6 points banked, Brugge require only 4 more points (e.g. 1 win, 1 draw) from their last 5 fixtures to cement their spot in the top 24."
    },
    "Sporting CP": {
        "league": "Primeira Liga",
        "why_good": "Sporting play a high-octane 3-4-3 system characterized by ferocious wing-back aggression, rock-solid central defending, and the most lethal central striker in European club football.",
        "key_players": [
            {"name": "Viktor Gyökeres", "role": "Bulldozing forward with unplayable power, pace & finishing"},
            {"name": "Morten Hjulmand", "role": "Tenacious midfield captain & defensive screen"},
            {"name": "Francisco Trincão", "role": "Inventive wide playmaker with sublime technical skill"},
            {"name": "Gonçalo Inácio", "role": "Left-footed ball-playing defender with elite distribution"}
        ],
        "fan_perspective": "Sporting fans believe Gyökeres gives them a puncher's chance against anyone on the continent. With 6 points from 3 games, Alvalade is confident of reaching at least the playoff seeded positions.",
        "needs_to_advance": "Sitting on 6 points, Sporting are 8 to 9 points away from automatic top-8 qualification, and just 4 points away from sealing a top-24 playoff berth."
    },
    "Borussia Dortmund": {
        "league": "Bundesliga",
        "why_good": "Dortmund boast immense European pedigree, thriving in chaotic, transition-heavy encounters. The Yellow Wall turns the Westfalenstadion into a fortress where momentum can overwhelm even the stiffest opposition.",
        "key_players": [
            {"name": "Serhou Guirassy", "role": "Intelligent focal point striker with clinical box presence"},
            {"name": "Julian Brandt", "role": "Creative hub capable of game-opening through-balls"},
            {"name": "Karim Adeyemi", "role": "Blistering pace merchant who punishes high defensive lines"},
            {"name": "Nico Schlotterbeck", "role": "Aggressive front-foot center-back with elite passing range"}
        ],
        "fan_perspective": "Following their recent run to Wembley, Dortmund fans know how to navigate this tournament. Sitting on 6 points, supporters expect a top-8 push and dread the coin-flip of playoff ties.",
        "needs_to_advance": "6 points from 3 matches is a solid start. Dortmund need 9 points from their remaining 5 fixtures to avoid the playoff round and proceed straight to the Round of 16."
    },
    "Bayern Munich": {
        "league": "Bundesliga",
        "why_good": "Vincent Kompany has restored Bayern's terrifying, hyper-aggressive counter-pressing game. They suffocatingly pin opponents in their half and generate enormous chance volumes through Kane's link-up and Musiala's wizardry.",
        "key_players": [
            {"name": "Harry Kane", "role": "Complete world-class #9: elite finisher & deep distributor"},
            {"name": "Jamal Musiala", "role": "Untouchable dribbling maestro in tight central spaces"},
            {"name": "Michael Olise", "role": "Sensational inverted winger with wicked set-piece delivery"},
            {"name": "Joshua Kimmich", "role": "Midfield orchestrator and tactical compass"}
        ],
        "fan_perspective": "With the final being hosted at their own Allianz Arena in Munich, Bayern fans view reaching the final as non-negotiable. 5 points from 3 games is slightly under par, so fans demand an immediate surge.",
        "needs_to_advance": "On 5 points with a massive +5 GD and 2281 Elo rating, Bayern need 10 points (3 wins, 1 draw) from their remaining 5 matches to secure a top-8 bye."
    },
    "Roma": {
        "league": "Serie A",
        "why_good": "Roma are a streetwise, physically combative European tournament team. They excel in tight, low-scoring contests where tactical discipline, set-piece execution, and individual moments of brilliance decide outcomes.",
        "key_players": [
            {"name": "Paulo Dybala", "role": "World-class mercurial genius who unlocks low defensive blocks"},
            {"name": "Artem Dovbyk", "role": "Physical target-man & relentless penalty-box presence"},
            {"name": "Lorenzo Pellegrini", "role": "Captain & dead-ball specialist with European pedigree"},
            {"name": "Gianluca Mancini", "role": "Aggressive, battle-hardened defensive leader"}
        ],
        "fan_perspective": "The Curva Sud lives for European nights under the lights at the Stadio Olimpico. With 4 points and +3 GD, Romanisti believe they have the grit to reach the knockout rounds once Dybala is fit.",
        "needs_to_advance": "Sitting on 4 points, Roma need 6 more points (2 wins) from their final 5 matches to comfortably guarantee a top-24 playoff spot."
    },
    "Atletico Madrid": {
        "league": "La Liga",
        "why_good": "Diego Simeone's Atletico remain Europe's most resilient defensive nightmare, now supplemented by world-class attacking quality. Their compact 5-man low block and ruthless counter-attacks make them venomous.",
        "key_players": [
            {"name": "Antoine Griezmann", "role": "Footballing visionary, tactical leader & decisive finisher"},
            {"name": "Julián Álvarez", "role": "Relentless pressing predator with world-class instincts"},
            {"name": "Jan Oblak", "role": "World-class goalkeeper capable of miracle saves"},
            {"name": "Rodrigo De Paul", "role": "Combative midfield warrior & transition launcher"}
        ],
        "fan_perspective": "Colchoneros are hungry for European redemption. 4 points from 3 matches leaves room for improvement, but the Metropolitano faithful know nobody wants to draw Atleti in a two-legged knockout.",
        "needs_to_advance": "With 4 points in hand and an elite 2095 Elo, Atletico are heavily favored in their remaining fixtures to collect the 6 to 7 points needed for safe playoff passage."
    },
    "Shakhtar Donetsk": {
        "league": "Ukrainian Premier League",
        "why_good": "Shakhtar showcase extraordinary technical bravery, playing fluid, expansive attacking football despite immense logistical adversity. Their young talents play with high speed and fearless combination play.",
        "key_players": [
            {"name": "Georgiy Sudakov", "role": "Elite playmaking talent with razor-sharp vision & passing"},
            {"name": "Danylo Sikan", "role": "Hard-working mobile striker with opportunistic finishing"},
            {"name": "Mykola Matviyenko", "role": "Calm, experienced ball-playing central defender"},
            {"name": "Dmytro Riznyk", "role": "Agile goalkeeper tested often in big European ties"}
        ],
        "fan_perspective": "Shakhtar are playing for an entire nation. Every point earned on the road is greeted with immense pride. Sitting 17th with 4 points, Ukrainian fans believe qualifying for the playoffs is well within reach.",
        "needs_to_advance": "On 4 points with a +1 GD, Shakhtar need 6 points from their remaining 5 fixtures (likely 2 wins) to seal a top-24 playoff berth."
    },
    "PSV Eindhoven": {
        "league": "Eredivisie",
        "why_good": "Peter Bosz has made PSV one of Europe's most prolific attacking sides. They commit bodies forward in devastating numbers, utilizing vertical overloads and relentless high-tempo counter-pressing.",
        "key_players": [
            {"name": "Luuk de Jong", "role": "Europe's most dangerous aerial target-man & veteran captain"},
            {"name": "Johan Bakayoko", "role": "Explosive young right-winger with dazzling 1v1 trickery"},
            {"name": "Joey Veerman", "role": "Exceptional passing metronome & set-piece deliverer"},
            {"name": "Jerdy Schouten", "role": "Midfield stabilizer who cleans up opponent transition attempts"}
        ],
        "fan_perspective": "Philips Stadion believes Bosz's fearless attack can score against any defense in the world. 4 points from 3 games keeps them well alive, and supporters expect to comfortably make the playoff round.",
        "needs_to_advance": "With 4 points and neutral GD, PSV require approximately 6 points (2 wins) from their final 5 league-phase matches to lock in a top-24 playoff berth."
    },
    "Villarreal": {
        "league": "La Liga",
        "why_good": "Marcelino has restored the Yellow Submarine's signature identity: razor-sharp 4-4-2 defensive compactness, swift horizontal ball circulation, and sudden vertical breakthroughs through dynamic wide forwards.",
        "key_players": [
            {"name": "Álex Baena", "role": "La Liga's premier assist provider with sublime creative vision"},
            {"name": "Ayoze Pérez", "role": "In-form clinical finisher with clever movement between lines"},
            {"name": "Gerard Moreno", "role": "Talismanic link-striker with exceptional technical class"},
            {"name": "Dani Parejo", "role": "Veteran midfield conductor with world-class distribution"}
        ],
        "fan_perspective": "Villarreal punches above its weight like no other town in Europe. With 3 points from 3 games, the Estadio de la Cerámica faithful know their upcoming home fixtures will determine whether they reach the playoffs.",
        "needs_to_advance": "Currently on 3 points, Villarreal need 7 points (2 wins, 1 draw) from their remaining 5 fixtures to reach the magic 10-point playoff safety mark."
    },
    "Inter": {
        "league": "Serie A",
        "why_good": "Simone Inzaghi's Inter are a tactically sublime 3-5-2 machine. Their automated passing patterns, rotating center-backs, and lethal strike partnership make them one of the most complete teams on the continent.",
        "key_players": [
            {"name": "Lautaro Martínez", "role": "World-class captain, tenacious presser & lethal box finisher"},
            {"name": "Nicolò Barella", "role": "Dynamo midfielder with boundless stamina & technical quality"},
            {"name": "Hakan Çalhanoğlu", "role": "Premier deep-lying playmaker & immaculate penalty taker"},
            {"name": "Alessandro Bastoni", "role": "Modern wide center-back who creates chances from the half-space"}
        ],
        "fan_perspective": "Interisti are not satisfied with 3 points from 3 games. As reigning Italian champions and 2023 finalists, the San Siro faithful expect an immediate reaction and a dominant run through the winter fixtures.",
        "needs_to_advance": "Holding an elite 2194 Elo rating, Inter are heavily favored in their remaining ties. Winning 3 of their last 5 matches (9 points) will vault them into the top 16, while 7 points secures the playoffs."
    },
    "Manchester United": {
        "league": "Premier League",
        "why_good": "United possess game-winning individual quality capable of turning any contest in an instant. When their midfield transitions click, their wing speed can punish any aggressive European high line.",
        "key_players": [
            {"name": "Bruno Fernandes", "role": "High-risk, high-reward talismanic creator & captain"},
            {"name": "Kobbie Mainoo", "role": "Press-resistant midfield prodigy with elite composure"},
            {"name": "Alejandro Garnacho", "role": "Direct, fearless winger with relentless vertical ambition"},
            {"name": "André Onana", "role": "Proactive ball-playing goalkeeper capable of miraculous saves"}
        ],
        "fan_perspective": "Old Trafford expects European nights of glory, but fans are on edge after taking 3 points from the first 3 games. Supporters know every remaining fixture is a must-win battle for knockout survival.",
        "needs_to_advance": "Sitting on 3 points with a -1 GD, United need at least 7 points (2 wins, 1 draw) from their remaining 5 matches to avoid the catastrophe of an early European exit."
    },
    "Napoli": {
        "league": "Serie A",
        "why_good": "Antonio Conte has injected fierce intensity, tactical rigor, and structural solidity into Napoli. They are suffocatingly organized defensively and clinical when unleashing Lukaku's hold-up play and Kvaratskhelia's wizardry.",
        "key_players": [
            {"name": "Khvicha Kvaratskhelia", "role": "Unpredictable dribbler with game-deciding individual magic"},
            {"name": "Romelu Lukaku", "role": "Imposing physical target-man & selfless focal point"},
            {"name": "Stanislav Lobotka", "role": "Press-resistant midfield pivot who dictates game flow"},
            {"name": "Alessandro Buongiorno", "role": "Dominant front-foot central defensive rock"}
        ],
        "fan_perspective": "Napoli fans adore Conte's fighting spirit. The Stadio Diego Armando Maradona is ready to erupt. On 3 points, Neapolitans believe their squad is far better than their rank suggests and expect a rapid climb.",
        "needs_to_advance": "On 3 points, Napoli need 7 points from their final 5 fixtures. Two home victories and an away draw will comfortably book their ticket to the knockout playoffs."
    },
    "LASK": {
        "league": "Austrian Bundesliga",
        "why_good": "LASK are an intensely hardworking, structured Austrian unit that relies on collective discipline, set-piece opportunities, and aggressive counter-pressing in midfield to frustrate superior opposition.",
        "key_players": [
            {"name": "Robert Zulj", "role": "Veteran playmaking talisman with clinical finishing ability"},
            {"name": "Sascha Horvath", "role": "Energetic midfield battler with sharp distribution"},
            {"name": "Philipp Ziereis", "role": "Organizing central defender who commands the backline"},
            {"name": "Jörg Siebenhandl", "role": "Experienced goalkeeper capable of high-volume shot stopping"}
        ],
        "fan_perspective": "Reaching the Champions League league phase was already historic for Linz. Sitting on 3 points after 3 games gives fans genuine hope of snatching a playoff spot.",
        "needs_to_advance": "LASK need roughly 7 points from their remaining 5 matches. Target fixtures at home will be vital if they are to squeeze into 24th place."
    },
    "Galatasaray": {
        "league": "Süper Lig",
        "why_good": "Galatasaray boast one of the most frightening attacking forward lines in Europe. Driven by the deafening cauldron of Rams Park, their front-foot pressing and world-class strike duo can dismantle any defense.",
        "key_players": [
            {"name": "Victor Osimhen", "role": "World-class explosive striker with uncontainable athletic power"},
            {"name": "Mauro Icardi", "role": "Instinctive penalty-box assassin with ice-cold finishing"},
            {"name": "Lucas Torreira", "role": "Bite-sized midfield pitbull who disrupts opposition rhythm"},
            {"name": "Barış Alper Yılmaz", "role": "Powerful, versatile winger who terrorizes full-backs"}
        ],
        "fan_perspective": "The Yellow-Red faithful believe this is their strongest squad in two decades. With Osimhen leading the line, Turkish supporters believe Rams Park can intimidate any visitor. 3 points leaves everything to play for.",
        "needs_to_advance": "Currently on 3 points with 51.5% top-24 odds, Galatasaray need 7 points (2 wins, 1 draw) from their remaining 5 fixtures to guarantee knockout football."
    },
    "Sabah FK": {
        "league": "Azerbaijan Premier League",
        "why_good": "Sabah are the ultimate underdogs, relying on a compact 5-4-1 low block, ferocious defensive commitment, and lightning-quick breaks through isolated forward outlets to scrap for every inch.",
        "key_players": [
            {"name": "Joy-Lance Mickels", "role": "Tricky transition winger with an eye for goal"},
            {"name": "Bojan Letić", "role": "Reliable set-piece specialist & disciplined left wing-back"},
            {"name": "Sofian Chakla", "role": "Towering central defender who wins crucial aerial duels"},
            {"name": "Yusif Imanov", "role": "Young shot-stopper with razor-sharp reflexes"}
        ],
        "fan_perspective": "Every goal and point earned in this Champions League campaign is celebrated as national history. Sitting on 3 points is already an incredible achievement that has fans dreaming of an unthinkable playoff miracle.",
        "needs_to_advance": "Sabah need an extraordinary 7 points from their remaining 5 fixtures against European heavyweights to have any mathematical chance of reaching 24th place."
    },
    "Feyenoord": {
        "league": "Eredivisie",
        "why_good": "Feyenoord play high-octane Dutch football powered by the cauldron of De Kuip. They utilize intense wing overloads, aggressive front-foot pressing, and fearless verticality into the channels.",
        "key_players": [
            {"name": "Quinten Timber", "role": "All-action midfield powerhouse with elite ball-carrying drive"},
            {"name": "Igor Paixão", "role": "Electric Brazilian winger with deadly long-range shooting"},
            {"name": "Santiago Giménez", "role": "Instinctive goalscorer who thrives on service into the box"},
            {"name": "Dávid Hancko", "role": "Exceptional left-footed center-back who organizes the defense"}
        ],
        "fan_perspective": "De Kuip under the floodlights is one of football's greatest atmospheres. 3 points from 3 matches leaves Feyenoord in the thick of the battle, and fans fully expect their home games to carry them through.",
        "needs_to_advance": "Holding a strong 1957 Elo rating and 92.6% top-24 odds, Feyenoord need 7 points from their final 5 matches to comfortably book a knockout playoff spot."
    },
    "Lens": {
        "league": "Ligue 1",
        "why_good": "Lens are a furiously energetic, tactically disciplined 3-4-2-1 collective. Backed by their passionate working-class fanbase, they press aggressively in packs and transition with ruthless efficiency.",
        "key_players": [
            {"name": "Brice Samba", "role": "Commanding captain & acrobatic shot-stopper"},
            {"name": "Florian Sotoca", "role": "Selfless, tactically intelligent pressing forward"},
            {"name": "Facundo Medina", "role": "Aggressive, ball-playing Argentine defender with elite grit"},
            {"name": "Andy Diouf", "role": "Dynamic central midfield engine with powerful ball-carrying"}
        ],
        "fan_perspective": "Stade Bollaert-Delelis is one of the loudest venues in France. The Sang et Or fans are proud of their team's fight. On 3 points, supporters believe their fortress can deliver the wins needed to reach the playoffs.",
        "needs_to_advance": "Lens need approximately 7 points from their remaining 5 fixtures. Winning their two home matches is essential to breaking into the top 24."
    },
    "Bodo/Glimt": {
        "league": "Eliteserien",
        "why_good": "The pride of northern Norway plays fearless, synchronized 4-3-3 attacking football on their artificial surface inside the Arctic Circle. Their rapid passing patterns and relentless running stun visiting European giants.",
        "key_players": [
            {"name": "Patrick Berg", "role": "Captain, midfield anchor & precision passing metronome"},
            {"name": "Jens Petter Hauge", "role": "Silky inverted left-winger with decisive finishing quality"},
            {"name": "Philip Zinckernagel", "role": "Experienced creative wide forward with set-piece quality"},
            {"name": "Kasper Høgh", "role": "Physical, hard-working center-forward who presses tirelessly"}
        ],
        "fan_perspective": "The Aspmyra Stadion is a fortress where European giants fear to tread in freezing winds. With 3 points banked and a 52.2% playoff probability, Glimt fans genuinely believe the Arctic fairy-tale will continue.",
        "needs_to_advance": "On 3 points, Bodo/Glimt need 7 points from their last 5 fixtures. Turning their home games in Bodø into victories is their golden ticket to the top 24."
    },
    "AEK Athens": {
        "league": "Super League Greece",
        "why_good": "Matías Almeyda has transformed AEK into a relentless, high-pressing Greek powerhouse. Driven by the suffocating atmosphere of the OPAP Arena, they play physical, transition-focused football.",
        "key_players": [
            {"name": "Levi García", "role": "Devastatingly fast and powerful striker who terrorizes center-backs"},
            {"name": "Orbelín Pineda", "role": "Agile Mexican midfielder with creative flair & high workrate"},
            {"name": "Domagoj Vida", "role": "Veteran Croatian warrior with vast European knockout experience"},
            {"name": "Petros Mantalos", "role": "Experienced playmaker with clutch European deliveries"}
        ],
        "fan_perspective": "Original 21 turns Nea Filadelfeia into an intimidating wall of yellow and black. Sitting on 3 points, Greek supporters know qualifying for the playoffs will require heroic performances against European elite.",
        "needs_to_advance": "AEK need 7 points from their remaining 5 matches. They will need to turn their home fortress into points to overcome the odds and reach 24th place."
    },
    "RB Leipzig": {
        "league": "Bundesliga",
        "why_good": "Leipzig possess blistering young talent capable of devastating transitional speed. While currently rebuilding roster balance, their vertical combinations and counter-pressing can punish any lapse in concentration.",
        "key_players": [
            {"name": "Xavi Simons", "role": "Electric attacking midfield prodigy with world-class creative output"},
            {"name": "Benjamin Šeško", "role": "Towering modern striker with elite physical speed and power"},
            {"name": "Loïs Openda", "role": "Rapid vertical forward who lives on the shoulder of defenders"},
            {"name": "Willi Orbán", "role": "Veteran defensive general who commands the backline"}
        ],
        "fan_perspective": "After a rocky European start with 3 points from 3 matches, Leipzig supporters know the squad has the individual talent to stage a dramatic recovery. The focus is entirely on securing a top-24 playoff berth.",
        "needs_to_advance": "Holding an Elo of 1793 and a 57.4% top-24 chance, Leipzig need 7 points (2 wins, 1 draw) from their final 5 fixtures to avoid an embarrassing early exit."
    },
    "Fenerbahce": {
        "league": "Süper Lig",
        "why_good": "Under José Mourinho, Fenerbahçe are a battle-hardened, pragmatic European outfit. They combine physical midfield dominance, disciplined defensive rest-structures, and clinical set-piece execution.",
        "key_players": [
            {"name": "Edin Džeko", "role": "Iconic veteran striker with world-class hold-up play & leadership"},
            {"name": "Dušan Tadić", "role": "Creative wizard with unmatched vision & delivery from the half-spaces"},
            {"name": "Fred", "role": "Tenacious midfield engine who drives team transitions"},
            {"name": "Dominik Livaković", "role": "World-class Croatian shot-stopper who shines in high-pressure games"}
        ],
        "fan_perspective": "Kadıköy believes in the Mourinho factor. While sitting 31st with 2 points looks daunting on the surface, fans know their remaining schedule features favorable clashes (at LASK, vs Villarreal). The yellow-and-navy faithful believe they are very much alive.",
        "needs_to_advance": "On 2 points, Fenerbahçe need 8 points from their remaining 5 matches (e.g. 2 wins, 2 draws) to reach the 10-point threshold that virtually guarantees top-24 playoff qualification."
    },
    "Slavia Praha": {
        "league": "Czech First League",
        "why_good": "Jindřich Trpišovský's Slavia are renowned across Europe as one of the most physically demanding, man-oriented pressing sides. They outwork opponents, dominate second balls, and thrive on high-intensity duels.",
        "key_players": [
            {"name": "Tomáš Chorý", "role": "Gigantic 6ft 6in target-man who dominates aerial battles"},
            {"name": "Lukáš Provod", "role": "Dynamic left-sided creator with thunderous shooting ability"},
            {"name": "Oscar Dorley", "role": "Tireless midfield presser with exceptional agility"},
            {"name": "Igoh Ogbu", "role": "Aggressive, physical central defender who excels in 1v1 duels"}
        ],
        "fan_perspective": "The Eden Arena always stands by their team. With just 1 point from 3 matches, supporters know the mountain is steep, but Slavia's famous work ethic means they will fight until the final whistle.",
        "needs_to_advance": "Slavia need an improbable 9 points (3 wins) from their last 5 fixtures to climb from 32nd into the top-24 playoff cut."
    },
    "Viking": {
        "league": "Eliteserien",
        "why_good": "Viking play an open, Scandinavian style characterized by high crossing volume, energetic midfield running, and set-piece inventiveness from out wide.",
        "key_players": [
            {"name": "Zlatko Tripić", "role": "Passionate captain, penalty specialist & emotional heartbeat"},
            {"name": "Lars-Jørgen Salvesen", "role": "Hard-working target striker who battles center-backs"},
            {"name": "Joe Bell", "role": "Composed midfield distributor who controls team tempo"},
            {"name": "Gianni Stensness", "role": "Tough-tackling Australian defender with aerial authority"}
        ],
        "fan_perspective": "Stavanger is proud to be on this stage, but 1 point from 3 games highlights the harsh reality of Europe's top table. Supporters want to see pride, courage, and at least one famous victory.",
        "needs_to_advance": "Sitting on 1 point with a -4 GD, Viking would need to win at least 3 of their remaining 5 fixtures against European royalty to stay alive."
    },
    "Porto": {
        "league": "Primeira Liga",
        "why_good": "Porto are historically one of the most dangerous, streetwise tournament sides in European history. They play with immense tactical aggression, pressing traps, and ferocious intensity at the Estádio do Dragão.",
        "key_players": [
            {"name": "Diogo Costa", "role": "World-class goalkeeper with peerless penalty-saving records"},
            {"name": "Galeno", "role": "Blistering left-winger with a lethal curling strike"},
            {"name": "Alan Varela", "role": "Classy Argentine holding midfielder who dictates game rhythm"},
            {"name": "Samu Omorodion", "role": "Terrifying physical forward with explosive speed and power"}
        ],
        "fan_perspective": "Porto fans are in shock to sit on 0 points after 3 games. However, with an elite 2004 Elo and 77.5% playoff odds, the Dragão faithful know that winning 3 of their final 5 matches will comfortably catapult them into the playoffs.",
        "needs_to_advance": "Despite 0 points, Porto's high Elo means they are favored in most remaining ties. Securing 9 to 10 points (3 wins, 1 draw) from their last 5 matches will punch their playoff ticket."
    },
    "Lille": {
        "league": "Ligue 1",
        "why_good": "Bruno Génésio has crafted a technically slick, tactically adaptable outfit capable of slaying giants (having beaten Real Madrid and Atletico previously). Their midfield technical security and swift wide combinations are top tier.",
        "key_players": [
            {"name": "Jonathan David", "role": "Clinical Canadian international striker with ice-cold finishing"},
            {"name": "Edon Zhegrova", "role": "Mercurial left-footed dribbler who can beat three defenders"},
            {"name": "Angel Gomes", "role": "Deep-lying English playmaker with sublime vision and press resistance"},
            {"name": "Lucas Chevalier", "role": "Phenomenal young French goalkeeper tipped for the very top"}
        ],
        "fan_perspective": "Stade Pierre-Mauroy is desperate to get off the mark after 3 narrow defeats. The supporters know this squad has defeated the best in Europe and refuse to concede their season is over.",
        "needs_to_advance": "On 0 points, Lille have zero margin for error. They must secure at least 9 to 10 points (minimum 3 wins) from their final 5 fixtures to claw their way into 24th place."
    },
    "Slovan Bratislava": {
        "league": "Slovak Super Liga",
        "why_good": "Vladimír Weiss's side are a veteran, resilient team built on defensive low-block compactness, veteran leadership, and opportunistic counter-attacks through experienced European campaigners.",
        "key_players": [
            {"name": "Vladimír Weiss Jr.", "role": "Mercurial veteran playmaker with supreme dribbling skills"},
            {"name": "Tigran Barseghyan", "role": "Dangerous cutting-in wide forward with a thunderous strike"},
            {"name": "Juraj Kucka", "role": "Warrior midfield veteran with vast Champions League experience"},
            {"name": "Dominik Takáč", "role": "Busy goalkeeper who has pulled off miraculous saves throughout qualifying"}
        ],
        "fan_perspective": "Tehelné pole has celebrated historic nights just reaching the 36-team stage. While 0 points and -12 GD shows the brutal step up in quality, fans are determined to savor every match and hunt for a historic point.",
        "needs_to_advance": "Sitting 36th with 0 points, Slovan are on the brink of mathematical elimination. Winning 3 or 4 matches from their final 5 would be required for an unprecedented miracle."
    }
}

with open("data/team_dossiers.json", "w", encoding="utf-8") as f:
    json.dump(DOSSIERS, f, indent=2, ensure_ascii=False)

print(f"Generated complete dossiers for {len(DOSSIERS)} clubs in data/team_dossiers.json")
