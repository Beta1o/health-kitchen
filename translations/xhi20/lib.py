import json,os
J=json.load(open('/mnt/c/WSL/davita/translations/jobs_xhi20.json'))
def conv(l):
    return [[None,x] if isinstance(x,str) else list(x) for x in (l or [])]
def build(part,start,recs):
    out=[]
    for k,r in enumerate(recs):
        t,de,po,sv,ing,st,hi,fc=(list(r)+[None]*8)[:8]
        j=J[start+k]
        out.append({"id":j["id"],"translations":{"hi":{"title":t,"description":de,"portions":po,"serving_size":sv,
          "ingredients":conv(ing),"steps":conv(st),"hints":conv(hi),"food_choices":list(fc or [])}}})
    json.dump(out,open(f'/mnt/c/WSL/davita/translations/out_xhi20_part{part}.json','w'),ensure_ascii=False,indent=1)
