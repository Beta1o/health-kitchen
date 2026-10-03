import json,sys
def _l(x):
    return [i if isinstance(i,list) else [None,i] for i in x]
def R(id,t,d,p,s,ing,st,h,fc):
    return {"id":id,"translations":{"id":{"title":t,"description":d,"portions":p,"serving_size":s,"ingredients":_l(ing),"steps":_l(st),"hints":_l(h),"food_choices":fc}}}
def save(n,items):
    json.dump(items,open(f'/mnt/c/WSL/davita/translations/out_xid9_part{n}.json','w'),ensure_ascii=False,indent=0)
    print(len(items))
