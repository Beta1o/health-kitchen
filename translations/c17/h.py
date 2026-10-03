import json,sys
def pairs(l):
    return [list(x) if isinstance(x,(tuple,list)) else [None,x] for x in l]
def L(title,desc,portions,serving,ing,steps,hints=(),fc=()):
    return {"title":title,"description":desc,"portions":portions,"serving_size":serving,
            "ingredients":pairs(ing),"steps":pairs(steps),"hints":pairs(hints),"food_choices":list(fc)}
def save(name,recs):
    json.dump([{"id":i,"translations":t} for i,t in recs],open(f"/mnt/c/WSL/davita/translations/{name}","w"),ensure_ascii=False,indent=1)
