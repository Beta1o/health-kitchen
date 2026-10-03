import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent.parent
jobs=json.load(open(H/'jobs_xur5.json'))
n=int(sys.argv[1]); lo=(n-1)*15; hi=min(lo+15,len(jobs))
txt=(Path(__file__).parent/f'part{n}.txt').read_text(encoding='utf-8')
blocks={}
cur=None
for ln in txt.split('\n'):
    if ln.startswith('@'):
        cur=int(ln[1:].strip()); blocks[cur]=[]
    elif cur is not None and ln.strip()!='' :
        blocks[cur].append(ln.strip().replace('\\n','\n'))
out=[]
for j in jobs[lo:hi]:
    L=iter(blocks[j['id']]); need=0
    def nx():
        global need
        need+=1
        return next(L)
    d={}
    for k in('title','description','portions','serving_size'):
        d[k]=None if j[k] is None else nx()
    for k in('ingredients','steps','hints'):
        d[k]=[]
        for g,t in j[k] or []:
            g2=None if g is None else nx()
            d[k].append([g2,nx()])
    d['food_choices']=[nx() for _ in j['food_choices']]
    assert len(blocks[j['id']])==need,(j['id'],len(blocks[j['id']]),need)
    out.append({'id':j['id'],'translations':{'ur':d}})
assert len(out)==hi-lo
json.dump(out,open(H/f'out_xur5_part{n}.json','w'),ensure_ascii=False,indent=1)
print('ok',n,len(out))
