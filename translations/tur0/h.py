import json,sys
def G(g,l): return [[g,t] for t in l]
def N(l): return [[None,t] for t in l]
def build(R,out):
    res=[]
    for (i,t,d,p,s,ing,st,h,f) in R:
        res.append({"id":i,"translations":{"ur":{"title":t,"description":d,"portions":p,"serving_size":s,"ingredients":ing,"steps":st,"hints":h,"food_choices":f}}})
    json.dump(res,open(out,"w",encoding="utf-8"),ensure_ascii=False)
