import json,sys
J=json.load(open('/mnt/c/WSL/davita/translations/jobs_xfr21.json'))
def build(start,end,recs):
    out=[]
    assert len(recs)==end-start,(len(recs),end-start)
    for j,r in zip(J[start:end],recs):
        t,d,p,s,ing,st,h,fc=r
        def pair(src,tr):
            assert len(src)==len(tr),(j['id'],len(src),len(tr))
            res=[]
            for (g,_),x in zip(src,tr):
                if isinstance(x,list): res.append(x)
                else:
                    assert g is None,(j['id'],'group needs label')
                    res.append([None,x])
            return res
        assert len(fc)==len(j['food_choices']),(j['id'],'fc')
        out.append({"id":j['id'],"translations":{"fr":{"title":t,"description":d,"portions":p,"serving_size":s,"ingredients":pair(j['ingredients'],ing),"steps":pair(j['steps'],st),"hints":pair(j['hints'],h),"food_choices":fc}}})
    return out
def save(n,start,end,recs):
    json.dump(build(start,end,recs),open(f'/mnt/c/WSL/davita/translations/out_xfr21_part{n}.json','w'),ensure_ascii=False)
