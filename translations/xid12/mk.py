import json
J={r['id']:r for r in json.load(open('../jobs_xid12.json'))}
LBL={}
def build(recipes,out):
    res=[]
    for (i,t,d,p,s,ing,st,h,fc) in recipes:
        r=J[i]
        def pr(src,L):
            assert len(src)==len(L),(i,len(src),len(L),L[:1])
            o=[]
            for (g,_),x in zip(src,L):
                if g is not None: assert g in LBL,(i,g)
                o.append([LBL[g] if g is not None else None,x])
            return o
        assert len(r['food_choices'])==len(fc),(i,'fc')
        assert (r['description'] is None)==(d is None),(i,'desc')
        res.append({"id":i,"translations":{"id":{"title":t,"description":d,"portions":p,"serving_size":s,"ingredients":pr(r['ingredients'],ing),"steps":pr(r['steps'],st),"hints":pr(r['hints'],h),"food_choices":fc}}})
    json.dump(res,open(out,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
