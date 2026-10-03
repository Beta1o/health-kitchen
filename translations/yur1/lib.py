import json,sys
JOBS={j['id']:j for j in json.load(open('/mnt/c/WSL/davita/translations/jobs_yur1.json'))}
LAB={"Fruit/veg portions":"پھل/سبزیوں کی مقدار"}
def build(name, recs):
    out=[]
    for r in recs:
        id_,t,d,p,s,ing,st,h,fc=r
        j=JOBS[id_]
        def mk(k,tx):
            src=j[k]
            assert len(src)==len(tx),(id_,k,len(src),len(tx))
            return [[ (LAB.get(a[0],a[0]) if a[0] else None) if not isinstance(b,tuple) else b[0], (b[1] if isinstance(b,tuple) else b)] for a,b in zip(src,tx)]
        assert len(j['food_choices'])==len(fc),(id_,'fc')
        out.append({"id":id_,"translations":{"ur":{"title":t,"description":d,"portions":p,"serving_size":s,"ingredients":mk('ingredients',ing),"steps":mk('steps',st),"hints":mk('hints',h),"food_choices":fc}}})
    json.dump(out,open(f'/mnt/c/WSL/davita/translations/out_yur1_{name}.json','w'),ensure_ascii=False,indent=1)
    print(name,len(out))
