import json,sys
def n(l): return [[None,t] for t in l]
def g(label,l): return [[label,t] for t in l]
def build(items,part):
    jobs={j['id']:j for j in json.load(open('../jobs_ses0.json'))}
    out=[]
    for (id,title,desc,por,serv,ing,st,hi,*fc) in items:
        j=jobs[id]
        f=fc[0] if fc else []
        assert len(f)==len(j['food_choices']),id
        assert len(ing)==len(j['ingredients']) and len(st)==len(j['steps']) and len(hi)==len(j['hints']),(id,len(ing),len(j['ingredients']),len(st),len(j['steps']),len(hi),len(j['hints']))
        out.append({"id":id,"translations":{"es":{"title":title,"description":desc,"portions":por,"serving_size":serv,"ingredients":ing,"steps":st,"hints":hi,"food_choices":f}}})
    json.dump(out,open(f'part_{part}.json','w'),ensure_ascii=False,indent=1)
    print(part,len(out))
