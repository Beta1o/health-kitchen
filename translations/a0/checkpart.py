import json,sys,re
sys.path.insert(0,'/mnt/c/WSL/davita/translations')
from collections import Counter
FRAC = {"½": " 1/2", "⅓": " 1/3", "⅔": " 2/3", "¼": " 1/4", "¾": " 3/4", "⅛": " 1/8"}
def nums(s):
    s=s or ''
    for k,v in FRAC.items(): s=s.replace(k,v)
    for k,v in {"دقيقتين": "2", "ساعتين": "2", "مرتين": "2", "ملعقتين": "2", "كوبين": "2"}.items(): s=s.replace(k,' '+v+' ')
    return Counter(re.findall(r"\d+(?:\.\d+)?", s))
jobs={j['id']:j for j in json.load(open('jobs_a0.json'))}
p=json.load(open(sys.argv[1]))
for o in p:
    j=jobs[o['id']]
    assert set(o['translations'])==set(j['translate_to']),o['id']
    for l,d in o['translations'].items():
        for k in ('ingredients','steps','hints','food_choices'):
            if len(d[k])!=len(j[k]): print(o['id'],l,k,'count',len(d[k]),len(j[k]))
        for k in ('ingredients','steps','hints'):
            for a,b in zip(j[k],d[k]):
                if (a[0] is None)!=(b[0] is None): print(o['id'],l,k,'group null mismatch',a[0])
        for k in ('description','portions','serving_size'):
            if (j[k] is None)!=(d[k] is None): print(o['id'],l,k,'null')
        pairs=[(j['title'],d['title']),(j['description'],d['description']),(j['portions'],d['portions']),(j['serving_size'],d['serving_size'])]
        for k in ('ingredients','steps','hints'): pairs+=[(a[1],b[1]) for a,b in zip(j[k],d[k])]
        pairs+=list(zip(j['food_choices'],d['food_choices']))
        for a,b in pairs:
            m=nums(a)-nums(b)
            if m: print(o['id'],l,dict(m),'|',a[:60],'|',(b or '')[:60])
print('ids',[o['id'] for o in p])
