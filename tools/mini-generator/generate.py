#!/usr/bin/env python3
"""
Daybreak Mini — offline puzzle-bank generator.

Builds a bank of verified 4x4 mini crosswords for the Daybreak briefing.
Every row and every column is a common 4-letter word (a "double word
square"), so every Across AND Down entry is a real, clue-able word. Each
entry is re-checked against the system dictionary before a puzzle ships.

This runs ONCE (or on refill) to produce briefing/minis/NN.html. NOTHING
here runs at briefing time — the routine only picks a pre-built file.

Grid: 4x4, no blocks. Across = the 4 rows; Down = the 4 columns.

Usage:  python3 generate.py [COUNT]          (default 20)
        python3 generate.py --bigtest        (solver self-test, full dict)
Output: ../../briefing/minis/01.html ...  plus a report to stdout.
"""
import sys, os, random, html

N = 4
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(os.path.join(HERE, "..", "..", "briefing", "minis"))
SYS_DICT = "/usr/share/dict/words"

# --- Curated clued 4-letter words (UPPERCASE). Clues are short and factual. ---
W4 = {
    "AREA": "Region or zone", "IDEA": "Bright thought", "OPEN": "Not shut",
    "ECHO": "Reflected sound", "OMEN": "Sign of things to come", "OVEN": "Baking appliance",
    "EPIC": "Grand and heroic", "OBOE": "Double-reed instrument", "ALOE": "Soothing plant",
    "ANTE": "Poker starter", "OATH": "Solemn promise", "ODOR": "Smell",
    "OGRE": "Fairy-tale brute", "OPAL": "Iridescent gem", "ORCA": "Killer whale",
    "ARIA": "Opera solo", "ACRE": "Land measure", "AMEN": "End of a prayer",
    "ATOM": "Tiny particle", "AUTO": "Car, informally", "AXLE": "Wheel rod",
    "EASE": "Lack of difficulty", "EDIT": "Revise text", "EMIT": "Give off",
    "ETCH": "Engrave with acid", "EXAM": "Test", "EXIT": "Way out",
    "IRIS": "Eye's colored part", "IRON": "Press clothes", "ISLE": "Small island",
    "ITEM": "Entry on a list", "ONCE": "A single time", "ONYX": "Black gemstone",
    "OOZE": "Seep slowly", "ORAL": "Spoken, not written", "USED": "Secondhand",
    "USER": "One who logs in", "ACID": "Sour compound", "AGED": "Grown old",
    "ALTO": "Low female voice", "ARCH": "Curved doorway", "AUNT": "Family relative",
    "BOLD": "Daring", "CALM": "Serene", "CITY": "Urban center",
    "COIN": "Bit of change", "DAWN": "Daybreak", "DEAL": "Business agreement",
    "DUNE": "Sand hill", "EARN": "Work for pay", "GOLD": "Precious metal",
    "HERO": "Brave figure", "LAKE": "Inland water", "LIME": "Green citrus",
    "MOON": "Night light", "NEST": "Bird's home", "NOTE": "Brief message",
    "OKRA": "Gumbo vegetable", "PARK": "Green public space", "ROSE": "Thorny flower",
    "SNOW": "Winter flurries", "STAR": "Twinkler in the sky", "TIDE": "Ocean's rise and fall",
    "TREE": "Leafy plant", "WAVE": "Ocean swell", "WIND": "Moving air",
    "ROAD": "Route for cars", "RAIN": "Wet weather", "SEAL": "Arctic swimmer",
    "SAND": "Beach grains", "SALT": "Table seasoning", "MILE": "5,280 feet",
    "BEAR": "Woodland giant", "BOAT": "Water craft", "CAKE": "Birthday treat",
    "CARD": "Deck member", "CAVE": "Rocky hollow", "COAT": "Winter wear",
    "CORN": "Cob crop", "DESK": "Office table", "DISH": "Serving plate",
    "DOOR": "Room entrance", "DOVE": "Peace bird", "DRUM": "Beaten instrument",
    "FERN": "Shade plant", "FISH": "Gilled swimmer", "FLAG": "Nation's banner",
    "FROG": "Pond hopper", "GATE": "Fence opening", "GOAT": "Horned climber",
    "HAND": "End of an arm", "HILL": "Small rise", "KING": "Chess piece",
    "KITE": "Windy-day flier", "LAMP": "Light source", "LEAF": "Tree bit",
    "LION": "Savanna cat", "MASK": "Face cover", "MAZE": "Puzzle of paths",
    "MOTH": "Lamp-drawn insect", "NAIL": "Hammer target", "OWL": "",
    "PALM": "Beach tree", "PEAR": "Bell-shaped fruit", "PLUM": "Purple fruit",
    "POND": "Small lake", "RICE": "Grain in a paddy", "RING": "Finger band",
    "ROCK": "Solid stone", "ROOF": "House top", "ROOT": "Underground part",
    "SAIL": "Boat's canvas", "SHIP": "Ocean vessel", "SHOE": "Foot cover",
    "SILK": "Smooth fabric", "SOAP": "Bath bar", "SOCK": "Foot cover",
    "SOFA": "Living-room seat", "SONG": "Tune with words", "SOUP": "Bowl starter",
    "SWAN": "Graceful bird", "TENT": "Camper's shelter", "VASE": "Flower holder",
    "WOLF": "Pack hunter", "YARN": "Knitter's thread", "ZERO": "Nothing at all",
    "BELL": "Ringer in a tower", "BIRD": "Feathered flier", "BONE": "Skeleton part",
    "BOOK": "Bound pages", "CLAY": "Potter's material", "CLUE": "Detective's hint",
    "CROW": "Cawing bird", "DUCK": "Pond paddler", "FIRE": "Campfire blaze",
    "GEM": "", "GLOW": "Soft light", "HALO": "Angel's ring",
    "HIVE": "Bee home", "IDOL": "Adored star", "JADE": "Green stone",
    "LEAD": "Pencil core", "MENU": "List of dishes", "MINT": "Cool herb",
    "MOSS": "Damp-rock green", "OPAL2": "", "PATH": "Walking route",
    "PINE": "Evergreen tree", "POEM": "Verse work", "RUBY": "Red gem",
    "SAGE": "Wise one", "SEED": "Plant start", "TALE": "Story",
    "VINE": "Climbing plant", "WING": "Bird's limb", "WOOD": "Log material",
    "BLUE": "Sky color", "NAVY": "Dark blue", "TEAL": "Blue-green",
    "COLD": "Chilly", "WARM": "Cozy", "COOL": "Mildly cold",
    "WIDE": "Broad", "TALL": "High up", "THIN": "Not thick",
    "SOFT": "Not hard", "FAST": "Speedy", "SLOW": "Not fast",
    "LOUD": "Noisy", "NEAT": "Tidy", "KIND": "Considerate",
    "WISE": "Sage", "PURE": "Unmixed", "RARE": "Uncommon",
    "REAL": "Genuine", "TRUE": "Accurate", "FREE": "At no cost",
    "TINY": "Very small", "VAST": "Huge", "EASY": "Not hard",
    "OPUS": "Musical work", "GURU": "Expert guide", "HALT": "Bring to a stop",
    "IDLE": "Not in use", "JEEP": "Rugged vehicle", "KELP": "Ocean seaweed",
    "LOFT": "Attic space", "MELON": "", "MULE": "Stubborn animal",
    "OMIT": "Leave out", "PACE": "Walking speed", "QUIZ": "Short test",
    "REEF": "Coral ridge", "TUNA": "Sandwich fish", "VETO": "Reject a bill",
}
# Larger pool of recognizable (some less-common) 4-letter words, to make proper
# (Across != Down) grids plentiful. Anything missing from the system dictionary
# is dropped automatically at load, so bulk additions are safe.
W4_MORE = {
    "BAND": "Music group", "BANK": "Money holder", "BARN": "Farm building",
    "BASE": "Bottom support", "BEAM": "Ray of light", "BEAN": "Chili legume",
    "BELT": "Waist strap", "BOMB": "Explosive device", "BOOT": "Ankle footwear",
    "BOSS": "Head honcho", "BOWL": "Cereal dish", "BULB": "Light globe",
    "BUSH": "Shrub", "CAGE": "Zoo enclosure", "CAMP": "Site of tents",
    "CANE": "Walking stick", "CART": "Wheeled basket", "CASE": "Container",
    "CASH": "Bills and coins", "CAST": "A play's actors", "CHEF": "Kitchen boss",
    "CHIN": "Face's bottom", "CLIP": "Paper fastener", "CLUB": "Golfer's tool",
    "COAL": "Black fuel", "COLT": "Young horse", "COOK": "Meal maker",
    "COVE": "Small bay", "CRAB": "Clawed crustacean", "CREW": "Ship's team",
    "CROP": "Harvest yield", "CUBE": "Six-sided shape", "CURB": "Street edge",
    "DART": "Thrown point", "DATE": "Calendar day", "DECK": "Ship's floor",
    "DEER": "Forest grazer", "DIAL": "Clock's face", "DIET": "Eating plan",
    "DIRT": "Loose soil", "DOCK": "Boat's berth", "DOLL": "Toy figure",
    "DOME": "Rounded roof", "DUST": "Fine dirt", "FACE": "Front of the head",
    "FAIR": "County carnival", "FARM": "Crop land", "FAWN": "Baby deer",
    "FILM": "Movie", "FIST": "Clenched hand", "FLAT": "Level",
    "FLEA": "Tiny pest", "FLOW": "Stream along", "FOAM": "Bath bubbles",
    "FOAL": "Baby horse", "FOLD": "Bend over", "FONT": "Type style",
    "FOOD": "Meal fuel", "FOOT": "Ankle's base", "FORK": "Dining utensil",
    "FORM": "Shape", "FORT": "Stronghold", "FUEL": "Gas or coal",
    "FUND": "Money pool", "GALE": "Strong wind", "GANG": "Rowdy group",
    "GEAR": "Equipment", "GERM": "Tiny microbe", "GIFT": "Present",
    "GLEN": "Small valley", "GLUE": "Sticky stuff", "GOAL": "Soccer target",
    "GOWN": "Formal dress", "GRIP": "Firm hold", "GULF": "Large bay",
    "GUST": "Wind blast", "HALL": "Corridor", "HARE": "Fast hopper",
    "HARM": "Do damage", "HAWK": "Sharp-eyed bird", "HAZE": "Light mist",
    "HEAP": "Untidy pile", "HEAT": "Warmth", "HEEL": "Foot's back",
    "HELM": "Ship's wheel", "HERB": "Cooking plant", "HIDE": "Conceal",
    "HOOF": "Horse's foot", "HOOK": "Fishing bend", "HORN": "Bull's point",
    "HOSE": "Garden tube", "HOST": "Party giver", "HUNT": "Pursue game",
    "HYMN": "Church song", "JAIL": "Lockup", "JAZZ": "Improv music",
    "JURY": "Court panel", "KALE": "Leafy green", "KNEE": "Leg joint",
    "KNOT": "Rope tie", "LACE": "Shoe string", "LAMB": "Young sheep",
    "LANE": "Narrow road", "LAVA": "Molten rock", "LAWN": "Grassy yard",
    "LENS": "Camera glass", "LIMB": "Tree branch", "LOAF": "Bread unit",
    "LOCK": "Key's target", "LONE": "Solitary", "LORD": "Noble title",
    "LUNG": "Breathing organ", "LURE": "Fishing bait", "MALL": "Shopping center",
    "MANE": "Lion's hair", "MEAL": "Food sitting", "MEAT": "Butcher's cut",
    "MESH": "Net fabric", "MIST": "Fine spray", "MOAT": "Castle ditch",
    "MODE": "Method or style", "MOLD": "Damp fungus", "MOOD": "State of mind",
    "NECK": "Head's support", "NODE": "Network point", "NOON": "Midday",
    "NOSE": "Face's smeller", "NOUN": "Naming word", "PACT": "Agreement",
    "PAIL": "Sand bucket", "PAIN": "Ache", "PAIR": "Twosome",
    "PANE": "Window glass", "PAWN": "Chess piece", "PEAK": "Mountaintop",
    "PEEL": "Fruit skin", "PIER": "Seaside dock", "PILE": "Heap",
    "PILL": "Medicine dose", "PIPE": "Water tube", "PLOT": "Story line",
    "PLOW": "Field tool", "PLUG": "Outlet fitter", "POLE": "Long rod",
    "POLL": "Opinion survey", "POOL": "Swimming spot", "PORT": "Harbor",
    "POSE": "Model's stance", "PRAY": "Say grace", "PREY": "Hunter's target",
    "PROP": "Stage item", "PUMP": "Air pusher", "RACE": "Speed contest",
    "RACK": "Storage frame", "RAFT": "River float", "RAGE": "Fury",
    "RAIL": "Track bar", "RAMP": "Incline", "RANK": "Military level",
    "RANT": "Angry tirade", "RATE": "Speed or price", "REED": "Marsh plant",
    "REIN": "Horse strap", "RENT": "Monthly payment", "RIND": "Cheese skin",
    "RISE": "Go up", "ROAM": "Wander", "ROBE": "Bathrobe",
    "ROLE": "Actor's part", "ROPE": "Thick cord", "RUIN": "Wreck",
    "RUNG": "Ladder step", "RUST": "Iron's flaking", "SASH": "Window frame",
    "SCAR": "Old wound mark", "SEAM": "Sewn join", "SHED": "Garden hut",
    "SHIN": "Lower leg", "SHOT": "Attempt", "SIGN": "Notice board",
    "SINK": "Kitchen basin", "SITE": "Location", "SKIN": "Body cover",
    "SLED": "Snow ride", "SLOT": "Narrow opening", "SNAP": "Quick break",
    "SOIL": "Garden dirt", "SOLE": "Shoe bottom", "SPUR": "Rider's prod",
    "STEM": "Plant stalk", "STEW": "Simmered dish", "SURF": "Ride waves",
    "TAIL": "Rear end", "TANK": "Water holder", "TARP": "Cover sheet",
    "TASK": "Chore", "TEAM": "Sports side", "TEXT": "Phone message",
    "TILE": "Floor square", "TOAD": "Warty hopper", "TOLL": "Bridge fee",
    "TOMB": "Burial vault", "TOOL": "Handy implement", "TRAP": "Snare",
    "TRAY": "Serving board", "TRIM": "Cut back", "TUBE": "Hollow cylinder",
    "TUNE": "Melody", "TUSK": "Elephant tooth", "TWIG": "Small branch",
    "VEIL": "Face cover", "VEIN": "Blood tube", "VERB": "Action word",
    "VEST": "Sleeveless top", "WAGE": "Weekly pay", "WAND": "Magic stick",
    "WARD": "Hospital section", "WART": "Skin bump", "WASP": "Stinging insect",
    "WEED": "Garden pest", "WELL": "Water source", "WHIP": "Lash",
    "WICK": "Candle string", "WIRE": "Metal thread", "WOOL": "Sheep's coat",
    "WORM": "Soil crawler", "WRAP": "Cover up", "YARD": "Lawn area",
    "YOLK": "Egg center", "ZONE": "Marked area", "GEAR2": "",
}
W4.update(W4_MORE)
# strip placeholder empties and wrong lengths
W4 = {k: v for k, v in W4.items() if v and len(k) == 4}


