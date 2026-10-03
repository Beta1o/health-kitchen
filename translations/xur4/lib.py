import json,sys
def R(i,t,d,p,s,I,S,H,F):
    P=lambda L:[[None,x] for x in L]
    return {"id":i,"translations":{"ur":{"title":t,"description":d,"portions":p,"serving_size":s,"ingredients":P(I),"steps":P(S),"hints":P(H),"food_choices":F}}}
def dump(n,recs):
    json.dump(recs,open(f'/mnt/c/WSL/davita/translations/out_xur4_part{n}.json','w',encoding='utf-8'),ensure_ascii=False)
