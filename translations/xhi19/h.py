import json,sys
def L(x): return [i if isinstance(i,list) else [None,i] for i in x]
def R(id,t,d,p,s,ing,st,h=(),fc=()):
    return {"id":id,"translations":{"hi":{"title":t,"description":d,"portions":p,"serving_size":s,"ingredients":L(ing),"steps":L(st),"hints":L(h),"food_choices":list(fc)}}}
def save(n,items):
    json.dump(items,open(f'/mnt/c/WSL/davita/translations/out_xhi19_part{n}.json','w'),ensure_ascii=False,indent=1)
