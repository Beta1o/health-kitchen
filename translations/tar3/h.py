import json,sys
J={x['id']:x for x in json.load(open('/mnt/c/WSL/davita/translations/jobs_tar3.json'))}
OUT=[]
def R(id,title,desc,portions,serving,ing,steps,hints,g=None):
    g=g or {}
    s=J[id]
    def mk(k,t):
        src=s[k]
        assert len(src)==len(t),(id,k,len(src),len(t))
        r=[]
        for (lab,_),x in zip(src,t):
            if lab is not None: assert lab in g,(id,lab)
            r.append([None if lab is None else g[lab],x])
        return r
    assert (s['description'] is None)==(desc is None),id
    OUT.append({"id":id,"translations":{"ar":{"title":title,"description":desc,"portions":portions,"serving_size":serving,"ingredients":mk('ingredients',ing),"steps":mk('steps',steps),"hints":mk('hints',hints),"food_choices":[]}}})
def save(path):
    json.dump(OUT,open(path,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
