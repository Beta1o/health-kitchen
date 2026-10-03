import json,glob,sys
d=json.load(open('../jobs_xhi13.json'))
uniq=json.load(open('uniq.json'))
tr={}
for f in sorted(glob.glob('tr_*.txt')):
    for line in open(f,encoding='utf-8'):
        line=line.rstrip('\n')
        if not line.strip(): continue
        n,t=line.split('\t',1)
        tr[uniq[int(n)]]=t.replace('\\n','\n')
miss=[s for s in uniq if s not in tr]
print('missing',len(miss),miss[:5])
if miss: sys.exit(1)
T=lambda s: None if s is None else tr[s]
out=[]
for r in d:
    h={'title':T(r['title']),'description':T(r['description']),'portions':T(r['portions']),'serving_size':T(r['serving_size'])}
    for k in ['ingredients','steps','hints']:
        h[k]=[[T(g),T(t)] for g,t in r[k]]
    h['food_choices']=[T(f) for f in r['food_choices']]
    out.append({'id':r['id'],'translations':{'hi':h}})
parts=[out[i:i+15] for i in range(0,len(out),15)]
for i,p in enumerate(parts,1):
    json.dump(p,open(f'../out_xhi13_part{i}.json','w'),ensure_ascii=False,indent=1)
merged=[]
for i in range(1,len(parts)+1):
    merged+=json.load(open(f'../out_xhi13_part{i}.json'))
json.dump(merged,open('../out_xhi13.json','w'),ensure_ascii=False,indent=1)
import os
for i in range(1,len(parts)+1): os.remove(f'../out_xhi13_part{i}.json')
print(len(merged))
