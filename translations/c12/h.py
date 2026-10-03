import json
def N(l): return [[None,x] for x in l]
def R(id,**kw):
    t={}
    for k,v in kw.items():
        ti,de,po,se,ing,st,hi,fc=v
        t[k]={"title":ti,"description":de,"portions":po,"serving_size":se,"ingredients":N(ing),"steps":N(st),"hints":N(hi),"food_choices":fc}
    return {"id":id,"translations":t}
def dump(items,path):
    json.dump(items,open(path,"w",encoding="utf-8"),ensure_ascii=False,indent=1)
