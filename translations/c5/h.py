import json,sys
def P(x):
    return [i if isinstance(i,list) else [None,i] for i in x]
def L(t,d,p,s,i=(),st=(),h=(),f=()):
    return dict(title=t,description=d,portions=p,serving_size=s,ingredients=P(i),steps=P(st),hints=P(h),food_choices=list(f))
def save(n,recs):
    json.dump([{"id":a,"translations":b} for a,b in recs],open(f"/mnt/c/WSL/davita/translations/out_c5_part{n}.json","w"),ensure_ascii=False,indent=1)
