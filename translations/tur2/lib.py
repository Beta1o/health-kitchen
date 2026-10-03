import json
def _p(x): return list(x) if isinstance(x,(tuple,list)) else [None,x]
def R(id,title,desc,portions,serving,ing,steps,hints,fc):
    return {"id":id,"translations":{"ur":{"title":title,"description":desc,"portions":portions,"serving_size":serving,
      "ingredients":[_p(x) for x in ing],"steps":[_p(x) for x in steps],"hints":[_p(x) for x in hints],"food_choices":list(fc)}}}
def save(n,recs):
    json.dump(recs,open(f"/mnt/c/WSL/davita/translations/out_tur2_part{n}.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
    print(n,len(recs))
