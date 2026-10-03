import json,sys,importlib
n=int(sys.argv[1]); size=15
jobs=json.load(open('../jobs_xur3.json'))
m=importlib.import_module(f'p{n}')
start=(n-1)*size
out=[]
assert len(m.D)==len(jobs[start:start+size]),(len(m.D),len(jobs[start:start+size]))
for j,t in zip(jobs[start:start+size],m.D):
    ti,de,po,se,ing,st,hi,fc=t
    for k,a in(('ing',ing),('st',st),('hi',hi),('fc',fc)):
        pass
    assert len(ing)==len(j['ingredients']),(j['id'],'ing')
    assert len(st)==len(j['steps']),(j['id'],'steps')
    assert len(hi)==len(j['hints']),(j['id'],'hints')
    assert len(fc)==len(j['food_choices']),(j['id'],'fc')
    out.append({'id':j['id'],'translations':{'ur':{'title':ti,'description':de,'portions':po,'serving_size':se,
      'ingredients':[[None,x] for x in ing],'steps':[[None,x] for x in st],'hints':[[None,x] for x in hi],'food_choices':fc}}})
json.dump(out,open(f'../out_xur3_part{n}.json','w'),ensure_ascii=False,indent=1)
print('ok',len(out))
