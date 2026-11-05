import json, collections, sys, re
cards = json.load(open(sys.argv[1])); ban = json.load(open(sys.argv[2])); fmt = json.load(open(sys.argv[3])); out = sys.argv[4]
by = collections.defaultdict(list)
for c in cards: by[c['card_number']].append(c)
def eff_block(num):
    if num in fmt['block_override']: return fmt['block_override'][num]
    icons = {c['block_icon'] for c in by[num] if c['block_icon']}
    if num in fmt['block_always_legal'] or 'X' in icons: return 'X'
    nums = [int(i) for i in icons if i.isdigit()]
    return str(max(nums)) if nums else None
KW = [('Blocker', r'\[Blocker\]'), ('Rush', r'\[Rush(: Character)?\]'), ('Double Attack', r'\[Double Attack\]'), ('Banish', r'\[Banish\]'),
      ('Unblockable', r'\[Unblockable\]'), ('On Play', r'\[On Play\]'), ('When Attacking', r'\[When Attacking\]'), ('On K.O.', r'\[On K\.O\.\]'),
      ('Activate: Main', r'\[Activate: ?Main\]'), ('Counter Event', r'\[Counter\]'), ('Draw', r'\bdraw \d|\bdraw a card'), ('Removal', r'K\.O\. up to|return up to \d+ of your opponent|place up to \d+ of your opponent|to the bottom of the owner')]
banned = set(ban['banned']); cat = {'Character': 'C', 'Event': 'E', 'Stage': 'S'}
res = []
for num, prints in by.items():
    b = next((p for p in prints if not p['is_alt_art']), prints[0])
    if b['category'] == 'Leader': continue
    blk = eff_block(num); ef = b['effect'] or ''
    kw = [k for k, rx in KW if re.search(rx, ef, re.I if k in ('Draw', 'Removal') else 0)]
    if b['trigger']: kw.append('Trigger')
    std = (blk == 'X' or (blk and blk.isdigit() and int(blk) >= fmt['standard']['min_block']))
    prices = [p['tcgplayer_market_price'] for p in prints if p['tcgplayer_market_price'] is not None and not p['is_alt_art']] or [p['tcgplayer_market_price'] for p in prints if p['tcgplayer_market_price'] is not None]
    res.append({'n': num, 'nm': b['name'], 'c': cat[b['category']], 'col': b['colors'], 'cost': b['cost'], 'pw': b['power'], 'ct': b['counter'],
        'at': b['attribute'], 'ty': b['types'], 'ef': b['effect'], 'tr': b['trigger'], 'r': b['rarity'], 'bk': blk, 'st': b['set_name'], 'p': min(prices) if prices else None,
        'img': b['id'], 'kw': kw, 'unl': bool(re.search(r'you may have any number of this card in your deck', ef)),
        'ban': num in banned, 'std': bool(std), 'rot': bool(std and blk.isdigit() and int(blk) < fmt['standard']['next_rotation']['min_block'])})
res.sort(key=lambda x: x['n'])
json.dump({'banned_pairs': ban['banned_pairs'], 'cards': res}, open(out, 'w'), ensure_ascii=False, separators=(',', ':'))
print(len(res), collections.Counter(x['c'] for x in res), 'std', sum(x['std'] for x in res), 'unl', [x['n'] for x in res if x['unl']], 'ban', [x['n'] for x in res if x['ban']])
print(collections.Counter(k for x in res for k in x['kw']))
