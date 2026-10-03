import json,sys,importlib.util
n=sys.argv[1]
s=importlib.util.spec_from_file_location('p','/mnt/c/WSL/davita/translations/xid10/p%s.py'%n);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def pairs(l):
    return [list(x) if isinstance(x,tuple) else [None,x] for x in l]
out=[]
for id_,t,d,p,sv,ing,st,h,fc in m.R:
    out.append({"id":id_,"translations":{"id":{"title":t,"description":d,"portions":p,"serving_size":sv,"ingredients":pairs(ing),"steps":pairs(st),"hints":pairs(h),"food_choices":fc}}})
json.dump(out,open('/mnt/c/WSL/davita/translations/out_xid10_part%s.json'%n,'w'),ensure_ascii=False,indent=0)
print(len(out))
