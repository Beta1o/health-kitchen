import json,sys
def R(i,title,desc,portions,serving,ings,steps,hints,fc):
    p=lambda l:[[None,x] for x in l]
    return {"id":i,"translations":{"id":{"title":title,"description":desc,"portions":portions,"serving_size":serving,"ingredients":p(ings),"steps":p(steps),"hints":p(hints),"food_choices":fc}}}
def save(n,lst):
    json.dump(lst,open(f"/mnt/c/WSL/davita/translations/out_xid6_part{n}.json","w"),ensure_ascii=False,indent=1)
