import json,sys
sys.path.insert(0,'/mnt/c/WSL/davita/translations/xhi4')
jobs={j['id']:j for j in json.load(open('/mnt/c/WSL/davita/translations/jobs_xhi4.json'))}
def pairs(L): return [x if isinstance(x,list) else [None,x] for x in (L or [])]
def build(recs,out):
    res=[]
    for r in recs:
        i,t,d,p,s,I,S,H,F=r
        res.append({"id":i,"translations":{"hi":{"title":t,"description":d,"portions":p,"serving_size":s,"ingredients":pairs(I),"steps":pairs(S),"hints":pairs(H),"food_choices":F}}})
    json.dump(res,open(out,'w'),ensure_ascii=False)
