import json,sys
sys.path.insert(0,'/mnt/c/WSL/davita/translations')
from crosscheck import nums
jobs={j['id']:j for j in json.load(open('jobs_b0.json'))}
part=json.load(open(sys.argv[1]))
for o in part:
    j=jobs[o['id']]
    for l in j['translate_to']:
        d=o['translations'][l]
        for k in ('ingredients','steps','hints','food_choices'):
            if len(d[k])!=len(j[k]): print('COUNT',o['id'],l,k)
        for k in ('ingredients','steps','hints'):
            for a,b in zip(j[k],d[k]):
                if (a[0] is None)!=(b[0] is None): print('GROUPNULL',o['id'],l,k)
        pairs=[(j['title'],d['title'])]+[(a[1],b[1]) for k in ('ingredients','steps','hints') for a,b in zip(j[k],d[k])]+list(zip(j['food_choices'],d['food_choices']))
        for a,b in pairs:
            m=nums(a)-nums(b)
            if m: print('NUM',o['id'],l,dict(m),b[:60])
print('ids',[o['id'] for o in part])
