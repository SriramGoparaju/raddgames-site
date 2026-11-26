#!/usr/bin/env python3
"""Draws the files in static/ that are pictures: the favicon PNGs and the share cards (og/*.png).

Run it only when the mascot, a game's icon or a tagline changes:
    pip install playwright pillow && playwright install chromium
    python tools/make_brand.py
The results are committed, so build.py itself needs no browser.
"""
import os, sys
from html import escape as e
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
@font-face {{ font-family: "Bricolage Grotesque"; src: url("{FONTS}/bricolage-grotesque-latin-wght-normal.woff2"); font-weight: 200 800; }}
@font-face {{ font-family: "Figtree"; src: url("{FONTS}/figtree-latin-wght-normal.woff2"); font-weight: 300 900; }}
* {{ box-sizing: border-box; margin: 0; }}
body {{ width: 1200px; height: 630px; overflow: hidden; font-family: "Figtree", sans-serif; background: #FFFFFF; color: #15141B; }}
.badge {{ position: absolute; left: 64px; bottom: 50px; display: flex; align-items: center; gap: 12px; font: 800 30px/1 "Bricolage Grotesque"; letter-spacing: -.02em; }}
.badge svg {{ width: 50px; height: 50px; }}
.phone {{ position: absolute; padding: 7px; border-radius: 34px; background: #17161D; box-shadow: 0 30px 60px -30px rgba(21, 20, 27, .6); }}
.phone img {{ display: block; width: 100%; border-radius: 28px; }}
.panel {{ position: absolute; right: 40px; top: 40px; bottom: 40px; width: 500px; border-radius: 40px; background: #F4F3EE; overflow: hidden; }}
"""

ACCENT = {"inkbloom": "#5E7A56", "lumiwire": "#F2B705", "shapelings": "#D81B60", "loopo": "#2A62D6"}


def studio_card():
    phones = "".join(
        f'<div class="phone" style="left:{28 + i * 116}px; top:{110 + (34 if i % 2 else -6)}px; width:106px; padding:4px; border-radius:18px"><img style="border-radius:14px" src="{IMAGES}/{g["slug"]}/{g["hero_shot"]}.png"></div>'
        for i, g in enumerate(C.GAMES))
    return f"""<!doctype html><meta charset="utf-8"><style>{FACES}
h1 {{ position: absolute; left: 64px; top: 86px; width: 600px; font: 800 82px/.97 "Bricolage Grotesque"; letter-spacing: -.045em; }}
h1 em {{ font-style: normal; background: linear-gradient(transparent 58%, #FFC93C 58% 92%, transparent 92%); }}
p {{ position: absolute; left: 66px; top: 380px; width: 540px; font: 500 26px/1.4 "Figtree"; color: #3F3D49; }}
</style><div class="panel">{phones}</div>
<h1>Small games. Big <em>“one more go”</em> energy.</h1>
<p>Inkbloom, Lumiwire, Shapelings and Loopo.</p>
<div class="badge">{RADDY}<span>raddgames.com</span></div>"""


def game_card(g):
    a, b = g["hero_shots"]
    return f"""<!doctype html><meta charset="utf-8"><style>{FACES}
.icon {{ position: absolute; left: 64px; top: 64px; width: 132px; height: 132px; border-radius: 23%; box-shadow: 0 0 0 1px rgba(21, 20, 27, .08); }}
.kind {{ position: absolute; left: 66px; top: 232px; font: 700 20px/1 "Figtree"; letter-spacing: .1em; text-transform: uppercase; color: #6A6874; }}
.kind::before {{ content: ""; display: inline-block; width: 14px; height: 14px; border-radius: 50%; background: {ACCENT[g["slug"]]}; margin-right: 12px; }}
h1 {{ position: absolute; left: 62px; top: 266px; font: 800 104px/1 "Bricolage Grotesque"; letter-spacing: -.045em; }}
p {{ position: absolute; left: 66px; top: 392px; width: 560px; font: 600 30px/1.3 "Figtree"; color: #3F3D49; }}
</style><img class="icon" src="{IMAGES}/{g["slug"]}/icon.png">
<div class="panel"><div class="phone" style="left:44px; top:70px; width:212px"><img src="{IMAGES}/{g["slug"]}/{a}.png"></div>
<div class="phone" style="left:262px; top:130px; width:212px"><img src="{IMAGES}/{g["slug"]}/{b}.png"></div></div>
<div class="kind">{e(g["genre"])}</div><h1>{e(g["name"])}</h1><p>{e(g["tagline"])}</p><div class="badge">{RADDY}<span>Radd Games</span></div>"""


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
    touch = Image.new("RGB", (180, 180), "#FFFFFF")
    small = big.resize((150, 150), Image.LANCZOS)
    touch.paste(small, (15, 15), small)
    touch.save(STATIC / "apple-touch-icon.png")
    big.resize((192, 192), Image.LANCZOS).save(STATIC / "icon-192.png")
    big.save(STATIC / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print("drew the favicons")


main()
