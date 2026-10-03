import json, sys, importlib
sys.path.insert(0, '.')
n = sys.argv[1]
m = importlib.import_module(f'p{n}')
jobs = {j['id']: j for j in json.load(open('../jobs_c6.json'))}
out = []
for rid, langs in m.DATA:
    j = jobs[rid]
    assert set(langs) == set(j['translate_to']), rid
    tr = {}
    for lg, d in langs.items():
        tr[lg] = {'title': d['title'], 'description': d['description'], 'portions': d['portions'],
                  'serving_size': d['serving_size'],
                  'ingredients': [[None, s] for s in d['ing']],
                  'steps': [[None, s] for s in d['steps']], 'hints': [], 'food_choices': []}
    out.append({'id': rid, 'translations': tr})
json.dump(out, open(f'../out_c6_part{n}.json', 'w'), ensure_ascii=False, indent=1)
print(len(out))
