import json,sys,importlib.util
n=sys.argv[1]; a=int(sys.argv[2])
spec=importlib.util.spec_from_file_location('p',f'xhi25/p{n}.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
jobs=json.load(open('jobs_xhi25.json'))
out=[]
for k,(t,d,p,s,ing,st) in enumerate(m.R):
    j=jobs[a+k]
    assert len(ing)==len(j['ingredients']) and len(st)==len(j['steps']),(a+k,len(ing),len(j['ingredients']),len(st),len(j['steps']))
    out.append({"id":j['id'],"translations":{"hi":{"title":t,"description":d,"portions":p,"serving_size":s,
     "ingredients":[[None,x] for x in ing],"steps":[[None,x] for x in st],"hints":[],"food_choices":[]}}})
assert len(m.R)==int(sys.argv[3])-a,len(m.R)
json.dump(out,open(f'out_xhi25_part{n}.json','w'),ensure_ascii=False,indent=1)
print('ok',len(out))
