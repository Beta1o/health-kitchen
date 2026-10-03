import json,sys
sys.path.insert(0,'/mnt/c/WSL/davita/translations/hi4')
from lib import *
n=int(sys.argv[1])
T=json.load(open(f'/mnt/c/WSL/davita/translations/hi4/tr{n}.json'))
out=[]
for j in part(n):
    t=T[str(j['id'])]; f=flat(j)
    assert len(t)==len(f),(j['id'],len(t),len(f))
    it=iter(t); d={}
    for k in ('title','description','portions','serving_size'):
        d[k]=next(it) if j[k] is not None else None
    for k in ('ingredients','steps','hints'):
        L=[]
        for g,_ in j[k]:
            gg=next(it) if g is not None else None
            L.append([gg,next(it)])
        d[k]=L
    d['food_choices']=[next(it) for _ in j['food_choices']]
    out.append({"id":j['id'],"translations":{"hi":d}})
json.dump(out,open(f'/mnt/c/WSL/davita/translations/out_hi4_part{n+1}.json','w'),ensure_ascii=False,indent=1)
print(len(out))
