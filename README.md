# raddgames.com

The Radd Games studio site: one home for Inkbloom, Lumiwire, Shapelings and Loopo.
Plain static files, no framework, no cookies, no trackers, nothing loaded from other companies.

## Build

    pip install pillow
    python build.py                 # writes docs/ (what GitHub Pages serves)
    python build.py preview --preview   # a copy you can open from disk: preview/index.html

The build stops if any link or picture in the built pages points at a file that isn't there.

## Where things live

| What | Where |
| --- | --- |
| Words, facts, store links, the support email | `content.py` |
| Lumiwire's and Shapelings' facts (copied from their old sites) | `content_lumiwire.py`, `content_shapelings.py` |
| Privacy policy, terms, delete page for each game | `legal/<game>/` (body only, with `{{EMAIL}}` style placeholders) |
| Inkbloom's eleven how-to pages and its FAQ | `pages/inkbloom/` |
| Pictures (PNG sources; the build makes WebP) | `images/<game>/` |
| Look and scripts | `src/site.css`, `src/site.js` |
| Favicon, share cards, files copied as they are | `static/` (drawn by `tools/make_brand.py`) |
| Fonts (self-hosted, SIL Open Font License) | `fonts/` |

## The addresses (don't change these: stores and apps link to them)

    /<game>/                  about the game
    /<game>/how-to-play/
    /<game>/support/
    /<game>/privacy/
    /<game>/terms/
    /<game>/delete-account/
    /app-ads.txt              one AdMob line for every game

`<game>` is `inkbloom`, `lumiwire`, `shapelings` or `loopo`.

## Common jobs

- **A game goes live in a store:** in `content.py` set `play_live` / `appstore_live` (and `appstore_url`), build, push.
- **New screenshots:** replace `images/<game>/screen-N.png` (same names), build, push. Captions are in `content.py` (`shots`).
- **A policy changes:** edit `legal/<game>/<page>.html`, update its date, build, push. The same text must be what the store listing links to.
- **A new game:** add a block to `GAMES` in `content.py`, a world in `src/site.css` (`[data-world="<slug>"]`), pictures in `images/<slug>/`, three files in `legal/<slug>/`, then `python tools/make_brand.py` for its share card.
- **The support email:** `SUPPORT_EMAIL` in `content.py`. It appears on every page and in every policy.

## Legal texts

The policies, terms and delete pages were carried over on 26 November 2026 from each game's own site
(inkbloompuzzles.com, lumiwire-site, shapelings-site, loopo-privacy), word for word. Only the contact address changed.
