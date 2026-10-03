import json,sys
# usage: build.py N  (imports xhi2/pN.py defining R list of tuples)
import importlib.util
n=sys.argv[1]
s=importlib.util.spec_from_file_location('p','/mnt/c/WSL/davita/translations/xhi2/p%s.py'%n);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
jobs={x['id']:x for x in json.load(open('/mnt/c/WSL/davita/translations/jobs_xhi2.json'))}
out=[]
for r in m.R:
    id_,t,dsc,p,sv,ing,st,h,f=r
    j=jobs[id_]
    for k,v in(('ingredients',ing),('steps',st),('hints',h),('food_choices',f)):
        assert len(v)==len(j[k]),(id_,k,len(v),len(j[k]))
    out.append({"id":id_,"translations":{"hi":{"title":t,"description":dsc,"portions":p,"serving_size":sv,
     "ingredients":[[None,x] for x in ing],"steps":[[None,x] for x in st],"hints":[[None,x] for x in h],"food_choices":f}}})
json.dump(out,open('/mnt/c/WSL/davita/translations/out_xhi2_part%s.json'%n,'w'),ensure_ascii=False,indent=1)
print(len(out))
