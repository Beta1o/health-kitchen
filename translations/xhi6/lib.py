import json,sys
def P(x):
    return x if isinstance(x,list) else [None,x]
def T(id,title,desc,portions,serving,ing,steps,hints,fc):
    return {"id":id,"translations":{"hi":{"title":title,"description":desc,"portions":portions,"serving_size":serving,
      "ingredients":[P(i) for i in ing],"steps":[P(i) for i in steps],"hints":[P(i) for i in hints],"food_choices":fc}}}
def save(n,items):
    json.dump(items,open(f'/mnt/c/WSL/davita/translations/out_xhi6_part{n}.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
