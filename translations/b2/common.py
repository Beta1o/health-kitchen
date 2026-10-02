import json
JOBS = {r['id']: r for r in json.load(open('/mnt/c/WSL/davita/translations/jobs_b2.json', encoding='utf-8'))}
OUT = []
def _pairs(src, texts, groups):
    assert len(src) == len(texts), (len(src), len(texts), texts[:1])
    return [[None if g is None else groups[g], t] for (g, _), t in zip(src, texts)]
def R(rid, es, ar, es_groups=None, ar_groups=None):
    j = JOBS[rid]
    tr = {}
    for lang, d, grp in (('es', es, es_groups or {}), ('ar', ar, ar_groups or {})):
        o = {'title': d['title'], 'description': d.get('description'),
             'portions': d.get('portions'), 'serving_size': d.get('serving_size')}
        for k in ('ingredients', 'steps', 'hints'):
            o[k] = _pairs(j[k], d.get(k, []), grp)
        o['food_choices'] = d.get('food_choices', [])
        assert len(o['food_choices']) == len(j['food_choices']), rid
        for k in ('description', 'portions', 'serving_size'):
            assert (o[k] is None) == (j[k] is None), (rid, lang, k)
        tr[lang] = o
    OUT.append({'id': rid, 'translations': tr})
def save(n):
    p = f'/mnt/c/WSL/davita/translations/out_b2_part{n}.json'
    json.dump(OUT, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('wrote', p, len(OUT))
