import json,sys
GL={'Optional Toppings':'वैकल्पिक टॉपिंग्स'}
def P(n,recs):
    jobs=json.load(open('/mnt/c/WSL/davita/translations/jobs_xhi7.json'))
    s=(n-1)*15; exp=jobs[s:s+15]
    assert len(recs)==len(exp),(len(recs),len(exp))
    out=[]
    for j,r in zip(exp,recs):
        assert r[0]==j['id'],(r[0],j['id'])
        def pairs(key,items):
            o=j[key]; assert len(o)==len(items),(j['id'],key,len(o),len(items))
            return [[GL.get(oo[0],oo[0]),t] for oo,t in zip(o,items)]
        _,title,desc,por,serv,ing,st,hi,fc=r
        assert len(j['food_choices'])==len(fc),(j['id'],'fc')
        out.append({"id":j['id'],"translations":{"hi":{"title":title,"description":desc,"portions":por,"serving_size":serv,"ingredients":pairs('ingredients',ing),"steps":pairs('steps',st),"hints":pairs('hints',hi),"food_choices":fc}}})
    json.dump(out,open(f'/mnt/c/WSL/davita/translations/out_xhi7_part{n}.json','w'),ensure_ascii=False,indent=0)
    print('ok',n,len(out))
