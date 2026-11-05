# OPTCG Deck Builder — Card Data (updated 2026-11-05)

## Status
Card database built: `data/optcg_cards.json` — 4,945 printings (2,850 unique cards + alt arts), every set on the official English site through OP17, EB05, PRB02, ST01–ST36, plus promos (P-xxx) and "Other Product" cards. OP18 (releases 2026-11-20) not yet on official site.

## Sources used
1. **Official Bandai card list** (en.onepiece-cardgame.com/cardlist/?series=<id>) — primary source for all stats/text. One page per series (63 series IDs from the page's `series` dropdown).
2. **OPTCG API** (optcgapi.com /api/allSetCards/, /api/allSTCards/) — TCGPlayer market prices joined by card id (4,270 of 4,945 priced). Also used to confirm "-" on the official site means 0.
3. **tcgcsv.com** (/tcgplayer/68/groups) — TCGPlayer set names.

## Fields
id, card_number, is_alt_art, name, category (Leader/Character/Event/Stage), color, colors[], cost, life (Leaders), power, counter, attribute, attributes[], types[] / types_text (affiliation), effect, trigger, rarity, block_icon (format rotation), set_code, set_name, card_sets (where this printing came from), tcgplayer_market_price, price_date, image_url.

## Data rules
- Official site shows "-" for zero: Character power/counter and Event/Stage cost are set to 0. Leaders have no cost/counter.
- Alt arts use Bandai ids with _p1/_r1 suffixes; card_number is the playable identity (deck limit of 4 applies per card_number).
- EB04 cards were split across the OP14-EB04 and OP15-EB04 packs; set_name follows the base card.
- DON!! cards are excluded (not part of the 50-card deck).

## Refresh
`scripts/parse_official.py <dir of series html> official_cards.json`, then `scripts/build_cards.py <raw dir> official_cards.json <outdir>` (raw dir holds allSetCards.json, allSTCards.json, tcg_groups.json).

## App plan
Free static web app (HTML/JS) reading the card JSON; host as a Claude artifact or GitHub Pages.
