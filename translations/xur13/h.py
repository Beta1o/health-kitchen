import json,sys
N=None
out=[]
def P(l):
    return [x if isinstance(x,list) else [N,x] for x in l]
def add(i,title,description,portions,serving_size,ing,steps,hints=(),fc=()):
    out.append({"id":i,"translations":{"ur":dict(title=title,description=description,portions=portions,serving_size=serving_size,ingredients=P(ing),steps=P(steps),hints=P(hints),food_choices=list(fc))}})
def save(n):
    json.dump(out,open(f'/mnt/c/WSL/davita/translations/out_xur13_part{n}.json','w'),ensure_ascii=False,indent=1)
    print(len(out))
