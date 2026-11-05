import sys, os, re, json, html, glob
from html.parser import HTMLParser
src = sys.argv[1]; out = sys.argv[2]
def clean(s):
    s = re.sub(r'<br\s*/?>', '\n', s); s = re.sub(r'<[^>]+>', '', s)
    return html.unescape(s).strip()
def field(block, cls):
    m = re.search(r'<div class="%s">(.*?)</div>' % cls, block, re.S)
    if not m: return None, None
    inner = m.group(1); h = re.search(r'<h3>(.*?)</h3>', inner, re.S)
    label = clean(h.group(1)) if h else None
    val = clean(re.sub(r'<h3>.*?</h3>', '', inner, flags=re.S))
    return label, val
cards = {}
for f in sorted(glob.glob(os.path.join(src, '*.html'))):
    s = open(f, encoding='utf-8').read()
    for m in re.finditer(r'<dl class="modalCol" id="([^"]+)">(.*?)</dl>', s, re.S):
        cid, b = m.group(1), m.group(2)
        info = [clean(x) for x in re.findall(r'<span>(.*?)</span>', re.search(r'<div class="infoCol">(.*?)</div>', b, re.S).group(1))]
        name = clean(re.search(r'<div class="cardName">(.*?)</div>', b, re.S).group(1))
        img = re.search(r'data-src="\.\./images/cardlist/card/([^"?]+)', b)
        cl, cv = field(b, 'cost')
        attrm = re.search(r'<div class="attribute">(.*?)</div>', b, re.S)
        attr = clean(re.search(r'<i>(.*?)</i>', attrm.group(1), re.S).group(1)) if attrm and '<i>' in attrm.group(1) else None
        _, power = field(b, 'power'); _, counter = field(b, 'counter'); _, color = field(b, 'color')
        _, block = field(b, 'block'); _, typ = field(b, 'feature'); _, eff = field(b, 'text')
        _, trig = field(b, 'trigger'); _, sets = field(b, 'getInfo')
        nil = lambda v: None if v in (None, '', '-') else v
        num = lambda v: int(v) if v and re.fullmatch(r'-?\d+', v) else None
        cat = info[2].title() if len(info) > 2 else None
        rec = {
          'id': cid, 'card_number': info[0], 'is_alt_art': cid != info[0],
          'name': name, 'category': cat, 'rarity': info[1],
          'color': nil(color), 'colors': nil(color).split('/') if nil(color) else [],
          'cost': num(cv) if cl == 'Cost' else None, 'life': num(cv) if cl == 'Life' else None,
          'power': num(power), 'counter': num(counter),
          'attribute': nil(attr), 'types': nil(typ).split('/') if nil(typ) else [], 'types_text': nil(typ),
          'effect': nil(eff), 'trigger': nil(trig), 'block_icon': nil(block),
          'card_sets': nil(sets), 'set_code': (re.findall(r'\[([^\]]+)\]', sets or '') or [None])[-1],
          'image_url': 'https://en.onepiece-cardgame.com/images/cardlist/card/' + img.group(1) if img else None,
        }
        cards.setdefault(cid, rec)
json.dump(list(cards.values()), open(out, 'w'), ensure_ascii=False, indent=1)
print(len(cards))
