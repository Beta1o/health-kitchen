import json,sys
def T(title,desc,portions,serving,ing,steps,hints=(),fc=()):
    p=lambda L:[[None,x] for x in L]
    return {"title":title,"description":desc,"portions":portions,"serving_size":serving,
            "ingredients":p(ing),"steps":p(steps),"hints":p(hints),"food_choices":list(fc)}
def save(n,items):
    json.dump(items,open(f"/mnt/c/WSL/davita/translations/out_c23_part{n}.json","w"),ensure_ascii=False,indent=1)