def load_sysdict():
    words = set()
    try:
        with open(SYS_DICT) as f:
            for line in f:
                w = line.strip().upper()
                if w.isalpha():
                    words.add(w)
    except OSError:
        pass
    return words

SYS = load_sysdict()

def prune_wordlist():
    """Remove typos (hard error) and words not in the system dictionary (drop)."""
    typos = [w for w in W4 if len(w) != 4 or not w.isalpha()]
    if typos:
        print("ABORT — malformed curated words:", typos); sys.exit(1)
    missing = sorted(w for w in W4 if SYS and w not in SYS)
    for w in missing:
        del W4[w]
    if missing:
        print(f"Dropped {len(missing)} words not in system dict: {missing}")

WORDS = sorted(W4)

def prefixes(words):
    p = set()
    for w in words:
        for i in range(1, len(w) + 1):
            p.add(w[:i])
    return p

PRE = prefixes(WORDS)

def col_ok(letters):
    if letters == "":
        return True
    if len(letters) < N:
        return letters in PRE
    return letters in set(WORDS)

WORDSET = set(WORDS)

def solve(rng, want, seen):
    grid = {}
    results = []
    accepted = []  # word-sets of accepted puzzles, for a variety cap

    def columns_ok(upto_row):
        for c in range(N):
            s = "".join(grid[(r, c)] for r in range(upto_row + 1))
            if len(s) < N:
                if s not in PRE:
                    return False
            else:
                if s not in WORDSET:
                    return False
        return True

    def place(row):
        if len(results) >= want:
            return
        if row == N:
            # Reject symmetric squares (Across == Down — degenerate crossword).
            if all(grid[(r, c)] == grid[(c, r)] for r in range(N) for c in range(N)):
                return
            gstr = "".join(grid[(r, c)] for r in range(N) for c in range(N))
            tstr = "".join(grid[(c, r)] for r in range(N) for c in range(N))
            canon = min(gstr, tstr)  # dedupe a grid and its transpose
            if canon in seen:
                return
            rows = ["".join(grid[(r, c)] for c in range(N)) for r in range(N)]
            cols = ["".join(grid[(r, c)] for r in range(N)) for c in range(N)]
            wset = set(rows) | set(cols)
            if any(len(wset & pw) > 3 for pw in accepted):
                return  # too similar to an already-chosen puzzle
            seen.add(canon)
            accepted.append(wset)
            results.append(dict(grid))
            return
        words = WORDS[:]
        rng.shuffle(words)
        for w in words:
            for c in range(N):
                grid[(row, c)] = w[c]
            if columns_ok(row):
                place(row + 1)
                if len(results) >= want:
                    return
            for c in range(N):
                grid.pop((row, c), None)

    place(0)
    return results

