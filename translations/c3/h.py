import json,sys
def T(title,desc,portions,serving,ing,steps,hints=(),fc=()):
    w=lambda L:[[None,x] if isinstance(x,str) else list(x) for x in L]
    return dict(title=title,description=desc,portions=portions,serving_size=serving,ingredients=w(ing),steps=w(steps),hints=w(hints),food_choices=list(fc))
def save(name,items):
    json.dump([{"id":i,"translations":t} for i,t in items],open(f"/mnt/c/WSL/davita/translations/out_c3_{name}.json","w"),ensure_ascii=False,indent=1)
