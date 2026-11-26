#!/usr/bin/env python3
"""Draws the files in static/ that are pictures: the favicon PNGs and the share cards (og/*.png).

Run it only when the mascot, a game's icon or a tagline changes:
    pip install playwright pillow && playwright install chromium
    python tools/make_brand.py
The results are committed, so build.py itself needs no browser.
"""
import os, sys
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import content as C

STATIC = ROOT / "static"
FONTS = (ROOT / "fonts").as_uri()
IMAGES = (ROOT / "images").as_uri()
RADDY = (STATIC / "favicon.svg").read_text(encoding="utf-8")

FACES = f"""
@font-face {{ font-family: "Bagel Fat One"; src: url("{FONTS}/bagel-fat-one-latin-400-normal.woff2"); }}
@font-face {{ font-family: "Figtree"; src: url("{FONTS}/figtree-latin-wght-normal.woff2"); font-weight: 300 900; }}
@font-face {{ font-family: "Fredoka"; src: url("{FONTS}/fredoka-latin-wght-normal.woff2"); font-weight: 300 700; }}
@font-face {{ font-family: "Lilita One"; src: url("{FONTS}/lilita-one-latin-400-normal.woff2"); }}
@font-face {{ font-family: "Nunito"; src: url("{FONTS}/nunito-latin-wght-normal.woff2"); font-weight: 200 1000; }}
@font-face {{ font-family: "Fraunces"; src: url("{FONTS}/fraunces-latin-wght-italic.woff2"); font-style: italic; font-weight: 100 900; }}
* {{ box-sizing: border-box; margin: 0; }}
body {{ width: 1200px; height: 630px; overflow: hidden; font-family: "Figtree", sans-serif; }}
.badge {{ position: absolute; left: 64px; bottom: 52px; display: flex; align-items: center; gap: 14px; font: 400 34px/1 "Bagel Fat One"; }}
.badge svg {{ width: 58px; height: 58px; }}
"""

WORLDS = {
    "inkbloom": dict(bg="#F6F3EC", fg="#26241F", sub="#6E6A60", title='500 italic 112px/1 "Fraunces"', badge="#26241F"),
    "lumiwire": dict(bg="#1C1F26", fg="#F6F7F9", sub="#BFC5D1", title='600 112px/1 "Fredoka"', badge="#FFD45E"),
    "shapelings": dict(bg="radial-gradient(700px 520px at 100% 0%, #FFE3EB 0 60%, transparent 61%), #FFF3F6", fg="#2A1B4A", sub="#6A5B86", title='900 108px/1 "Nunito"', badge="#2A1B4A"),
    "loopo": dict(bg="linear-gradient(180deg, #3FC0F8 0%, #2C8EEC 34%, #2458CC 72%, #213A98 100%)", fg="#FFFFFF", sub="#E3F1FF", title='400 124px/1 "Lilita One"', badge="#FFFFFF"),
}


def studio_card():
    icons = "".join(
        f'<img src="{IMAGES}/{g["slug"]}/icon.png" style="width:150px;height:150px;border-radius:24%;border:6px solid #fff;outline:4px solid #1C1A33;box-shadow:0 10px 0 #1C1A33;rotate:{r}deg">'
        for g, r in zip(C.GAMES, (-7, 5, -4, 8)))
    return f"""<!doctype html><meta charset="utf-8"><style>{FACES}
body {{ background: #FFF6E3; color: #1C1A33; background-image: radial-gradient(rgba(28,26,51,.13) 2px, transparent 2.3px); background-size: 28px 28px; }}
.sun {{ position: absolute; right: -180px; top: -260px; width: 700px; height: 700px; border-radius: 50%; background: #FFC93C; }}
h1 {{ position: absolute; left: 64px; top: 70px; font: 400 104px/.98 "Bagel Fat One"; width: 760px; }}
h1 span {{ display: inline-block; background: #1C1A33; color: #FFF6E3; padding: 0 .16em .04em; border-radius: .18em; rotate: -2deg; }}
.icons {{ position: absolute; left: 64px; bottom: 150px; display: flex; gap: 30px; }}
.mascot {{ position: absolute; right: 90px; top: 70px; width: 250px; filter: drop-shadow(0 12px 0 #1C1A33); rotate: 6deg; }}
</style><div class="sun"></div><div class="mascot">{RADDY}</div>
<h1>Small games. <span>Big</span> “one more go” energy.</h1><div class="icons">{icons}</div>
<div class="badge">{RADDY}<span>raddgames.com</span></div>"""


def game_card(g):
    w = WORLDS[g["slug"]]
    return f"""<!doctype html><meta charset="utf-8"><style>{FACES}
body {{ background: {w["bg"]}; color: {w["fg"]}; }}
.icon {{ position: absolute; left: 64px; top: 64px; width: 210px; height: 210px; border-radius: 23%; box-shadow: 0 12px 0 rgba(0,0,0,.25); }}
h1 {{ position: absolute; left: 64px; top: 312px; font: {w["title"]}; }}
p {{ position: absolute; left: 68px; top: 446px; font: 600 40px/1.2 "Figtree"; color: {w["sub"]}; width: 800px; }}
.shot {{ position: absolute; right: 70px; top: 54px; width: 300px; border-radius: 34px; border: 10px solid #15141F; box-shadow: 0 14px 0 rgba(0,0,0,.28); rotate: 5deg; }}
.badge {{ color: {w["badge"]}; font-size: 28px; }} .badge svg {{ width: 46px; height: 46px; }}
</style><img class="icon" src="{IMAGES}/{g["slug"]}/icon.png"><img class="shot" src="{IMAGES}/{g["slug"]}/{g["hero_shot"]}.png">
<h1>{g["name"]}</h1><p>{g["tagline"]}</p><div class="badge">{RADDY}<span>Radd Games</span></div>"""


def main():
    (STATIC / "og").mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1200, "height": 630})
        jobs = [("og/radd-games.png", studio_card())] + [(f'og/{g["slug"]}.png', game_card(g)) for g in C.GAMES]
        tmp = ROOT / "tools" / "_card.html"
        for name, markup in jobs:
            tmp.write_text(markup, encoding="utf-8")
            page.goto(tmp.as_uri())
            page.evaluate("document.fonts.ready")
            page.wait_for_timeout(250)
            page.screenshot(path=str(STATIC / name))
            print("drew", name)
        tmp.unlink()
        # the mascot as PNGs, on a transparent ground
        icon = browser.new_page(viewport={"width": 512, "height": 512})
        icon.set_content(f'<style>html,body{{margin:0;background:transparent}}svg{{width:512px;height:512px;display:block}}</style>{RADDY}')
        icon.screenshot(path=str(STATIC / "icon-512.png"), omit_background=True)
        browser.close()
    big = Image.open(STATIC / "icon-512.png")
    touch = Image.new("RGB", (180, 180), "#FFF6E3")
    small = big.resize((150, 150), Image.LANCZOS)
    touch.paste(small, (15, 15), small)
    touch.save(STATIC / "apple-touch-icon.png")
    big.resize((192, 192), Image.LANCZOS).save(STATIC / "icon-192.png")
    big.save(STATIC / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print("drew the favicons")


main()
