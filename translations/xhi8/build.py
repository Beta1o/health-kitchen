import json,sys
d=json.load(open('../jobs_xhi8.json'))
n=int(sys.argv[1]);jobs=d[(n-1)*15:n*15]
txt=open(f'part{n}.txt',encoding='utf-8').read()
blocks=[b for b in txt.split('### ')[1:]]
assert len(blocks)==len(jobs),(len(blocks),len(jobs))
out=[]
for b,j in zip(blocks,jobs):
    lines=b.strip('\n').split('\n')
    assert int(lines[0].strip())==j['id'],(lines[0],j['id'])
    t={'T':None,'D':None,'P':None,'S':None,'I':[],'W':[],'H':[],'F':[]}
    for l in lines[1:]:
        if not l.strip(): continue
        c,v=l.split(': ',1) if ': ' in l else (l.rstrip(':'),'')
        if c in('T','D','P','S'): t[c]=v
        else: t[c].append(v)
    for c,k in(('I','ingredients'),('W','steps'),('H','hints'),('F','food_choices')):
        assert len(t[c])==len(j[k] or []),(j['id'],k,len(t[c]),len(j[k] or []))
    out.append({'id':j['id'],'translations':{'hi':{'title':t['T'],'description':t['D'] if j['description'] is not None else None,'portions':t['P'] if j['portions'] is not None else None,'serving_size':t['S'] if j['serving_size'] is not None else None,
      'ingredients':[[None,x] for x in t['I']],'steps':[[None,x] for x in t['W']],'hints':[[None,x] for x in t['H']],'food_choices':t['F']}}})
json.dump(out,open(f'../out_xhi8_part{n}.json','w'),ensure_ascii=False)
print('ok',n,len(out))
