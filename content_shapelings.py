"""The words on the Shapelings website (build.py lays them out)."""

UPDATED = "14 November 2026"
SUPPORT_EMAIL = "sriramgoparaju99@gmail.com"   # support@<domain> once the site has its own domain
PLAY_URL = "https://play.google.com/store/apps/details?id=com.shapelings.app"
APP_STORE_URL = ""                             # set on launch day (App Store Connect app id)

FEATURES = [
    ("One answer, always reachable",
     "Every board was solved by a computer before it shipped, so there is always a way to fill it. No luck, no timer, no lives."),
    ("Ten worlds, three grids",
     "Squares, then triangles and hexagons. Colour dots that only take their own colour, and pieces that turn. 300 levels, getting gently harder."),
    ("A new puzzle every day",
     "One Daily puzzle, the same for everyone. Missed a day? Play it later; nothing is lost."),
    ("Hints that show, not tell",
     "A hint lights up where one piece goes, or which piece is in the way. You start with a few and earn more as you play."),
    ("Calm and fair",
     "Ads only between levels, never in the middle of a puzzle, and a video only when you choose one. Remove ads once and they stay gone."),
    ("Easy to read",
     "Every colour dot carries a symbol too, so colour is never the only clue. Big text, sound and haptics are your choice."),
]

RULES = [
    "Drag a piece from the tray onto the board. It snaps into place when it fits.",
    "Fill every empty cell of the shape. Pieces may not overlap or hang over the edge.",
    "Change your mind: drag a placed piece back to the tray, or tap Undo.",
    "Colour dots (from World 2) take only a piece of their own colour.",
    "Pieces with the turn badge (from World 3) turn when you tap them.",
]

FAQ = [
    ("I'm stuck on a level. What can I do?",
     "Tap Hint: it lights up where one piece goes, or the piece that is in the way. Out of hints? Watch a short video for one, use gems, or skip the level with gems and come back later."),
    ("Is every puzzle really solvable?",
     "Yes. Every level and every Daily puzzle was solved by a computer before the app shipped, and the Hard levels were checked to have only a few solutions."),
    ("Where is my progress saved?",
     "On your phone. There is no account and no cloud save, so progress does not move to a new phone, and it is lost if you uninstall the app or clear its data."),
    ("I bought Remove ads. How do I get it back on a new phone?",
     "Open the Shop and tap Restore purchases, signed in to the same Google Play or App Store account. Hint and gem packs are used up when you buy them and are not restored."),
    ("A purchase didn't arrive.",
     "Some payments take a while to clear; the app adds the item as soon as the store confirms it, also after a restart. If it still hasn't arrived, write to us with the date and the item."),
    ("How do I change what the ads may use?",
     "Where the law gives you a choice, Settings shows Privacy options, which opens Google's consent form again. See the privacy policy for the details."),
    ("Does it work offline?",
     "Yes. Everything plays without a connection. Videos for hints and purchases need the internet."),
]
