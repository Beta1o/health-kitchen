import json,sys
sys.path.insert(0,'/mnt/c/WSL/davita/translations/xfr12')
from lab import LAB
J={j['id']:j for j in json.load(open('/mnt/c/WSL/davita/translations/jobs_xfr12.json'))}
def build(recs,name):
    out=[]
    for (i,t,d,p,s,ing,st,hi,fc) in recs:
        j=J[i]
        def pr(k,L):
            assert len(L)==len(j[k]),(i,k,len(L),len(j[k]))
            return [[LAB[g] if g else None,x] for (g,_),x in zip(j[k],L)]
        assert len(fc)==len(j['food_choices']),i
        assert (d is None)==(j['description'] is None) and (p is None)==(j['portions'] is None) and (s is None)==(j['serving_size'] is None),i
        out.append({"id":i,"translations":{"fr":{"title":t,"description":d,"portions":p,"serving_size":s,
          "ingredients":pr('ingredients',ing),"steps":pr('steps',st),"hints":pr('hints',hi),"food_choices":fc}}})
    json.dump(out,open(f"/mnt/c/WSL/davita/translations/{name}","w"),ensure_ascii=False,indent=1)
