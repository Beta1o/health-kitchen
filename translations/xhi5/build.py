import json,sys,importlib.util
n=sys.argv[1]
B='/mnt/c/WSL/davita/translations/'
s=importlib.util.spec_from_file_location('p',B+'xhi5/p%s.py'%n);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
jobs={x['id']:x for x in json.load(open(B+'jobs_xhi5.json'))}
out=[]
def pairs(v,orig):
    r=[]
    for a,(g,_) in zip(v,orig):
        r.append([g,a] if not isinstance(a,tuple) else [a[0],a[1]])
    return r
for r in m.R:
    id_,t,dsc,p,sv,ing,st,h,f=r
    j=jobs[id_]
    for k,v in(('ingredients',ing),('steps',st),('hints',h),('food_choices',f)):
        assert len(v)==len(j[k] or []),(id_,k,len(v),len(j[k] or []))
    out.append({"id":id_,"translations":{"hi":{"title":t,"description":dsc,"portions":p,"serving_size":sv,
     "ingredients":pairs(ing,j['ingredients']),"steps":pairs(st,j['steps']),"hints":pairs(h,j['hints'] or []),"food_choices":f}}})
json.dump(out,open(B+'out_xhi5_part%s.json'%n,'w'),ensure_ascii=False,indent=1)
print(len(out))
