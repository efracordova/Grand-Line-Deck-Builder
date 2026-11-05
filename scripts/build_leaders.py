import json, collections, sys
cards = json.load(open(sys.argv[1])); groups = json.load(open(sys.argv[5]))['results']; ban = json.load(open(sys.argv[2])); fmt = json.load(open(sys.argv[3])); out = sys.argv[4]
by = collections.defaultdict(list)
for c in cards: by[c['card_number']].append(c)
def eff_block(num):
    if num in fmt['block_override']: return fmt['block_override'][num]
    icons = {c['block_icon'] for c in by[num] if c['block_icon']}
    if num in fmt['block_always_legal'] or 'X' in icons: return 'X'
    nums = [int(i) for i in icons if i.isdigit()]
    return str(max(nums)) if nums else None
RULE_NOTES = {
 'OP12-001': 'Deck rule: you cannot include cards with a cost of 5 or more.',
 'OP13-079': 'Deck rule: you cannot include Events with a cost of 2 or more. Starts the game with a {Mary Geoise} Stage in play.',
 'P-117': 'Deck rule: you can only include {East Blue} type cards. You win instead of losing when your deck runs out.',
 'OP15-058': 'Game rule: your DON!! deck has only 6 cards.',
 'OP03-040': 'Game rule: you win instead of losing when your deck runs out.',
 'OP15-022': 'Game rule: you don\'t lose immediately at 0 cards in deck; you lose at the end of that turn.',
 'ST13-003': 'Game rule: face-up Life cards go to the bottom of your deck instead of your hand.',
}
rel = {}
for g in groups:
    ab = g['abbreviation'].split(' ')[0].replace('-', '')
    for part in ab.split('EB04') if ab.startswith('OP1') and 'EB04' in ab else [ab]:
        if part and (part not in rel or g['publishedOn'] < rel[part]): rel[part] = g['publishedOn'][:10]
rel.setdefault('EB04', rel.get('OP14', ''))
banned = set(ban['banned']); pairs = ban['banned_pairs']
leaders = []
for num, prints in by.items():
    base = next((p for p in prints if not p['is_alt_art']), prints[0])
    if base['category'] != 'Leader': continue
    b = eff_block(num)
    is_banned = num in banned
    legal_std = (b == 'X' or (b and b.isdigit() and int(b) >= fmt['standard']['min_block'])) and not is_banned
    rotates = b and b.isdigit() and int(b) < fmt['standard']['next_rotation']['min_block'] and legal_std
    arts = [{'id': p['id'], 'image': p['image_url'], 'from': p['card_sets'], 'rarity': p['rarity'], 'price': p['tcgplayer_market_price']} for p in sorted(prints, key=lambda p: (p['is_alt_art'], p['id']))]
    leaders.append({
      'num': num, 'name': base['name'], 'colors': base['colors'], 'life': base['life'], 'power': base['power'],
      'attribute': base['attribute'], 'types': base['types'], 'effect': base['effect'], 'set': base['set_name'],
      'block': b, 'banned': is_banned,
      'banned_with': [p[1] if p[0] == num else p[0] for p in pairs if num in p],
      'legal': {'standard': bool(legal_std), 'extra': not is_banned, 'casual': True},
      'rotates_2027': bool(rotates), 'rule_note': RULE_NOTES.get(num), 'arts': arts,
      'popularity': None, 'released': rel.get(num.split('-')[0], ''),
    })
leaders.sort(key=lambda l: l['num'])
json.dump(leaders, open(out, 'w'), ensure_ascii=False, separators=(',', ':'))
c = collections.Counter((len(l['colors']), l['legal']['standard']) for l in leaders)
print(len(leaders), c, 'banned', [l['num'] for l in leaders if l['banned']], 'pairs', [(l['num'], l['banned_with']) for l in leaders if l['banned_with']])
print('pairings', len({'/'.join(sorted(l['colors'])) for l in leaders if len(l['colors'])==2}))
print('pairings std', collections.Counter('/'.join(l['colors']) for l in leaders if len(l['colors'])==2 and l['legal']['standard']))
