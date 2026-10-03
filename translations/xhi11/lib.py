import json
def conv(lst):
    return [[None,x] if isinstance(x,str) else list(x) for x in lst]
def build(recs, path):
    out=[]
    for (i,t,d,p,s,ing,st,h,fc) in recs:
        out.append({"id":i,"translations":{"hi":{"title":t,"description":d,"portions":p,"serving_size":s,
          "ingredients":conv(ing),"steps":conv(st),"hints":conv(h),"food_choices":fc}}})
    json.dump(out,open(path,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
