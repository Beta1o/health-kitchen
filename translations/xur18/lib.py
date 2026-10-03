import json,sys
def R(id,title,desc,portions,serving,ings,steps):
    return {"id":id,"translations":{"ur":{"title":title,"description":desc,"portions":portions,"serving_size":serving,
     "ingredients":[[None,t] for t in ings],"steps":[[None,t] for t in steps],"hints":[],"food_choices":[]}}}
def dump(n,recs):
    json.dump(recs,open(f"/mnt/c/WSL/davita/translations/out_xur18_part{n}.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
