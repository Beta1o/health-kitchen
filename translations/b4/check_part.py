import json, sys, re, importlib.util
sys.path.insert(0, '/mnt/c/WSL/davita/translations')
spec = importlib.util.spec_from_file_location('cc', '/mnt/c/WSL/davita/translations/crosscheck.py')
cc = importlib.util.module_from_spec(spec); spec.loader.exec_module(cc)
n = sys.argv[1]
jobs = {j['id']: j for j in json.load(open('/mnt/c/WSL/davita/translations/jobs_b4.json'))}
out = json.load(open(f'/mnt/c/WSL/davita/translations/out_b4_part{n}.json'))
KEYS = ("title","description","portions","serving_size","ingredients","steps","hints","food_choices")
for o in out:
    j = jobs[o['id']]
    for lang in j['translate_to']:
        d = o['translations'][lang]
        for k in KEYS:
            if k not in d: print(o['id'], lang, 'lacks', k)
        for k in ("ingredients","steps","hints","food_choices"):
            if len(d[k]) != len(j[k]): print(o['id'], lang, k, 'count', len(d[k]), len(j[k]))
        for k in ("ingredients","steps","hints"):
            for a, b in zip(j[k], d[k]):
                if (a[0] is None) != (b[0] is None): print(o['id'], lang, k, 'group null mismatch', a[0])
        for k in ("description","portions","serving_size"):
            if (j[k] is None) != (d[k] is None): print(o['id'], lang, k, 'null mismatch')
        pairs = [(j['title'], d['title'])]
        for k in ("ingredients","steps","hints"):
            pairs += [(a[1], b[1]) for a, b in zip(j[k], d[k])]
        pairs += list(zip(j['food_choices'], d['food_choices']))
        for a, b in pairs:
            m = cc.nums(a) - cc.nums(b)
            if m: print('NUM', o['id'], lang, dict(m), '|', a[:60], '|', (b or '')[:60])
print('checked', [o['id'] for o in out])
