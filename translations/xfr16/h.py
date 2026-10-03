import json,sys
def P(n,recs):
    out=[]
    for r in recs:
        id,t,d,po,se,ing,st,hi,fc=r
        f=lambda L:[x if isinstance(x,list) else [None,x] for x in L]
        out.append({"id":id,"translations":{"fr":{"title":t,"description":d,"portions":po,"serving_size":se,"ingredients":f(ing),"steps":f(st),"hints":f(hi),"food_choices":fc}}})
    json.dump(out,open(f"/mnt/c/WSL/davita/translations/out_xfr16_part{n}.json","w"),ensure_ascii=False)
