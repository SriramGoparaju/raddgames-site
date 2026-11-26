"""The words and facts on raddgames.com (build.py lays them out).

Keep every claim true to the build that is in players' hands. Each game's facts
come from its own project: Inkbloom (Projects/inkbloom, docs/store-listing.md),
Lumiwire (content_lumiwire.py, copied from lumiwire-site), Shapelings
(content_shapelings.py, copied from shapelings-site) and Loopo (PLAN.md 16, build 10).
"""
import content_lumiwire as lw
import content_shapelings as sh

SITE_NAME = "Radd Games"
SITE_ORIGIN = "https://raddgames.com"
SUPPORT_EMAIL = "support@raddgames.com"   # Cloudflare Email Routing -> the owner's inbox. Test it before go-live.
PUBLISHER = "Sriram Goparaju"
COUNTRY = "India"
YEAR = "2026"
MOVED = "26 November 2026"                # the day the legal pages moved to raddgames.com

# AdMob's line for every Radd Games app (one publisher account).
APP_ADS = "google.com, pub-8395918704114267, DIRECT, f08c47fec0942fa0"

TICKER = ["Four games", "Zero homework", "No ads mid-puzzle", "No sign-up", "One more level",
          "OK, one more", "Made in India", "Powered by tea"]

HOUSE_RULES = [
    ("No ads in the middle of a puzzle.",
     "Ads wait for a natural pause, like the end of a level. And every game lets you pay once to switch them off."),
    ("No sign-up. Not even a tiny one.",
     "No email, no password, no profile picture. Open the game and play."),
    ("Your data, your call.",
     "Every game says plainly what it collects and gives you a way to delete it. The links are at the bottom of every page."),
    ("A real person reads the inbox.",
     "Stuck, confused, or found a bug wearing a tiny hat? Write to us. We usually reply within two working days."),
]