def entries_of(grid):
    num = {}
    n = 0
    across, down = [], []
    def isL(r, c):
        return 0 <= r < N and 0 <= c < N
    for r in range(N):
        for c in range(N):
            starts_a = (c == 0)
            starts_d = (r == 0)
            if starts_a or starts_d:
                n += 1
                num[(r, c)] = n
            if starts_a:
                cells = [(r, cc) for cc in range(N)]
                across.append((num[(r, c)], cells, "".join(grid[x] for x in cells)))
            if starts_d:
                cells = [(rr, c) for rr in range(N)]
                down.append((num[(r, c)], cells, "".join(grid[x] for x in cells)))
    return num, across, down

def clue_for(word):
    return (W4.get(word) or "").strip()

def render_html(grid, pid):
    num, across, down = entries_of(grid)
    for (_, _, w) in across + down:
        if SYS and w not in SYS:
            raise ValueError(f"puzzle {pid}: '{w}' not in system dictionary")
        if not clue_for(w):
            raise ValueError(f"puzzle {pid}: no clue for '{w}'")

    def grid_html(solved):
        cells = []
        for r in range(N):
            for c in range(N):
                nlabel = f'<span class="mini-num">{num[(r,c)]}</span>' if (r, c) in num else ''
                lspan = f'<span class="mini-let">{html.escape(grid[(r,c)])}</span>' if solved else ''
                cells.append(f'<div class="mini-cell">{nlabel}{lspan}</div>')
        return '<div class="mini-grid' + (' solved' if solved else '') + '">' + "".join(cells) + '</div>'

    def clue_list(entries):
        items = [f'<li><span class="cn">{nn}</span> {html.escape(clue_for(w))}</li>'
                 for (nn, _, w) in sorted(entries)]
        return "<ol>" + "".join(items) + "</ol>"

    out = [f'<div class="mini-wrap" data-mini-id="{pid:02d}">', grid_html(False),
           '<div class="mini-clues">',
           f'<div class="mini-col"><h4>Across</h4>{clue_list(across)}</div>',
           f'<div class="mini-col"><h4>Down</h4>{clue_list(down)}</div>', '</div>',
           '<details class="mini-answer"><summary>Show answers</summary>',
           grid_html(True), '</details>', '</div>']
    return "\n".join(out)

