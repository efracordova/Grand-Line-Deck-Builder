import json, csv, re, sys
R = sys.argv[1]; off = json.load(open(sys.argv[2])); outdir = sys.argv[3]
api = {}
for f in ['allSetCards', 'allSTCards']:
    for x in json.load(open(R + f + '.json')): api.setdefault(x['card_image_id'], x)
setnames = {}
for x in json.load(open(R + 'tcg_groups.json'))['results']:
    a = x['abbreviation'].replace('-', '')
    if ' ' not in x['abbreviation'] and a not in setnames: setnames[a] = x['name']
setnames['P'] = 'Promotion Cards'
setnames['OP14'] = "The Azure Sea's Seven"; setnames['OP15'] = "Adventure on Kami's Island"
out = []
for c in off:
    cat = c['category']
    # Official site prints "-" for zero values
    if cat == 'Character':
        c['power'] = c['power'] if c['power'] is not None else 0
        c['counter'] = c['counter'] if c['counter'] is not None else 0
    if cat in ('Character', 'Event', 'Stage') and c['cost'] is None: c['cost'] = 0
    prefix = c['card_number'].split('-')[0]
    c['set_code'] = prefix
    c['set_name'] = setnames.get(prefix, setnames.get(prefix.replace('ST', 'ST-')) or '')
    if not c['set_name'] and c['card_sets']:
        c['set_name'] = next((v for v in setnames.values() if v.lower().replace('’',"'") in c['card_sets'].lower().replace('’',"'")), c['card_sets'])
    c['attributes'] = c['attribute'].split('/') if c['attribute'] else []
    a = api.get(c['id'])
    c['tcgplayer_market_price'] = a['market_price'] if a else None
    c['price_date'] = a['date_scraped'] if a else None
    out.append(c)
cols = ['id','card_number','is_alt_art','name','category','color','cost','life','power','counter','attribute','types_text','effect','trigger','rarity','block_icon','set_code','set_name','card_sets','tcgplayer_market_price','price_date','image_url']
json.dump(out, open(outdir + '/optcg_cards.json', 'w'), ensure_ascii=False, indent=1)
with open(outdir + '/optcg_cards.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore'); w.writeheader(); w.writerows(out)
print(len(out), 'missing set names:', sorted({c['set_code'] for c in out if not c['set_name']}))
# EB04 base cards were split across two packs: alt arts inherit their base card's set name
base = {c['id']: c['set_name'] for c in out if not c['is_alt_art']}
for c in out:
    if c['is_alt_art'] and c['card_number'] in base: c['set_name'] = base[c['card_number']]
json.dump(out, open(outdir + '/optcg_cards.json', 'w'), ensure_ascii=False, indent=1)
with open(outdir + '/optcg_cards.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore'); w.writeheader(); w.writerows(out)
