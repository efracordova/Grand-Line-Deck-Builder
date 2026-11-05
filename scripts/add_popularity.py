import json, sys
L = json.load(open(sys.argv[1])); M = json.load(open(sys.argv[2])); asof = sys.argv[3]
total = sum(int(r['value']) for r in M['rows'])
by = {r['num']: r for r in M['rows']}
for l in L:
    r = by.get(l['num'])
    l['popularity'] = {'rank': r['rank'], 'placings': int(r['value']), 'share': round(int(r['value']) / total * 100, 1),
                       'url': 'https://onepiece.limitlesstcg.com' + r['deck_url']} if r else None
meta = {'format': M['format'], 'total_placings': total, 'leaders_ranked': len(by), 'as_of': asof,
        'source': 'https://onepiece.limitlesstcg.com/decks?rank=count'}
json.dump({'meta': meta, 'leaders': L}, open(sys.argv[4], 'w'), ensure_ascii=False, separators=(',', ':'))
missing = [n for n in by if n not in {l['num'] for l in L}]
print(meta, 'unmatched:', missing)
