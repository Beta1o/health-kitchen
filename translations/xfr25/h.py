import json,sys
def P(x): return x if isinstance(x,list) else [None,x]
def R(id,title,desc,portions,serving,ings,steps,hints=(),fc=()):
    return {"id":id,"translations":{"fr":{"title":title,"description":desc,"portions":portions,"serving_size":serving,
     "ingredients":[P(i) for i in ings],"steps":[P(i) for i in steps],"hints":[P(i) for i in hints],"food_choices":list(fc)}}}
def save(n,items):
    json.dump(items,open(f"/mnt/c/WSL/davita/translations/out_xfr25_part{n}.json","w"),ensure_ascii=False,indent=1)
