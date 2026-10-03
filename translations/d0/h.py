import json,sys
def P(x):
    return [i if isinstance(i,list) else [None,i] for i in (x or [])]
def L(title,desc,portions,serving,ing,steps,hints=None,fc=None):
    return dict(title=title,description=desc,portions=portions,serving_size=serving,ingredients=P(ing),steps=P(steps),hints=P(hints),food_choices=list(fc or []))
def save(n,items):
    json.dump([{"id":i,"translations":t} for i,t in items],open(f"/mnt/c/WSL/davita/translations/out_d0_part{n}.json","w"),ensure_ascii=False,indent=1)
