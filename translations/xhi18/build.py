import json,sys,re
n,start=sys.argv[1],int(sys.argv[2])
src=json.load(open('jobs_xhi18.json'))
txt=open(f'xhi18/p{n}.txt',encoding='utf-8').read()
blocks=[b for b in re.split(r'^=== *',txt,flags=re.M) if b.strip()]
out=[]
for i,b in enumerate(blocks):
    lines=b.strip('\n').split('\n')
    j=src[start+i]; assert int(lines[0].strip())==j['id'],(lines[0],j['id'])
    r={'title':None,'description':None,'portions':None,'serving_size':None,'ingredients':[],'steps':[],'hints':[],'food_choices':[]}
    for l in lines[1:]:
        k,_,v=l.partition(' ')
        if k not in ('T','D','P','S','I','ST','H','F'):
            r['description']+='\n'+l; continue
        if k=='T':r['title']=v
        elif k=='D':r['description']=v
        elif k=='P':r['portions']=v
        elif k=='S':r['serving_size']=v
        elif k=='F':r['food_choices'].append(v)
        else:
            f={'I':'ingredients','ST':'steps','H':'hints'}[k]
            m=re.match(r'\[(.*?)\] (.*)',v)
            r[f].append([m.group(1),m.group(2)] if m else [None,v])
    for f in ('ingredients','steps','hints','food_choices'):
        assert len(r[f])==len(j[f]),(j['id'],f,len(r[f]),len(j[f]))
        if f!='food_choices':
            for a,bb in zip(r[f],j[f]): assert (a[0] is None)==(bb[0] is None),(j['id'],f)
    for f in ('description','portions','serving_size'):
        if j[f] is None: r[f]=None
    out.append({'id':j['id'],'translations':{'hi':r}})
json.dump(out,open(f'out_xhi18_part{n}.json','w'),ensure_ascii=False,indent=1)
print(len(out),'built')
