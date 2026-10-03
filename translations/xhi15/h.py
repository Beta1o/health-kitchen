import json,sys
J=json.load(open('/mnt/c/WSL/davita/translations/jobs_xhi15.json'))
def pairs(src,items):
    assert len(src)==len(items),(len(src),len(items),src)
    out=[]
    for s,i in zip(src,items):
        if isinstance(i,str): assert s[0] is None; out.append([None,i])
        else: out.append([i[0],i[1]])
    return out
def build(start,recs,part):
    res=[]
    for k,r in enumerate(recs):
        j=J[start+k]; t,d,p,s,ing,st,h,fc=r
        assert len(j['food_choices'])==len(fc),(j['id'])
        assert (j['description'] is None)==(d is None),j['id']
        res.append({"id":j['id'],"translations":{"hi":{"title":t,"description":d,"portions":p,"serving_size":s,
          "ingredients":pairs(j['ingredients'],ing),"steps":pairs(j['steps'],st),"hints":pairs(j['hints'],h),"food_choices":fc}}})
    json.dump(res,open(f'/mnt/c/WSL/davita/translations/out_xhi15_part{part}.json','w'),ensure_ascii=False,indent=1)
