import json,sys
J={j['id']:j for j in json.load(open('/mnt/c/WSL/davita/translations/jobs_c7.json'))}
def wrap(src,items):
    assert len(src)==len(items),(len(src),len(items),items[:2])
    out=[]
    for s,t in zip(src,items):
        if isinstance(t,(tuple,list)): out.append([t[0],t[1]])
        else: out.append([s[0],t])
    return out
def L(title,desc,portions,serving,ings,steps,hints,fc):
    return dict(title=title,description=desc,portions=portions,serving_size=serving,ingredients=ings,steps=steps,hints=hints,food_choices=fc)
def build(rid,**langs):
    j=J[rid]
    assert set(langs)==set(j['translate_to']),(rid,langs.keys())
    tr={}
    for k,v in langs.items():
        v=dict(v)
        for f in('ingredients','steps','hints'): v[f]=wrap(j[f],v[f])
        assert len(v['food_choices'])==len(j['food_choices'])
        tr[k]=v
    return {"id":rid,"translations":tr}
def save(name,recs):
    json.dump(recs,open(f'/mnt/c/WSL/davita/translations/{name}','w'),ensure_ascii=False,indent=1)
