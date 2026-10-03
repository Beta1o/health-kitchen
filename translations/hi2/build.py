import json,sys,re
# usage: build.py N  -> reads hi2/pN.txt, writes out_hi2_partN.json
jobs=json.load(open('/mnt/c/WSL/davita/translations/jobs_hi2.json'))
by={j['id']:j for j in jobs}
n=sys.argv[1]
txt=open(f'/mnt/c/WSL/davita/translations/hi2/p{n}.txt',encoding='utf-8').read()
out=[]
for blk in txt.split('\n# ')[0:]:
    blk=blk.strip()
    if not blk: continue
    blk=blk.lstrip('# ')
    lines=blk.split('\n')
    rid=int(lines[0].strip()); j=by[rid]
    r={'title':None,'description':None,'portions':None,'serving_size':None,'ingredients':[],'steps':[],'hints':[],'food_choices':[]}
    for l in lines[1:]:
        if not l.strip(): continue
        m=re.match(r'^([TDPSIXHF])(?:\[(.*?)\])?: ?(.*)$',l)
        assert m,(rid,l)
        c,g,t=m.groups()
        if c=='T':r['title']=t
        elif c=='D':r['description']=None if t=='None' else t
        elif c=='P':r['portions']=None if t=='None' else t
        elif c=='S':r['serving_size']=None if t=='None' else t
        elif c=='I':r['ingredients'].append([g,t])
        elif c=='X':r['steps'].append([g,t])
        elif c=='H':r['hints'].append([g,t])
        elif c=='F':r['food_choices']=[x.strip() for x in t.split(' | ')] if t else []
    out.append({'id':rid,'translations':{'hi':r}})
json.dump(out,open(f'/mnt/c/WSL/davita/translations/out_hi2_part{n}.json','w'),ensure_ascii=False)
print(len(out),'recipes')
