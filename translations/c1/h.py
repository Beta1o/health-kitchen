import json
N=None
def P(l): return [[N,t] for t in l]
out=[]
def add(i,**tr): out.append({"id":i,"translations":tr})
def T(title,description,portions,serving_size,ing,steps,hints=(),fc=()):
    return dict(title=title,description=description,portions=portions,serving_size=serving_size,ingredients=P(ing),steps=P(steps),hints=P(hints),food_choices=list(fc))
def save(n):
    json.dump(out,open(f'/mnt/c/WSL/davita/translations/out_c1_part{n}.json','w'),ensure_ascii=False,indent=1)
    print(len(out))