# Each game: where it stands in the stores. Flip the *_live flags on launch day and rebuild.
GAMES = [
    {
        "slug": "inkbloom",
        "name": "Inkbloom",
        "full": "Inkbloom: Nonogram Puzzles",
        "genre": "Daily logic puzzles",
        "tagline": "A calm page of puzzles, every day.",
        "blurb": "Eight fresh puzzles every day, drawn from eleven logic games: nonogram, sudoku, word search and more. "
                 "No timers shouting at you, and no ads while you solve.",
        "goofy": "For people who solve to think. And to avoid the dishes.",
        "facts": [("11", "logic games"), ("8", "new puzzles a day"), ("2,365", "puzzles that play offline")],
        "status": "Coming soon",
        "status_note": "In final testing on Android and iPhone.",
        "play_id": "com.inkbloom.app", "play_live": False,
        "appstore_url": "", "appstore_live": False,
        "shots": [
            ("screen-1", "The Library: one card for each of the eleven games."),
            ("screen-3", "A nonogram part-way through: the numbers describe a hidden picture."),
            ("screen-4", "A solved nonogram. It's a bear!"),
            ("screen-6", "Today's page: eight puzzles, new every day."),
            ("screen-5", "Sudoku with the number lock on 5."),
            ("screen-7", "Word search: one theme, hidden eight ways."),
            ("screen-2", "A track page: carry on where you left off."),
            ("screen-8", "Killer sudoku in the Evening Ink theme."),
        ],
        "hero_shot": "screen-3",
        "framed": True,
        "features": [
            ("One page a day", "A fresh page arrives every day with eight puzzles on it: four easy, three medium and one hard. Solve all eight and the day is perfect."),
            ("Keep the streak", "Perfect days build a streak, the only number the app asks you to care about. Miss a day and it says so kindly, once."),
            ("Plays anywhere", "Every puzzle is on your phone before you open it. Plane, train or basement: no signal needed. Progress syncs when you're back online."),
            ("A Library that doesn't run out", "Over two thousand puzzles across eleven games and three difficulties. The first fifteen in every track are free."),
            ("Compete only if you want to", "Leaderboards are there if you go looking. You see a percentile, like \"top 20% today\", never a rank thrown at you."),
            ("Ads that know their place", "No ad ever interrupts a puzzle, and the daily page stays clear of them. Go ad-free any time."),
            ("Easy on the eyes", "Two themes, Morning Paper and Evening Ink, in warm paper tones rather than glare. Type sized for reading."),
        ],
        "how_intro": "Inkbloom has eleven games. Five are on every daily page and the other six take turns. Pick one for its rules, controls and tips.",
        "delete_label": "Delete your account",
        "legal_dates": {},   # the dates are inside the carried-over texts
    },
    {
        "slug": "lumiwire",
        "name": "Lumiwire",
        "full": "Lumiwire: Connect Wire Puzzle",
        "genre": "Wire puzzle",
        "tagline": "Join every pair. Cross nothing. Fill the board.",
        "blurb": "A calm circuit puzzle. Drag a wire from each socket to its twin, never cross another wire, and cover every cell. "
                 "Every board has exactly one answer, so careful thinking always gets you there.",
        "goofy": "Like untangling your earphones, except this time you win.",
        "facts": [("400", "levels in eight chapters"), ("1", "answer for every board"), ("60", "seconds in a Blitz round")],
        "status": "Coming soon",
        "status_note": "In closed testing on Android. iPhone to follow.",
        "play_id": "com.lumiwire.app", "play_live": False,
        "appstore_url": "", "appstore_live": False,
        "shots": [
            ("screen-1", "Join every pair. Cross nothing."),
            ("screen-3", "Every board has one answer."),
            ("screen-2", "Every pair has its own symbol, in light mode too."),
            ("screen-4", "400 levels in eight chapters."),
            ("screen-5", "A new circuit trick in each chapter."),
            ("screen-6", "A Daily puzzle, with no streak nags."),
            ("screen-7", "Blitz: sixty seconds of tiny boards."),
            ("screen-8", "Wire styles and board finishes in the Shop."),
        ],
        "hero_shot": "screen-1",
        "framed": False,   # these are store pictures: caption and phone are already in the image
        "features": [(h, t) if h != "Easy on the eyes" else
                     (h, "Soft greys and gold, in dark and in light. Every pair has a symbol as well as a colour, and the colours are tuned to stay distinct for colour-blind players.")
                     for h, t in lw.FEATURES],
        "rules": lw.RULES,
        "obstacles": [(o["name"], o["chapter"], o["level"], o["rule"]) for o in lw.OBSTACLES],
        "stars": lw.STARS,
        "modes": lw.MODES,
        "chapters": lw.CHAPTERS,
        "faq": lw.FAQ,
        "delete_label": "Delete your account",
        "legal_dates": {"privacy": lw.UPDATED, "terms": lw.UPDATED, "delete-account": lw.UPDATED},
        "shop_live": lw.SHOP_LIVE,
    },
    {
        "slug": "shapelings",
        "name": "Shapelings",
        "full": "Shapelings: Block Puzzle",
        "genre": "Block jigsaw",
        "tagline": "Every piece fits. You just have to find where.",
        "blurb": "A relaxing block jigsaw. Drag candy-coloured pieces into a shape until it is full. "
                 "Every puzzle has an answer, and you never have to rush.",
        "goofy": "Tetris's calmer cousin, who brought snacks.",
        "facts": [("300", "levels in ten worlds"), ("3", "grids: squares, triangles, hexagons"), ("1", "Daily puzzle, same for everyone")],
        "status": "Coming soon",
        "status_note": "In closed testing on Android. iPhone to follow.",
        "play_id": "com.shapelings.app", "play_live": False,
        "appstore_url": "", "appstore_live": False,
        "shots": [
            ("screen-1", "Drag the pieces in until the shape is full."),
            ("screen-5", "Level complete: the pieces join into one sweet."),
            ("screen-2", "Colour dots take only a piece of their own colour."),
            ("screen-3", "The Journey: ten worlds, 300 levels."),
            ("screen-6", "Block styles to unlock in the Shop."),
            ("screen-4", "A Hard level, waiting."),
        ],
        "hero_shot": "screen-1",
        "framed": True,
        "features": sh.FEATURES,
        "rules": sh.RULES,
        "faq": sh.FAQ,
        "delete_label": "Delete your data",
        "legal_dates": {"privacy": sh.UPDATED, "terms": sh.UPDATED, "delete-account": sh.UPDATED},
    },
    {
        "slug": "loopo",
        "name": "Loopo",
        "full": "Loopo",
        "genre": "Bubble arcade",
        "tagline": "Draw a loop. Pop the bubbles.",
        "blurb": "Bubbles drift across a sunny lagoon. Circle a group of one colour with your finger and they pop. "
                 "Loop bigger groups to earn bombs, darts and colour-clearing powers.",
        "goofy": "Lasso practice for people who don't own a horse.",
        "facts": [("1", "finger is all you need"), ("3", "powers: Bomb, Colour, Dart"), ("2", "ways to play: Journey and Survival")],
        "status": "In the workshop",
        "status_note": "In closed testing on Android, and still changing. Pictures and rules here describe the current test build.",
        "play_id": "com.loopo.app", "play_live": False,
        "appstore_url": "", "appstore_live": False,
        "shots": [
            ("screen-2", "Loop a group of one colour and it pops."),
            ("screen-1", "Home: one big Play button."),
            ("screen-4", "The Journey map."),
            ("screen-3", "A level in play, with its goal at the top."),
        ],
        "hero_shot": "screen-2",
        "framed": True,
        "features": [
            ("One finger, one rule", "Draw a loop around bubbles of one colour. That's the whole game, and it's surprisingly hard to stop."),
            ("Loops don't have to be neat", "End your line near where it started and the loop closes itself. Wobbly circles welcome."),
            ("Big loops earn powers", "Catch a big group and it leaves a Bomb, a Dart or a Colour bubble behind. Save them, or set them off at once."),
            ("A Journey to follow", "Levels on a map, each with one simple goal shown as a picture. Hearts refill while you're away."),
            ("Survival for one more go", "No timer and no levels. Just keep the lagoon from filling up, and chase this week's best score."),
            ("Ads when you choose", "Videos for a reward only play when you ask for one. A short ad may show between rounds, and one purchase removes those."),
        ],
        "rules": [
            "Bubbles drift across the lagoon. Draw a loop around bubbles of one colour and lift your finger: they pop.",
            "One colour per loop. If another colour is inside, nothing pops. There's no penalty, so just try again.",
            "A loop doesn't have to be neat. Finish close to where you started and it closes itself.",
            "Bigger loops score more, and a big one leaves a power behind.",
            "Never loop an urchin, the spiky one with the frown. It ends your run.",
        ],
        "powers": [
            ("power-bomb", "Bomb", "Pops everything around it. Loop it where it sits, or drop one from your pocket."),
            ("power-colour", "Colour", "Loop it together with one colour and every bubble of that colour pops, wherever it is."),
            ("power-dart", "Dart", "Flies off and bounces around for three seconds, popping every plain bubble it touches."),
        ],
        "extras": [
            ("urchin", "Urchin", "Draw around it, never over it. Looping one ends the run."),
            ("coin", "Gold", "A coin bubble. Catch it in any loop and it pays out."),
            ("key", "Key", "Carries on a Survival run that has just ended, with your score kept."),
            ("star", "Stars", "Every Journey level gives up to three, for the goal and for your score."),
        ],
        "modes": [
            ("Journey", "Levels on a map, grouped into ponds. Each level has one goal and a timer. A failed level costs a heart, a win costs nothing, and hearts come back with time."),
            ("Survival", "No timer. Bubbles keep coming and things speed up. If 30 bubbles crowd the lagoon for three seconds, the run is over. Your best score of the week goes on the Ranks board."),
        ],
        "pocket": "Powers you've saved live in your pocket. Double-tap the water, or press pause, to use one. You can use up to three in a run.",
        "faq": [
            ("I drew a loop and nothing popped. Why?",
             "A loop pops only when every bubble inside it is the same colour. If a bubble of another colour is inside, the loop flashes red and nothing pops. There's no penalty: draw again and leave the odd one out."),
            ("How do hearts work?",
             "You have five. A failed Journey level costs one, a win costs none, and one comes back every 30 minutes. Survival never uses hearts, so you can always play that while you wait."),
            ("What are the powers, and how do I get them?",
             "Bomb, Colour and Dart. They sometimes float in by themselves, and a big loop leaves one behind. Powers you've collected wait in your pocket: double-tap the water or press pause to use one."),
            ("Do I need an account?",
             "No. Loopo has no sign-up and no login. The game gives you an anonymous player ID so your progress can be backed up; the privacy policy has the details."),
            ("How do I delete my data?",
             "Loopo has no accounts, so deletion is done by email. The delete-your-data page explains what to send and what is removed."),
            ("Loopo looks different from the pictures here.",
             "Loopo is in closed testing and we're still changing it, sometimes a lot. This page describes the current test build and will be updated as the game settles."),
        ],
        "delete_label": "Delete your data",
        "legal_dates": {},
    },
]

BY_SLUG = {g["slug"]: g for g in GAMES}

LEGAL_TITLES = {
    "privacy": ("Privacy policy", "privacy policy"),
    "terms": ("Terms of use", "terms of use"),
    "delete-account": (None, None),   # uses the game's delete_label
}
