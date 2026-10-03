import json,sys,importlib
sys.path.insert(0,'/mnt/c/WSL/davita/translations/xhi16')
jobs=json.load(open('/mnt/c/WSL/davita/translations/jobs_xhi16.json'))
n=int(sys.argv[1]); mod=importlib.import_module(f'p{n}')
out=[]
for j in jobs:
    if j['id'] not in mod.R: continue
    t,d,p,s,i,st=mod.R[j['id']]
    assert len(i)==len(j['ingredients']) and len(st)==len(j['steps']),j['id']
    out.append({"id":j['id'],"translations":{"hi":{"title":t,"description":d,"portions":p,"serving_size":s,
      "ingredients":[[None,x] for x in i],"steps":[[None,x] for x in st],"hints":[],"food_choices":[]}}})
json.dump(out,open(f'/mnt/c/WSL/davita/translations/out_xhi16_part{n}.json','w'),ensure_ascii=False,indent=1)
print(n,len(out))
