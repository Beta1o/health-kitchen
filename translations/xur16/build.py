import json,sys,importlib.util
n=int(sys.argv[1]); a=int(sys.argv[2]); b=int(sys.argv[3])
jobs=json.load(open('jobs_xur16.json'))[a:b]
spec=importlib.util.spec_from_file_location('p',f'xur16/p{n}.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
R=m.R
assert len(R)==len(jobs),(len(R),len(jobs))
out=[]
for j,r in zip(jobs,R):
    t,d,p,s,I,S,H=r
    for k,x in(('I',I),('S',S),('H',H)):
        e=len(j[{'I':'ingredients','S':'steps','H':'hints'}[k]] or [])
        assert len(x)==e,(j['id'],k,len(x),e)
    out.append({"id":j["id"],"translations":{"ur":{"title":t,"description":d,"portions":p,"serving_size":s,
      "ingredients":[[None,x] for x in I],"steps":[[None,x] for x in S],"hints":[[None,x] for x in H],"food_choices":[]}}})
json.dump(out,open(f'out_xur16_part{n}.json','w'),ensure_ascii=False,indent=1)
print('ok',len(out))
