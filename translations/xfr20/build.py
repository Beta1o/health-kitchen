import json,sys,importlib.util
n=sys.argv[1]
spec=importlib.util.spec_from_file_location('d',f'/mnt/c/WSL/davita/translations/xfr20/data{n}.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
jobs=json.load(open('/mnt/c/WSL/davita/translations/jobs_xfr20.json'))
start=(int(n)-1)*10
out=[]
for k,r in enumerate(m.R):
    j=jobs[start+k]; assert j['id']==r[0],(j['id'],r[0])
    assert len(r[5])==len(j['ingredients']) and len(r[6])==len(j['steps']),(r[0],len(r[5]),len(j['ingredients']),len(r[6]),len(j['steps']))
    assert (r[2] is None)==(j['description'] is None)
    out.append({"id":r[0],"translations":{"fr":{"title":r[1],"description":r[2],"portions":r[3],"serving_size":r[4],
      "ingredients":[[None,x] for x in r[5]],"steps":[[None,x] for x in r[6]],"hints":[],"food_choices":[]}}})
json.dump(out,open(f'/mnt/c/WSL/davita/translations/out_xfr20_part{n}.json','w'),ensure_ascii=False,indent=1)
print(len(out))
