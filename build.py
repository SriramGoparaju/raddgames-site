#!/usr/bin/env python3
"""Builds raddgames.com as plain static files.

usage: python build.py [out_dir] [--preview]
  out_dir    default: docs (GitHub Pages serves main /docs, with docs/CNAME = raddgames.com)
  --preview  writes explicit index.html links so the site can be browsed from disk.

Where things live:
  content.py            the words and facts (one block per game), store links, the support email
  content_lumiwire.py   Lumiwire's facts, copied from lumiwire-site/content.py
  content_shapelings.py Shapelings' facts, copied from shapelings-site/content.py
  legal/<game>/*.html   each game's privacy policy, terms and delete page (body only; placeholders
                        {{EMAIL}} {{UPDATED}} {{PRIVACY}} {{TERMS}} {{DELETE}} {{SUPPORT}} {{HOME}})
  pages/inkbloom/       Inkbloom's eleven how-to pages and its FAQ, carried over from inkbloompuzzles.com
  images/<game>/        source pictures (PNG); the build makes the WebP files
  src/site.css, site.js the look ("Gallery": one white site; a game brings only its screenshots and one
                        accent colour) and the small scripts (menu, screenshot arrows, Raddy's eyes, reveals)
  static/               files copied as they are (favicon, share pictures, CNAME, .nojekyll)

Launch day for a game: set play_live / appstore_live (and appstore_url) in content.py, rebuild, push.
Needs Python 3.9+ and Pillow.
"""
import html, json, os, re, shutil, sys
from urllib.parse import quote
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import content as C

args = [a for a in sys.argv[1:] if not a.startswith("--")]
OUT = os.path.abspath(args[0]) if args else os.path.join(ROOT, "docs")
PREVIEW = "--preview" in sys.argv
e = html.escape
CURRENT = ' aria-current="page"'
CUR = {"depth": 0, "abs": False}
PAGES = []          # (path, title) of every page written, for the sitemap


# ---------------------------------------------------------------- helpers
def u(target=""):
    """A link from the page being built to a site path: '' (home), 'loopo/', 'assets/site.css'."""
    if CUR["abs"]:
        return "/" + target
    up = "../" * CUR["depth"]
    if target == "" or target.endswith("/"):
        if PREVIEW:
            return up + target + "index.html"
        return (up + target) or "./"
    return up + target


def mailto(subject=None, body=None):
    """A mailto link. On computers site.js turns every mailto link into a small chooser
    (Gmail in the browser, the computer's mail app, or copy the address), because a bare
    mailto does nothing on a computer with no mail app set up. Phones open their mail app."""
    q = []
    if subject:
        q.append("subject=" + quote(subject, safe=""))
    if body:
        q.append("body=" + quote(body, safe=""))
    return f"mailto:{C.SUPPORT_EMAIL}" + ("?" + "&".join(q) if q else "")


def tester_mail(game=None):
    what = game or "your games"
    body = (f"Hi Radd,\n\nI'd like to test {what} on Android.\n\n"
            "The Gmail address I use on Google Play: \nMy phone model: \n\nThanks!")
    return mailto(f"I would like to test {what}", body)


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


def write(rel, text):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


IMG = {}            # "loopo/screen-1" -> (webp path, width, height)


