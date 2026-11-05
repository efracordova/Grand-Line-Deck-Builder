import re, sys, json
s = open(sys.argv[1]).read()
fmt = re.search(r'<span class="label">Format:</span>\s*([^<]+)', s)
rows = []
for m in re.finditer(r'<tr>\s*<td>(\d+)</td>(.*?)</tr>', s, re.S):
    r = m.group(2)
    num = re.search(r'/([A-Z0-9]+-\d{3})_EN', r); name = re.findall(r'<span>([^<]+)</span>', r)
    tds = re.findall(r'<td>([^<]*)</td>', r)
    rows.append({'rank': int(m.group(1)), 'num': num.group(1) if num else None, 'name': name[-1] if name else None,
                 'deck_url': (re.search(r'href="([^"]+)"', r) or [None, None])[1], 'value': tds[-2] if len(tds) >= 2 else None, 'share': tds[-1] if tds else None})
print(json.dumps({'format': fmt.group(1).strip() if fmt else None, 'rows': rows}))
