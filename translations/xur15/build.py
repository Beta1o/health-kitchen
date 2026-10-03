import json,sys,importlib.util
n=int(sys.argv[1]); lo=int(sys.argv[2]); hi=int(sys.argv[3])
H='/mnt/c/WSL/davita/translations/'
jobs=json.load(open(H+'jobs_xur15.json'))[lo:hi]
spec=importlib.util.spec_from_file_location('p',H+f'xur15/p{n}.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
assert len(m.R)==len(jobs),(len(m.R),len(jobs))
out=[]
for j,(t,d,po,sv,ing,st) in zip(jobs,m.R):
    assert len(ing)==len(j['ingredients']) and len(st)==len(j['steps']),(j['id'],len(ing),len(j['ingredients']),len(st),len(j['steps']))
    assert (d is None)==(j['description'] is None)
    out.append({"id":j['id'],"translations":{"ur":{"title":t,"description":d,"portions":po,"serving_size":sv,
     "ingredients":[[None,x] for x in ing],"steps":[[None,x] for x in st],"hints":[],"food_choices":[]}}})
json.dump(out,open(H+f'out_xur15_part{n}.json','w'),ensure_ascii=False,indent=1)
print('ok',len(out))