def bigtest():
    global WORDS, PRE, WORDSET
    WORDS = sorted(w for w in SYS if len(w) == N)
    PRE = prefixes(WORDS)
    WORDSET = set(WORDS)
    grids = solve(random.Random(1), 5, set())
    print(f"[bigtest] pool: {len(WORDS)} {N}-letter words -> {len(grids)} solutions")
    for g in grids[:2]:
        print("  " + " / ".join("".join(g[(r, c)] for c in range(N)) for r in range(N)))

def main():
    global WORDS, PRE, WORDSET
    if "--bigtest" in sys.argv:
        bigtest(); return
    want = int([a for a in sys.argv[1:] if a.isdigit()][0]) if any(a.isdigit() for a in sys.argv[1:]) else 20
    prune_wordlist()
    WORDS = sorted(W4)
    PRE = prefixes(WORDS)
    WORDSET = set(WORDS)
    print(f"Word pool: {len(WORDS)} clued 4-letter words")
    grids = solve(random.Random(20260727), want, set())
    os.makedirs(OUT_DIR, exist_ok=True)
    used = set()
    for i, g in enumerate(grids, 1):
        with open(os.path.join(OUT_DIR, f"{i:02d}.html"), "w") as f:
            f.write(render_html(g, i) + "\n")
        _, a, d = entries_of(g)
        used.update(w for (_, _, w) in a + d)
    print(f"Generated {len(grids)} puzzles into {OUT_DIR}")
    print(f"Unique answers used: {len(used)}")
    if len(grids) < want:
        print(f"NOTE: wanted {want}, produced {len(grids)} — add more words to W4 for variety.")

if __name__ == "__main__":
    main()
