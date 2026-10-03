import json
def P(x): return [None,x] if isinstance(x,str) else list(x)
def R(id,title,desc,portions,serving,ings,steps,hints=(),fc=()):
    return {"id":id,"translations":{"fr":{"title":title,"description":desc,"portions":portions,"serving_size":serving,
      "ingredients":[P(x) for x in ings],"steps":[P(x) for x in steps],"hints":[P(x) for x in hints],"food_choices":list(fc)}}}
def save(n,recs):
    json.dump(recs,open(f'/mnt/c/WSL/davita/translations/out_xfr2_part{n}.json','w'),ensure_ascii=False,indent=0)
