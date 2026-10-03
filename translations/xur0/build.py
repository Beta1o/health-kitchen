import json,sys
J={j['id']:j for j in json.load(open('/mnt/c/WSL/davita/translations/jobs_xur0.json'))}
def build(R,part):
    out=[]
    for r in R:
        i,t,d,p,s,ing,st,h,fc=r
        j=J[i]
        def pr(k,L):
            assert len(L)==len(j[k]),(i,k,len(L),len(j[k]))
            return [[a[0],x] for a,x in zip(j[k],L)]
        out.append({"id":i,"translations":{"ur":{"title":t,"description":d,"portions":p,"serving_size":s,
          "ingredients":pr('ingredients',ing),"steps":pr('steps',st),"hints":pr('hints',h),"food_choices":fc}}})
        assert len(fc)==len(j['food_choices']),(i,'fc')
    json.dump(out,open(f'/mnt/c/WSL/davita/translations/out_xur0_part{part}.json','w'),ensure_ascii=False,indent=1)
    print(part,len(out))
