import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent.parent
jobs={j['id']:j for j in json.load(open(H/'jobs_a2.json'))}
order=[j['id'] for j in json.load(open(H/'jobs_a2.json'))]
for p in sys.argv[1:]:
    part=json.load(open(H/p))
    print(p,len(part),'ids',[order.index(o['id']) for o in part])
    for o in part:
        j=jobs[o['id']]
        for l in j['translate_to']:
            d=o['translations'][l]
            for k in ('ingredients','steps','hints','food_choices'):
                if len(d[k])!=len(j[k]): print('COUNT',o['id'],l,k,len(d[k]),len(j[k]))
            for k in ('ingredients','steps','hints'):
                for a,b in zip(j[k],d[k]):
                    if (a[0] is None)!=(b[0] is None): print('GROUP',o['id'],l,k)
            for k in ('description','portions','serving_size'):
                if (j[k] is None)!=(d[k] is None): print('NULL',o['id'],l,k)
