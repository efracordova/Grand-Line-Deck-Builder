# Grand Line Deck Builder

A free, static web app for building One Piece Card Game decks: pick a format, Leader color and Leader, then build a 50-card deck with legality checks, stats, a test hand, and comparisons against winning tournament decklists.

## Run it

Everything the page needs sits next to `index.html` (`leaders.json`, `cards.json`, `meta.json`, `art-*.json`). Because the page loads those files with `fetch`, open it through a web server rather than double-clicking it:

```
python3 -m http.server 8000
```

Then visit http://localhost:8000. On GitHub Pages, publish from the repo root (Settings → Pages). Free Pages hosting needs a public repo on a free GitHub account.

## Folders

- `index.html`, `*.json` at the root: the app and the data it loads.
- `data/`: source data (`optcg_cards.json` full card list, `formats.json` block rotation rules, `banlist.json`).
- `scripts/`: Python scripts that rebuild the data (see `docs/data-sources.md`).
- `docs/`: notes on data sources and product decisions.

## Data

Card text and images: Bandai's official One Piece Card Game card list. Prices: TCGplayer via optcgapi.com. Tournament results: Limitless TCG. Card images carry Bandai's "SAMPLE" watermark.
