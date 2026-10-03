import json
def build(recipes,out):
    res=[]
    def pr(L):
        r=[]
        for x in L:
            if isinstance(x,(list,tuple)): r.append([x[0],x[1]])
            else: r.append([None,x])
        return r
    for (i,t,d,p,s,ing,st,h,fc) in recipes:
        res.append({"id":i,"translations":{"id":{"title":t,"description":d,"portions":p,"serving_size":s,"ingredients":pr(ing),"steps":pr(st),"hints":pr(h),"food_choices":fc}}})
    json.dump(res,open(out,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
def G(label,L): return [(label,x) for x in L]
