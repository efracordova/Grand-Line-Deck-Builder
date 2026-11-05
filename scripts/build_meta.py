import json, glob, collections, os, sys
FROM = sys.argv[1] if len(sys.argv) > 1 else '2026-10-12'
WFROM = sys.argv[2] if len(sys.argv) > 2 else '2026-08-28'
BAN = json.load(open('../banlist.json')); BANNED = set(BAN['banned'])
T = {t['id']: t for t in json.load(open('tournaments.json'))}
cards = {c['n']: c for c in json.load(open('../site/cards.json'))['cards']}
cid = lambda x: f"{x['set']}-{x['number']}"
lead = collections.Counter(); rec = collections.defaultdict(lambda: [0, 0, 0])
mu = collections.defaultdict(lambda: [0, 0, 0])  # (A,B) -> A wins, A losses, ties
winners = collections.defaultdict(list); unknown = collections.Counter(); events = 0; matches = 0; players = 0
for f in glob.glob('raw/*_standings.json'):
    tid = os.path.basename(f).split('_')[0]; t = T[tid]
    if t['date'][:10] < WFROM: continue
    recent = t['date'][:10] >= FROM
    S = json.load(open(f)); P = json.load(open(f.replace('standings', 'pairings')))
    pl = {}
    for s in S:
        d = s.get('decklist') or {}
        if not d.get('leader'): continue
        L = cid(d['leader'])
        if recent: pl[s['player']] = L; lead[L] += 1
        n = t['players']; cut = 8 if n >= 32 else 4 if n >= 16 else 2
        allc = {cid(c) for sec in ('character','event','stage') for c in d.get(sec, [])} | {L}
        if s.get('placing') and s['placing'] <= cut and not (allc & BANNED) and not any(a in allc and b in allc for a, b in BAN['banned_pairs']):
            cs = {}
            for sec in ('character', 'event', 'stage'):
                for c in d.get(sec, []):
                    k = cid(c); cs[k] = cs.get(k, 0) + c['count']
                    if k not in cards: unknown[k] += 1
            winners[L].append({'cards': cs, 'place': s['placing'], 'players': n, 'event': t['name'], 'date': t['date'][:10], 'record': s.get('record')})
    if pl: events += 1; players += len(pl)
    for m in P:
        a, b, w = m.get('player1'), m.get('player2'), m.get('winner')
        if not a or not b or a not in pl or b not in pl: continue
        la, lb = pl[a], pl[b]; matches += 1
        if w == a: r = (0, 1)
        elif w == b: r = (1, 0)
        else: r = None
        for (x, y, idx) in ((la, lb, 0), (lb, la, 1)):
            if r is None: mu[(x, y)][2] += 1; rec[x][2] += 1
            else:
                won = (r[0] == 0) if idx == 0 else (r[1] == 0)
                mu[(x, y)][0 if won else 1] += 1; rec[x][0 if won else 1] += 1
# leader summary
tot = sum(lead.values())
summary = {}
for L, n in lead.items():
    w, l, t_ = rec[L]; g = w + l + t_
    summary[L] = {'players': n, 'share': round(n / tot * 100, 1), 'w': w, 'l': l, 't': t_, 'wr': round(w / (w + l) * 100, 1) if w + l else None}
matchups = {}
for (a, b), (w, l, t_) in mu.items():
    if a == b: continue
    matchups.setdefault(a, {})[b] = [w, l, t_]
# winning deck profiles
def stats(cs):
    tot = sum(cs.values()); o = {'C': 0, 'E': 0, 'S': 0, 'c1': 0, 'c2': 0, 'blk': 0, 'trg': 0, 'cev': 0, 'cost': 0, 'curve': [0] * 11}
    for k, q in cs.items():
        c = cards.get(k)
        if not c: continue
        o[c['c']] += q; o['c1'] += q * (c['ct'] == 1000); o['c2'] += q * (c['ct'] == 2000)
        o['blk'] += q * ('Blocker' in c['kw']); o['trg'] += q * ('Trigger' in c['kw']); o['cev'] += q * ('Counter Event' in c['kw'])
        o['cost'] += q * (c['cost'] or 0); o['curve'][min(c['cost'] or 0, 10)] += q
    o['avgcost'] = round(o['cost'] / tot, 2) if tot else 0; del o['cost']; return o
profiles = {}
for L, lists in winners.items():
    ss = [stats(x['cards']) for x in lists]; n = len(lists)
    keys = ['C', 'E', 'S', 'c1', 'c2', 'blk', 'trg', 'cev', 'avgcost']
    rng = {k: [min(s[k] for s in ss), round(sum(s[k] for s in ss) / n, 1), max(s[k] for s in ss)] for k in keys}
    curve = [round(sum(s['curve'][i] for s in ss) / n, 1) for i in range(11)]
    inc = collections.Counter(); cop = collections.Counter()
    for x in lists:
        for k, q in x['cards'].items(): inc[k] += 1; cop[k] += q
    core = [{'n': k, 'pct': round(inc[k] / n * 100), 'avg': round(cop[k] / inc[k], 1)} for k in sorted(inc, key=lambda k: (-inc[k], -cop[k]))]
    best = sorted(lists, key=lambda x: (x['place'] > 2, x['date']), reverse=False)
    best = sorted([x for x in lists if x['place'] <= 2], key=lambda x: x['date'], reverse=True)[:5] or sorted(lists, key=lambda x: x['date'], reverse=True)[:5]
    profiles[L] = {'lists': n, 'ranges': rng, 'curve': curve, 'cards': core[:40], 'examples': best}
meta = {'source': 'Limitless TCG online tournaments (play.limitlesstcg.com)', 'from': FROM, 'from_reason': 'Current banned list took effect Oct 12, 2026', 'to': max(t['date'][:10] for t in T.values()),
        'events': events, 'players': players, 'matches': matches, 'format': 'Standard', 'winning_from': WFROM, 'winning_note': 'Winning lists from Aug 28, 2026 on, excluding any list with a now-banned card or pair', 'winning_definition': 'Top 2 (8–15 players), top 4 (16–31), top 8 (32+)'}
json.dump({'meta': meta, 'leaders': summary, 'matchups': matchups, 'winning': profiles}, open('../site/meta.json', 'w'), separators=(',', ':'))
print(meta, 'leaders', len(summary), 'profiles', len(profiles), sum(p['lists'] for p in profiles.values()), 'unknown', unknown.most_common(5))
top = sorted(summary.items(), key=lambda kv: -kv[1]['players'])[:10]
for L, s in top: print(L, s, profiles.get(L, {}).get('lists'))
