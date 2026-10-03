import json
def R(id,title,desc,por,serv,ing,steps,hints,fc):
    n=lambda l:[[None,t] for t in l]
    return {"id":id,"translations":{"fr":{"title":title,"description":desc,"portions":por,"serving_size":serv,"ingredients":n(ing),"steps":n(steps),"hints":n(hints),"food_choices":fc}}}
def save(o,k):
    json.dump(o,open(f'/mnt/c/WSL/davita/translations/out_xfr5_part{k}.json','w'),ensure_ascii=False)
