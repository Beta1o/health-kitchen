import json,re
out=json.load(open('/mnt/c/WSL/davita/translations/out_b0.json'))
frac=re.compile(r'(?<![\d/])(1/2|1/3|2/3|1/4|3/4|1/8)(?![\d/])')
for o in out:
  a=o['translations']['ar']
  ts=[a['title'],a['description'] or '',a['portions'] or '',a['serving_size'] or '']+[p[1] for k in('ingredients','steps','hints') for p in a[k]]+a['food_choices']
  for t in ts:
    if frac.search(t): print('FRAC',o['id'],t[:80])
    if t.count('فهرنهايت')!=t.count('مئوية'): print('TEMP',o['id'],t[:80])
