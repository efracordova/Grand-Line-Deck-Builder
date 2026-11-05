# OPTCG Deck Builder — Product Decisions & Status (updated 2026-11-05)

## Live build
Artifact "Grand Line Deck Builder" (v4): https://claude.ai/artifact/LwwpnAcV2KKaN3pUX9zFs4
Source: `index.html`. Data files: leaders.json, cards.json (2,707 deck cards; rebuild with `scripts/build_deckcards.py`), meta.json (tournament results; `scripts/build_meta.py`), art-base.json / art-alt.json (Leader art), art-<Color>.json (deck card art, ~6.5MB per color).
Bandai's images carry a "SAMPLE" watermark; TCGplayer product images are a possible clean alternative for a public version.

## Flow
1. Format — Standard (default) / Extra Regulation / Casual.
2. Leader color — six colors + Two-Color with a 15-pairing filter.
3. Leader — grid + detail sheet (art picker, rules notes, legality, major-tournament popularity, online win rate with best/toughest matchups).
4. Build your deck — card browser + deck panel with tabs:
   - Deck: grouped list, issues, legality chips for all three formats.
   - Stats: type split, curve, counters, Blockers, Triggers, est. price.
   - Compare: your deck vs winning decklists for the same Leader — range bars (min–max, average), curve overlay, core cards with inclusion % and Missing/✓, "Copy as new deck" from recent winning lists.
   - Matchups: Leader's overall win rate, all matchups with win bars, and a "stress-test against a specific Leader" picker.
   - Test hand: sample hand, mulligan, opening-hand odds.
   - Save on device (DeckStore adapter), My decks, export/import (OPTCG Simulator text format).

## Tournament data (meta.json)
- Source: play.limitlesstcg.com API — /tournaments?game=OP, /tournaments/{id}/standings (decklists, placing, record), /pairings (winners).
- Win rates and matchups: online Standard events since 2026-10-12 (current banned list) — 21 events, 823 players, 1,758 matches as of 2026-11-04. Matchups need ≥8 games to show as reliable.
- Winning lists: top 2 (8–15 players), top 4 (16–31), top 8 (32+), from 2026-08-28, excluding lists with now-banned cards/pairs — 265 lists across 36 Leaders. Compare needs ≥3 lists.
- Online meta differs from major in-person events (popularity box uses onepiece.limitlesstcg.com major-tournament placings).

## Decisions
- Accounts wanted eventually; device storage for now via swappable DeckStore.
- Alt arts grouped by card_number. Standard legality from `data/formats.json`; ban list `data/banlist.json` (2026-10-12).
- Full automated game simulator judged too large for now (every card effect + AI). Tournament matchup data used instead for stress-testing.

## Next up
- Refresh routine (new sets: OP18 on 2026-11-20; weekly tournament data).
- Beginner difficulty tags (Claude drafts, Efra reviews); starter-deck links.
- Accounts (Supabase/Firebase free tier) when ready.
