import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent.parent
def build(part, start, recs):
    jobs=json.load(open(H/'jobs_xur11.json'))
    out=[]
    for i,r in enumerate(recs):
        j=jobs[start+i]
        t,d,p,s,ing,st,hi,fc=r
        f=lambda L:[x if isinstance(x,list) else [None,x] for x in L]
        out.append({"id":j["id"],"translations":{"ur":{"title":t,"description":d,"portions":p,"serving_size":s,"ingredients":f(ing),"steps":f(st),"hints":f(hi),"food_choices":list(fc)}}})
    json.dump(out,open(H/f'out_xur11_part{part}.json','w'),ensure_ascii=False,indent=1)
    print(part,len(out))
