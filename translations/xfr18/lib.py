import json,sys
def P(x):
    return [p if isinstance(p,list) else [None,p] for p in x]
def R(id,title,description,portions,serving_size,ingredients,steps,hints=(),food_choices=()):
    return {"id":id,"translations":{"fr":{"title":title,"description":description,"portions":portions,"serving_size":serving_size,"ingredients":P(ingredients),"steps":P(steps),"hints":P(hints),"food_choices":list(food_choices)}}}
def save(n,items):
    json.dump(items,open(f"/mnt/c/WSL/davita/translations/out_xfr18_part{n}.json","w"),ensure_ascii=False)
