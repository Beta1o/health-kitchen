import json,sys
def build(recipes, out):
    res=[]
    for (i,t,d,p,s,ing,st,h,fc) in recipes:
        pr=lambda L:[[None,x] for x in L]
        res.append({"id":i,"translations":{"id":{"title":t,"description":d,"portions":p,"serving_size":s,"ingredients":pr(ing),"steps":pr(st),"hints":pr(h),"food_choices":fc}}})
    json.dump(res,open(out,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
