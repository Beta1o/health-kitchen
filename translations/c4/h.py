import json,sys
def P(x):
    return [[None,s] if isinstance(s,str) else list(s) for s in (x or [])]
def T(title,desc,portions,serving,ing,steps,hints=None,fc=None):
    return dict(title=title,description=desc,portions=portions,serving_size=serving,ingredients=P(ing),steps=P(steps),hints=P(hints),food_choices=list(fc or []))
def save(n,items):
    json.dump([{"id":i,"translations":t} for i,t in items],open(f'/mnt/c/WSL/davita/translations/out_c4_part{n}.json','w'),ensure_ascii=False,indent=1)