def build_images():
    """PNG sources -> WebP. Screens at 640 wide, icons at 256, Loopo's bubble art at 160."""
    src_root = os.path.join(ROOT, "images")
    for game in sorted(os.listdir(src_root)):
        gdir = os.path.join(src_root, game)
        if not os.path.isdir(gdir):
            continue
        for name in sorted(os.listdir(gdir)):
            stem, ext = os.path.splitext(name)
            if ext.lower() != ".png":
                continue
            im = Image.open(os.path.join(gdir, name))
            target = 256 if stem == "icon" else 640 if stem.startswith("screen-") else 160
            if im.width > target:
                im = im.resize((target, round(im.height * target / im.width)), Image.LANCZOS)
            im = im.convert("RGBA") if im.mode in ("RGBA", "LA", "P") else im.convert("RGB")
            rel = f"assets/img/{game}/{stem}.webp"
            dst = os.path.join(OUT, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            im.save(dst, "WEBP", quality=84, method=6)
            IMG[f"{game}/{stem}"] = (rel, im.width, im.height)
            if stem == "icon":       # a PNG too, for share cards and search results
                big = Image.open(os.path.join(gdir, name)).convert("RGB")
                if big.width > 512:
                    big = big.resize((512, 512), Image.LANCZOS)
                big.save(os.path.join(OUT, f"assets/img/{game}/icon-512.png"), optimize=True)


def img(key, alt, cls="", lazy=True):
    rel, w, h = IMG[key]
    c = f' class="{cls}"' if cls else ""
    l = ' loading="lazy" decoding="async"' if lazy else ' decoding="async"'
    return f'<img src="{u(rel)}" alt="{e(alt)}" width="{w}" height="{h}"{c}{l}>'


def raddy(label="Raddy, the Radd Games mascot", decorative=False):
    aria = 'aria-hidden="true"' if decorative else f'role="img" aria-label="{e(label)}"'
    return f'''<svg class="raddy" viewBox="0 0 64 64" {aria}>
<rect x="4" y="6" width="56" height="54" rx="18" fill="#FFC93C" stroke="#1C1A33" stroke-width="4"/>
<g class="eye"><circle cx="22" cy="28" r="9.5" fill="#fff" stroke="#1C1A33" stroke-width="3"/><circle class="pupil" cx="22" cy="28" r="4.2" fill="#1C1A33"/><circle class="lid" cx="22" cy="28" r="9.5" fill="#FFC93C" stroke="#1C1A33" stroke-width="3"/></g>
<g class="eye"><circle cx="42" cy="28" r="9.5" fill="#fff" stroke="#1C1A33" stroke-width="3"/><circle class="pupil" cx="42" cy="28" r="4.2" fill="#1C1A33"/><circle class="lid" cx="42" cy="28" r="9.5" fill="#FFC93C" stroke="#1C1A33" stroke-width="3"/></g>
<path d="M20 43 Q32 57 44 43 Z" fill="#1C1A33" stroke="#1C1A33" stroke-width="3" stroke-linejoin="round"/>
<path d="M26.5 49.5 Q32 46 37.5 49.5 Q32 54 26.5 49.5 Z" fill="#FF6FA8"/>
<rect x="29.3" y="43" width="5.4" height="4.6" rx="1.2" fill="#fff"/>
</svg>'''


PLAY_GLYPH = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 3.5v17a1 1 0 0 0 1.5.87l14.2-8.5a1 1 0 0 0 0-1.74L6.5 2.63A1 1 0 0 0 5 3.5z" fill="currentColor"/></svg>'
PHONE_GLYPH = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="6" y="2" width="12" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="18" r="1.3" fill="currentColor"/></svg>'


def store_buttons(g):
    out = []
    if g["play_live"]:
        out.append(f'<a class="store" href="https://play.google.com/store/apps/details?id={g["play_id"]}" rel="noopener">{PLAY_GLYPH}<small>Get it on</small><b>Google Play</b></a>')
    else:
        out.append(f'<span class="store soon">{PLAY_GLYPH}<small>Coming soon to</small><b>Google Play</b></span>')
    if g["appstore_live"] and g["appstore_url"]:
        out.append(f'<a class="store" href="{e(g["appstore_url"])}" rel="noopener">{PHONE_GLYPH}<small>Download on the</small><b>App Store</b></a>')
    else:
        out.append(f'<span class="store soon">{PHONE_GLYPH}<small>Coming soon to the</small><b>App Store</b></span>')
    return '<div class="stores">' + "".join(out) + "</div>"


def delete_label(g):
    return g["delete_label"]


# ---------------------------------------------------------------- layout
LEFT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>'
RIGHT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>'


def layout(path, title, desc, body, game=None, nav=None, og="og/radd-games.png", ld=None, index=True):
    canonical = f"{C.SITE_ORIGIN}/{path}"
    nav_items = [("", "Games", "games"), ("support/", "Support", "support"), ("about/", "About", "about")]
    links = "".join(
        f'<a href="{u(t) + ("#games" if key == "games" else "")}"{CURRENT if nav == key else ""}>{label}</a>'
        for t, label, key in nav_items)
    foot_games = "".join(f'<li><a href="{u(g["slug"] + "/")}">{e(g["name"])}</a></li>' for g in C.GAMES)
    foot_legal = "".join(
        f'<li>{e(g["name"])}: <a href="{u(g["slug"] + "/privacy/")}">Privacy</a> · <a href="{u(g["slug"] + "/terms/")}">Terms</a> · '
        f'<a href="{u(g["slug"] + "/delete-account/")}">Delete data</a></li>' for g in C.GAMES)
    robots = "" if index else '<meta name="robots" content="noindex">\n'
    ld_html = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n' if ld else ""
    main_attr = f' data-game="{game}"' if game else ""
    return f'''<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{robots}<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#FFFFFF">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{C.SITE_NAME}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{C.SITE_ORIGIN}/{og}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{u("favicon.svg")}" type="image/svg+xml">
<link rel="icon" href="{u("favicon.ico")}" sizes="32x32">
<link rel="apple-touch-icon" href="{u("apple-touch-icon.png")}">
<link rel="preload" href="{u("assets/fonts/bricolage-grotesque-latin-wght-normal.woff2")}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{u("assets/fonts/figtree-latin-wght-normal.woff2")}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{u("assets/site.css")}">
{ld_html}</head>
<body>
<a class="skip" href="#main">Skip to the page</a>
<header class="site-head"><div class="wrap bar">
  <a class="brand" href="{u("")}" aria-label="Radd Games, home">{raddy(decorative=True)}<span>Radd Games</span></a>
  <button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-nav"><i></i>Menu</button>
  <nav class="site-nav" id="site-nav" aria-label="Site">{links}<a class="hello" href="{mailto("Hello Radd Games")}">Say hello</a></nav>
</div></header>
<main id="main"{main_attr}>
{body}
</main>
<footer class="site-foot"><div class="wrap">
  <div class="foot-grid">
    <div class="foot-brand">
      <a class="brand" href="{u("")}">{raddy(decorative=True)}<span>Radd Games</span></a>
      <p>Puzzle games for the five minutes you definitely have.</p>
    </div>
    <div><h2>Games</h2><ul>{foot_games}</ul></div>
    <div><h2>Help</h2><ul>
      <li><a href="{u("support/")}">Support</a></li>
      <li><a href="{tester_mail()}">Become a tester</a></li>
      <li><a href="{u("about/")}">About</a></li>
      <li><a href="{mailto()}">{C.SUPPORT_EMAIL}</a></li></ul></div>
    <div class="foot-legal"><h2>Privacy, terms and your data</h2><ul>{foot_legal}
      <li><a href="{u("privacy/")}">Privacy on this website</a></li></ul></div>
  </div>
  <div class="foot-base"><span>© {C.YEAR} {C.SITE_NAME}. Games by {C.ALIAS} ({C.PUBLISHER}), {C.COUNTRY}.</span><span>This site uses no cookies and no trackers.</span></div>
</div></footer>
<script src="{u("assets/site.js")}" defer></script>
</body>
</html>
'''


def emit(path, builder, absolute=False):
    """path: '' for home, 'loopo/privacy/' for a folder page, '404.html' for a file."""
    CUR["abs"] = absolute
    CUR["depth"] = 0 if path.endswith(".html") else len([p for p in path.split("/") if p])
    page = builder()
    rel = path if path.endswith(".html") else path + "index.html"
    write(rel, layout(path, **page))
    if page.get("index", True) and not path.endswith(".html"):
        PAGES.append(path)


def phone(g, key, alt, cls="", lazy=True):
    c = f" {cls}" if cls else ""
    return f'<div class="phone{c}">{img(g["slug"] + "/" + key, alt, lazy=lazy)}</div>'


def subnav(g, current):
    """The game's own row of pages, under the studio header. The same on every page of every game."""
    s = g["slug"]
    items = [("", "Overview"), ("how-to-play/", "How to play"), ("support/", "Support"), ("privacy/", "Privacy"),
             ("terms/", "Terms"), ("delete-account/", delete_label(g))]
    lis = "".join(f'<li><a href="{u(s + "/" + t)}"{CURRENT if t == current else ""}>{e(label)}</a></li>' for t, label in items)
    return f'''<div class="subnav"><div class="wrap">
  <a class="gname" href="{u(s + "/")}">{img(s + "/icon", "", lazy=False)}{e(g["name"])}</a>
  <nav class="tabs" aria-label="{e(g["name"])} pages"><ul>{lis}</ul></nav>
  <a class="back" href="{u("")}#games">← All games</a>
</div></div>'''


def carousel(g):
    figs = "".join(f"<figure>{phone(g, key, cap, lazy=i > 3)}<figcaption>{e(cap)}</figcaption></figure>"
                   for i, (key, cap) in enumerate(g["shots"]))
    n = len(g["shots"])
    return f'''<section class="section shots" aria-labelledby="shots-h"><div class="wrap">
  <div class="shots-head"><h2 class="h2" id="shots-h">Screenshots</h2><span class="count" aria-live="polite">{n} pictures</span></div>
  <div class="carousel" data-carousel>
    <button class="arrow prev" type="button" aria-label="Previous pictures" disabled>{LEFT}</button>
    <div class="track" tabindex="0" role="group" aria-label="Pictures of {e(g["name"])}">{figs}</div>
    <button class="arrow next" type="button" aria-label="Next pictures">{RIGHT}</button>
  </div>
  <div class="dots"></div>
</div></section>'''


# ---------------------------------------------------------------- studio pages
def home():
    slots = "".join(
        f'<a class="slot" href="{u(g["slug"] + "/")}" aria-label="{e(g["name"])}"><span class="float f{i}">{phone(g, g["hero_shot"], "", lazy=False)}</span></a>'
        for i, g in enumerate(C.GAMES, 1))
    cards = []
    for g in C.GAMES:
        s = g["slug"]
        a, b = g["card_shots"]
        cards.append(f'''<a class="gcard" href="{u(s + "/")}" data-game="{s}" data-reveal>
  <span class="gcard-body">
    {img(s + "/icon", "", "icon")}
    <span class="kind">{e(g["genre"])}</span>
    <h3 class="h3">{e(g["name"])}</h3>
    <span class="gtag">{e(g["tagline"])}</span>
    <span class="chip">{e(g["status"])}</span>
    <span class="more">See {e(g["name"])} <span class="arr">→</span></span>
  </span>
  <span class="gcard-art" aria-hidden="true">{phone(g, a, "", "a")}{phone(g, b, "", "b")}</span>
</a>''')
    promises = "".join(f'<div class="promise" data-reveal><h3>{e(h)}</h3><p>{e(t)}</p></div>' for h, t in C.HOUSE_RULES)
    body = f'''<section class="hero"><div class="wrap">
  <div class="hero-copy">
    <p class="eyebrow rise">Four small games · one tiny studio</p>
    <h1 class="display rise r2">Small games. Big <em>“one more go”</em> energy.</h1>
    <p class="lede rise r3">Radd Games is a tiny studio making puzzle games for phones. No sign-ups, no ads in the middle of a puzzle, and nothing that needs a manual.</p>
    <div class="actions rise r4"><a class="btn" href="#games">Meet the games</a><a class="btn ghost" href="{tester_mail()}">Become a tester</a></div>
  </div>
  <div class="showcase rise r3">
    <div class="peek">{raddy()}<span class="say">Psst. Pick one.</span></div>
    <div class="phones">{slots}</div>
  </div>
</div></section>
<section class="section" id="games"><div class="wrap">
  <div class="sec-head"><h2 class="h2">The games</h2><p>Free to play · all four in testing now</p></div>
  <div class="gcards">{"".join(cards)}</div>
</div></section>
<section class="section"><div class="wrap">
  <div class="sec-head"><h2 class="h2">Things we promise</h2><p>Even for games that don't exist yet.</p></div>
  <div class="promises">{promises}</div>
</div></section>
<section class="section"><div class="wrap duo">
  <div class="panel" data-reveal><h2 class="h3">Play before everyone else.</h2>
    <p>All four games are in closed testing on Android. Send us the Gmail address you use on Google Play and we'll add you to the list. We use it for that and nothing else.</p>
    <a class="btn" href="{tester_mail()}">Become a tester <span class="arr">→</span></a></div>
  <div class="panel" data-reveal><h2 class="h3">Say hello.</h2>
    <p>Questions, bugs, ideas, or a high score that needs a witness. One real person reads everything sent to {C.SUPPORT_EMAIL}.</p>
    <a class="btn ghost" href="{mailto("Hello Radd Games")}">Email us</a></div>
</div></section>'''
    ld = {"@context": "https://schema.org", "@type": "Organization", "name": C.SITE_NAME, "url": C.SITE_ORIGIN + "/",
          "logo": C.SITE_ORIGIN + "/icon-512.png", "email": C.SUPPORT_EMAIL,
          "founder": {"@type": "Person", "name": C.ALIAS}}
    return dict(title="Radd Games: small puzzle games with big “one more go” energy",
                desc="Radd Games makes calm, clever puzzle games for phones: Inkbloom, Lumiwire, Shapelings and Loopo. No sign-ups and no ads in the middle of a puzzle.",
                body=body, nav="games", ld=ld)


def page_head(eyebrow, h1, lede, narrow=False):
    box = "narrow" if narrow else "wrap"
    return f'''<section class="page-head"><div class="{box}"><p class="eyebrow">{eyebrow}</p>
  <h1>{h1}</h1><p class="lede">{lede}</p></div></section>'''


def pick_cards(sub, path=""):
    return '<div class="pick">' + "".join(
        f'<a href="{u(g["slug"] + "/" + path)}">{img(g["slug"] + "/icon", "")}<span><b>{e(g["name"])}</b><span>{e(sub(g))}</span></span></a>'
        for g in C.GAMES) + "</div>"


def support_hub():
    datas = "".join(
        f'<div class="panel"><h3>{e(g["name"])}</h3><p><a href="{u(g["slug"] + "/privacy/")}">Privacy policy</a><br><a href="{u(g["slug"] + "/terms/")}">Terms of use</a><br>'
        f'<a href="{u(g["slug"] + "/delete-account/")}">{e(delete_label(g))}</a></p></div>' for g in C.GAMES)
    body = f'''{page_head("Support", "Stuck? Confused? Found a bug wearing a tiny hat?", "Pick your game for its common questions, or write to us directly. One real person reads every message, and we usually reply within two working days.")}
<section class="section"><div class="wrap"><div class="sec-head"><h2 class="h2">Which game?</h2></div>{pick_cards(lambda g: "Answers and contact for " + g["name"], "support/")}</div></section>
<section class="section"><div class="wrap"><div class="band"><div><h2 class="h3">Or just email us.</h2>
  <p>It helps to say which game, your phone model, its Android or iOS version, and to attach a screenshot if something looks wrong.</p></div>
  <a class="btn" href="{mailto("Support")}">{C.SUPPORT_EMAIL}</a></div></div></section>
<section class="section"><div class="wrap"><div class="sec-head"><h2 class="h2">Your data</h2><p>Every game has its own privacy policy and its own way to delete what it stores.</p></div>
  <div class="datas">{datas}</div></div></section>'''
    return dict(title="Support: Radd Games", desc=f"Help with Inkbloom, Lumiwire, Shapelings and Loopo. Common questions for each game, and how to reach us: {C.SUPPORT_EMAIL}.",
                body=body, nav="support")


def about():
    promises = "".join(f'<div class="promise"><h3>{e(h)}</h3><p>{e(t)}</p></div>' for h, t in C.HOUSE_RULES)
    body = f'''{page_head("About", "A very small studio with a very long to-do list.", "Radd Games makes puzzle games for phones: the kind you open for five minutes and close forty minutes later, slightly proud of yourself.")}
<section class="doc"><div class="narrow prose">
  <h2 style="margin-top:0">Who we are</h2>
  <p>Radd Games is an independent studio from {C.COUNTRY}. The games are designed, built and published by {C.ALIAS}, with a great deal of help from a small circle of patient friends who test everything first.</p>
  <h2>What we make</h2>
  <p>Calm, fair puzzle games. Easy to start, hard to put down, and never rude about it: no ads in the middle of a puzzle, no sign-up wall, and no dark tricks to keep you tapping.</p>
  <h2>How to reach us</h2>
  <p>Write to <a href="{mailto("Hello Radd Games")}">{C.SUPPORT_EMAIL}</a>. For help with a particular game, its <a href="{u("support/")}">support page</a> is the quickest route.</p>
</div></section>
<section class="section"><div class="wrap"><div class="sec-head"><h2 class="h2">The games</h2></div>{pick_cards(lambda g: g["genre"])}</div></section>
<section class="section"><div class="wrap"><div class="sec-head"><h2 class="h2">Things we promise</h2></div><div class="promises">{promises}</div></div></section>'''
    return dict(title="About Radd Games", desc="Radd Games is a small independent studio from India making calm, fair puzzle games for phones.", body=body, nav="about")


def privacy_hub():
    items = "".join(f'<li><a href="{u(g["slug"] + "/privacy/")}">{e(g["name"])} privacy policy</a> · <a href="{u(g["slug"] + "/delete-account/")}">{e(delete_label(g).lower())}</a></li>' for g in C.GAMES)
    body = f'''{page_head("Privacy", "Privacy at Radd Games", "The short version: this website collects nothing about you, and each game explains exactly what it collects on its own page.", narrow=True)}
<section class="doc" style="padding-top:8px"><div class="narrow prose">
  <h2 style="margin-top:0">The games</h2>
  <p>Each game has its own privacy policy, because each game stores different things:</p>
  <ul>{items}</ul>
  <h2>This website</h2>
  <ul>
    <li><strong>No cookies, no analytics, no ads.</strong> Nothing here tracks you or builds a profile.</li>
    <li><strong>Nothing loaded from other companies.</strong> The fonts, pictures and scripts are served from this site itself.</li>
    <li><strong>Hosting.</strong> The site is hosted on GitHub Pages and its domain is served by Cloudflare. Like any web host, these services process technical details such as your IP address to deliver the pages and keep them secure.</li>
    <li><strong>Email.</strong> If you write to us, we use your address and your message only to answer you. Ask us to delete the conversation and we will.</li>
    <li><strong>Testers.</strong> If you ask to test a game, we add the Google account address you send us to that game's tester list on Google Play, and use it for nothing else. Ask to be removed at any time.</li>
  </ul>
  <h2>Who is responsible</h2>
  <p>Radd Games is run by {C.ALIAS} ({C.PUBLISHER}), in {C.COUNTRY}. Questions about privacy: <a href="{mailto("Privacy")}">{C.SUPPORT_EMAIL}</a>.</p>
  <p class="updated">Last updated {C.MOVED}</p>
</div></section>'''
    return dict(title="Privacy: Radd Games", desc="How Radd Games handles privacy: this website sets no cookies and uses no trackers, and each game has its own privacy policy.", body=body)


def not_found():
    body = f'''<section class="lost"><div class="wrap">
  {raddy()}
  <h1 class="h1">This page wandered off.</h1>
  <p class="lede">It was here a minute ago. Probably went to play “just one more level”.</p>
  <div class="actions" style="justify-content:center"><a class="btn" href="{u("")}">Back to the games</a><a class="btn ghost" href="{u("support/")}">Support</a></div>
</div></section>'''
    return dict(title="Page not found: Radd Games", desc="That page isn't here.", body=body, index=False)


# ---------------------------------------------------------------- game pages
def tester_band(g):
    return f'''<section class="section"><div class="wrap"><div class="band">
  <div><h2 class="h3">Want to play {e(g["name"])} early?</h2>
  <p>{e(g["name"])} is in closed testing on Android. Send us the Gmail address you use on Google Play and we'll add you to the list. We use it for that and nothing else.</p></div>
  <a class="btn" href="{tester_mail(g["name"])}">Become a tester <span class="arr">→</span></a>
</div></div></section>'''


def link_cards(g):
    s = g["slug"]
    items = [("how-to-play/", "How to play", "The rules, in plain words."), ("support/", "Support", "Common questions, and how to reach us."),
             ("privacy/", "Privacy policy", "What the game collects, and why."), ("terms/", "Terms of use", "The agreement for playing."),
             ("delete-account/", delete_label(g), "Remove what the game stores about you.")]
    return '<div class="links">' + "".join(f'<a href="{u(s + "/" + t)}"><b>{e(a)}</b><span>{e(b)}</span></a>' for t, a, b in items) + "</div>"


def game_home(g):
    def build():
        s = g["slug"]
        a, b = g["hero_shots"]
        facts = "".join(f"<li><b>{e(n)}</b>{e(t)}</li>" for n, t in g["facts"])
        feats = "".join(f'<div class="feature" data-reveal><h3>{e(h)}</h3><p>{e(t)}</p></div>' for h, t in g["features"])
        if g.get("rules"):
            teaser = f'''<section class="section"><div class="wrap"><div class="sec-head"><h2 class="h2">How it plays</h2></div>
  <ol class="steps">{"".join(f"<li><span>{e(r)}</span></li>" for r in g["rules"][:3])}</ol>
  <p style="margin-top:24px"><a class="btn ghost" href="{u(s + "/how-to-play/")}">All the rules <span class="arr">→</span></a></p></div></section>'''
        else:
            teaser = f'''<section class="section"><div class="wrap"><div class="sec-head"><h2 class="h2">Eleven games in one</h2></div>
  <p class="lede" style="margin-bottom:22px">{e(g["how_intro"])}</p>
  <a class="btn ghost" href="{u(s + "/how-to-play/")}">How to play each game <span class="arr">→</span></a></div></section>'''
        body = f'''{subnav(g, "")}
<section class="ghero"><div class="wrap"><div class="ghero-panel">
  <div class="ghero-copy">
    {img(s + "/icon", g["name"] + " app icon", "icon", lazy=False)}
    <p class="kind">{e(g["genre"])}</p>
    <h1>{e(g["name"])}</h1>
    <p class="tagline">{e(g["tagline"])}</p>
    <p class="lede">{e(g["blurb"])}</p>
    {store_buttons(g)}
    <p class="note">{e(g["status_note"])}</p>
    <ul class="facts">{facts}</ul>
  </div>
  <div class="ghero-art" aria-hidden="true">{phone(g, a, "", "a", lazy=False)}{phone(g, b, "", "b", lazy=False)}</div>
</div></div></section>
{carousel(g)}
<section class="section"><div class="wrap"><div class="sec-head"><h2 class="h2">Why you might like it</h2></div><div class="features">{feats}</div></div></section>
<section class="section"><div class="wrap"><figure class="says" data-reveal>{raddy()}<div><blockquote>“{e(g["goofy"])}”</blockquote><figcaption>Raddy, who tests everything first</figcaption></div></figure></div></section>
{teaser}
<section class="section"><div class="wrap"><div class="sec-head"><h2 class="h2">The useful pages</h2></div>{link_cards(g)}</div></section>
{tester_band(g)}'''
        ld = {"@context": "https://schema.org", "@type": "MobileApplication", "name": g["full"], "applicationCategory": "GameApplication",
              "operatingSystem": "Android, iOS", "description": g["blurb"], "url": f'{C.SITE_ORIGIN}/{s}/',
              "image": f'{C.SITE_ORIGIN}/assets/img/{s}/icon-512.png', "publisher": {"@type": "Organization", "name": C.SITE_NAME},
              "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
        return dict(title=f'{g["full"]}: Radd Games', desc=g["blurb"], body=body, game=s, og=f"og/{s}.png", ld=ld)
    return build


def prose_page(g, current, inner, title, desc, extra=""):
    return dict(title=title, desc=desc, game=g["slug"], og=f'og/{g["slug"]}.png',
                body=f'''{subnav(g, current)}
<section class="doc"><div class="narrow prose">
{inner}
</div></section>{extra}''')


def how_to(g):
    def build():
        s = g["slug"]
        if s == "inkbloom":
            games = json.loads(read("pages", "inkbloom", "games.json"))
            def cards(tag):
                return "".join(f'<a class="game-card" href="{u(s + "/how-to-play/" + x["slug"] + "/")}"><span class="{x["tagcls"]}">{e(x["tag"])}</span><h3>{x["name"]}</h3>{x["vig"]}<p>{x["essence"]}</p></a>'
                               for x in games if x["tag"] == tag)
            body = f'''{subnav(g, "how-to-play/")}
{page_head("How to play", "How to play Inkbloom", "Rules, controls and tips for all eleven Inkbloom games.")}
<section class="section"><div class="wrap"><div class="sec-head"><h2 class="h2">On every daily page</h2><p>These five appear every day.</p></div><div class="games">{cards("On every daily page")}</div></div></section>
<section class="section"><div class="wrap"><div class="sec-head"><h2 class="h2">Taking turns</h2><p>These six rotate onto the daily page, and all of them are always in the Library.</p></div><div class="games">{cards("Rotates onto the page")}</div></div></section>
<section class="section"><div class="wrap"><div class="band"><div><h2 class="h3">Hints</h2><p>Every game has a hint for when you're stuck. Hints cost ink drops, which you earn by playing; with Inkbloom Plus they're unlimited. Library practice puzzles are untimed and unranked, so take as long as you like.</p></div></div></div></section>'''
            return dict(title="How to play Inkbloom: Radd Games", desc="Rules, controls and tips for all eleven Inkbloom games: nonogram, sudoku, word search, cross math, block puzzle and more.",
                        body=body, game=s, og=f"og/{s}.png")
        parts = [f'<h1>How to play {e(g["name"])}</h1>', f'<p class="lede">{e(g["tagline"])}</p>', '<h2>The rules</h2>',
                 '<ol class="steps">' + "".join(f"<li><span>{e(r)}</span></li>" for r in g["rules"]) + "</ol>"]
        if s == "lumiwire":
            parts.append("<h2>Stars</h2><ul>" + "".join(f"<li><strong>{n} stars.</strong> {e(t)}</li>" for n, t in g["stars"]) + "</ul>")
            parts.append("<h2>Three ways to play</h2>" + "".join(f"<h3>{e(n)}</h3><p>{e(t)}</p>" for n, t in g["modes"]))
            parts.append('<h2>The circuit tricks</h2><p>Each chapter adds one new idea, introduced on an easy board with a one-line tip.</p><div class="tablewrap"><table><thead><tr><th>Trick</th><th>Arrives</th><th>How it works</th></tr></thead><tbody>'
                         + "".join(f"<tr><td><strong>{e(n)}</strong></td><td>Level&nbsp;{lv}</td><td>{e(r)}</td></tr>" for n, ch, lv, r in g["obstacles"]) + "</tbody></table></div>")
            parts.append('<h2>The chapters</h2><div class="tablewrap"><table><thead><tr><th>Chapter</th><th>Levels</th><th>What it teaches</th></tr></thead><tbody>'
                         + "".join(f"<tr><td><strong>{e(n)}</strong></td><td>{a}–{b}</td><td>{e(t)}</td></tr>" for n, a, b, t in g["chapters"]) + "</tbody></table></div>")
        if s == "shapelings":
            parts.append("<h2>Good to know</h2>" + "".join(f"<h3>{e(h)}</h3><p>{e(t)}</p>" for h, t in g["features"][:4]))
        if s == "loopo":
            def rows(items):
                return '<div class="list">' + "".join(f'<div class="row">{img("loopo/" + k, "")}<p><b>{e(n)}.</b> {e(t)}</p></div>' for k, n, t in items) + "</div>"
            parts.append("<h2>The three powers</h2>" + rows(g["powers"]) + f'<p style="margin-top:14px">{e(g["pocket"])}</p>')
            parts.append("<h2>Also in the water</h2>" + rows(g["extras"]))
            parts.append("<h2>Two ways to play</h2>" + "".join(f"<h3>{e(n)}</h3><p>{e(t)}</p>" for n, t in g["modes"]))
            parts.append(f'<p class="note">{e(g["status_note"])}</p>')
        parts.append(f'<p style="margin-top:26px">Still stuck? The <a href="{u(s + "/support/")}">support page</a> has the common questions.</p>')
        return prose_page(g, "how-to-play/", "\n".join(parts), f'How to play {g["name"]}: Radd Games', f'The rules of {g["name"]} in plain words: {g["tagline"]}')
    return build


def inkbloom_game(g, games, i):
    def build():
        x = games[i]
        inner = read("pages", "inkbloom", "games", x["slug"] + ".html")
        prev = f'<a href="{u("inkbloom/how-to-play/" + games[i - 1]["slug"] + "/")}">← {games[i - 1]["name"]}</a>' if i > 0 else "<span></span>"
        nxt = f'<a href="{u("inkbloom/how-to-play/" + games[i + 1]["slug"] + "/")}">{games[i + 1]["name"]} →</a>' if i < len(games) - 1 else "<span></span>"
        inner = (f'<p class="crumb muted"><a href="{u("inkbloom/how-to-play/")}">How to play Inkbloom</a> / {x["name"]}</p>'
                 + inner + f'<nav class="next-prev" aria-label="Other games">{prev}{nxt}</nav>')
        return prose_page(g, "how-to-play/", inner, f'How to play {html.unescape(x["name"])} in Inkbloom: Radd Games',
                          f'{html.unescape(x["name"])} in Inkbloom: {html.unescape(x["essence"])} Rules, controls and tips.')
    return build


def support(g):
    def build():
        s = g["slug"]
        if s == "inkbloom":
            faq = read("pages", "inkbloom", "faq.html")
        else:
            faq = "".join(f'<details class="faq"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in g["faq"])
        inner = f'''<h1>{e(g["name"])} support</h1>
<p class="lede">Something not right, or a question we haven't answered? Write to us.</p>
<div class="contact contact-card"><span class="muted">Email</span>
  <a class="email" href="{mailto(g["name"] + " support")}">{C.SUPPORT_EMAIL}</a>
  <p class="muted" style="margin:0">It helps to include your phone model, its Android or iOS version, and a screenshot if something looks wrong. We read every message and usually reply within two working days.</p></div>
<h2>Common questions</h2>
{faq}
<h2>Your data</h2>
<p>Read the <a href="{u(s + "/privacy/")}">privacy policy</a> and the <a href="{u(s + "/terms/")}">terms of use</a>. To remove what the game stores about you, see <a href="{u(s + "/delete-account/")}">{e(delete_label(g).lower())}</a>.</p>'''
        return prose_page(g, "support/", inner, f'{g["name"]} support: Radd Games', f'Help with {g["name"]}: common questions, purchases, your data, and how to contact us at {C.SUPPORT_EMAIL}.')
    return build


def legal(g, name):
    def build():
        s = g["slug"]
        b = read("legal", s, name + ".html")
        start, end = "<!--IF_SHOP_NOT_LIVE-->", "<!--END-->"
        while start in b:
            i, j = b.index(start), b.index(end)
            b = b[:i] + ("" if g.get("shop_live", True) else b[i + len(start):j]) + b[j + len(end):]
        fill = {"{{EMAIL}}": C.SUPPORT_EMAIL, "{{UPDATED}}": g["legal_dates"].get(name, ""), "{{PRIVACY}}": u(s + "/privacy/"),
                "{{TERMS}}": u(s + "/terms/"), "{{DELETE}}": u(s + "/delete-account/"), "{{SUPPORT}}": u(s + "/support/"), "{{HOME}}": u(s + "/")}
        for k, v in fill.items():
            b = b.replace(k, v)
        assert "{{" not in b, (s, name, re.findall(r"\{\{[^}]*\}\}", b))
        b += f'\n<p class="moved">This page moved to raddgames.com on {C.MOVED}. Only the contact address and the publisher\'s name (Radd) changed.</p>'
        label = {"privacy": "privacy policy", "terms": "terms of use", "delete-account": delete_label(g).lower()}[name]
        descs = {"privacy": f'What {g["name"]} collects, why, who handles it, and what you can do about it.',
                 "terms": f'The terms for using {g["name"]}.',
                 "delete-account": f'How to delete what {g["name"]} stores about you, what is removed, and what is kept.'}
        title = f'{g["name"]} {label}: Radd Games' if name != "delete-account" else f'{delete_label(g)} in {g["name"]}: Radd Games'
        return prose_page(g, name + "/", b.strip(), title, descs[name])
    return build


# ---------------------------------------------------------------- everything else
def build_misc():
    shutil.copytree(os.path.join(ROOT, "static"), OUT, dirs_exist_ok=True)
    os.makedirs(os.path.join(OUT, "assets", "fonts"), exist_ok=True)
    for f in os.listdir(os.path.join(ROOT, "fonts")):
        shutil.copy(os.path.join(ROOT, "fonts", f), os.path.join(OUT, "assets", "fonts", f))
    shutil.copy(os.path.join(ROOT, "src", "site.css"), os.path.join(OUT, "assets", "site.css"))
    shutil.copy(os.path.join(ROOT, "src", "site.js"), os.path.join(OUT, "assets", "site.js"))
    write("app-ads.txt", C.APP_ADS + "\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {C.SITE_ORIGIN}/sitemap.xml\n")
    write(".well-known/security.txt", f"Contact: mailto:{C.SUPPORT_EMAIL}\nPreferred-Languages: en\nCanonical: {C.SITE_ORIGIN}/.well-known/security.txt\nExpires: 2027-11-26T00:00:00.000Z\n")
    write("CNAME", C.SITE_ORIGIN.split("//")[1] + "\n")
    write(".nojekyll", "")
    urls = "".join(f"  <url><loc>{C.SITE_ORIGIN}/{p}</loc></url>\n" for p in PAGES)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')


def check_links():
    """Every relative href and src in the built pages must point at a file that exists."""
    bad = []
    for base, _, files in os.walk(OUT):
        for f in files:
            if not f.endswith(".html"):
                continue
            page = os.path.join(base, f)
            text = open(page, encoding="utf-8").read()
            for ref in re.findall(r'(?:href|src)="([^"]+)"', text):
                if ref.startswith(("http:", "https:", "mailto:", "#", "data:")):
                    continue
                ref = ref.split("#")[0]
                target = os.path.join(OUT, ref.lstrip("/")) if ref.startswith("/") else os.path.normpath(os.path.join(base, ref))
                if os.path.isdir(target):
                    target = os.path.join(target, "index.html")
                if not os.path.exists(target):
                    bad.append((os.path.relpath(page, OUT), ref))
    if bad:
        for b in bad[:40]:
            print("BROKEN", b)
        sys.exit(1)


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    build_images()
    emit("", home)
    emit("support/", support_hub)
    emit("about/", about)
    emit("privacy/", privacy_hub)
    for g in C.GAMES:
        s = g["slug"]
        emit(f"{s}/", game_home(g))
        emit(f"{s}/how-to-play/", how_to(g))
        emit(f"{s}/support/", support(g))
        for name in ("privacy", "terms", "delete-account"):
            emit(f"{s}/{name}/", legal(g, name))
    ink = C.BY_SLUG["inkbloom"]
    games = json.loads(read("pages", "inkbloom", "games.json"))
    for i, x in enumerate(games):
        emit(f'inkbloom/how-to-play/{x["slug"]}/', inkbloom_game(ink, games, i))
    emit("404.html", not_found, absolute=True)
    build_misc()
    check_links()
    print(f"built {len(PAGES) + 1} pages into {OUT}" + (" (preview links)" if PREVIEW else ""))


main()
