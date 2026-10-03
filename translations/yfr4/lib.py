import json
def L(items):
    out=[]
    for x in items:
        if '§' in x:
            g,t=x.split('§',1); out.append([g,t])
        else: out.append([None,x])
    return out
def R(id,title,desc,portions,serving,ing,steps,hints,fc=()):
    return {"id":id,"translations":{"fr":{"title":title,"description":desc,"portions":portions,"serving_size":serving,
      "ingredients":L(ing),"steps":L(steps),"hints":L(hints),"food_choices":list(fc)}}}
def save(n,recs):
    json.dump(recs,open(f'/mnt/c/WSL/davita/translations/out_yfr4_part{n}.json','w'),ensure_ascii=False)
FV="Portions de fruits et légumes"
