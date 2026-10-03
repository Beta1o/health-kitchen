import json,sys
J=json.load(open('/mnt/c/WSL/davita/translations/jobs_c0.json'))
def pairs(src,items):
    assert len(src)==len(items),(len(src),len(items),items[:2])
    out=[]
    for (g,_),t in zip(src,items):
        if isinstance(t,(list,tuple)): out.append([t[0],t[1]])
        else:
            assert g is None,("group needs label",g)
            out.append([None,t])
    return out
def build(idx,tr):
    """tr: {lang:(title,desc,portions,serving,ings,steps,hints,fcs)}"""
    j=J[idx]; res={"id":j["id"],"translations":{}}
    assert set(tr)==set(j["translate_to"]),(idx,set(tr))
    for l,(t,d,p,s,i,st,h,f) in tr.items():
        assert len(f)==len(j["food_choices"])
        res["translations"][l]={"title":t,"description":d if j["description"] is not None else None,
          "portions":p,"serving_size":s,"ingredients":pairs(j["ingredients"],i),
          "steps":pairs(j["steps"],st),"hints":pairs(j["hints"],h),"food_choices":f}
    return res
def save(n,res):
    json.dump(res,open(f'/mnt/c/WSL/davita/translations/out_c0_part{n}.json','w'),ensure_ascii=False,indent=1)
