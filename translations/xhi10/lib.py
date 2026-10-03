import json,sys
def R(id,title,desc,portions,serving,ing,steps,hints,fc):
    P=lambda l:[[None,s] if isinstance(s,str) else list(s) for s in l]
    return {"id":id,"translations":{"hi":{"title":title,"description":desc,"portions":portions,"serving_size":serving,"ingredients":P(ing),"steps":P(steps),"hints":P(hints),"food_choices":fc}}}
def save(n,recs):
    json.dump(recs,open(f"/mnt/c/WSL/davita/translations/out_xhi10_part{n}.json","w"),ensure_ascii=False)
