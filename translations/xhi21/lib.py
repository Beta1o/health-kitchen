import json,sys
def R(id,title,desc,portions,serving,ing,steps,hints=(),fc=()):
    w=lambda L:[x if isinstance(x,list) else [None,x] for x in L]
    return {"id":id,"translations":{"hi":{"title":title,"description":desc,"portions":portions,"serving_size":serving,"ingredients":w(ing),"steps":w(steps),"hints":w(hints),"food_choices":list(fc)}}}
def save(n,items):
    json.dump(items,open(f'/mnt/c/WSL/davita/translations/out_xhi21_part{n}.json','w'),ensure_ascii=False)
