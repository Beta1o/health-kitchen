import json
def r(id,title,desc,portions,serving,ings,steps,hints,fc):
    def L(l):
        return [list(x) if isinstance(x,tuple) else [None,x] for x in l]
    return {"id":id,"translations":{"es":{"title":title,"description":desc,"portions":portions,"serving_size":serving,"ingredients":L(ings),"steps":L(steps),"hints":L(hints),"food_choices":fc}}}
def save(n,items):
    json.dump(items,open(f'/mnt/c/WSL/davita/translations/out_tes1_part{n}.json','w'),ensure_ascii=False,indent=1)
