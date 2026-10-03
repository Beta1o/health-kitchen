import json,sys
def P(n,recs):
    jobs=json.load(open('/mnt/c/WSL/davita/translations/jobs_thi1.json'))
    s=(n-1)*8; exp=jobs[s:s+8]
    assert len(recs)==len(exp),(len(recs),len(exp))
    out=[]
    for j,r in zip(exp,recs):
        assert r[0]==j['id'],(r[0],j['id'])
        def pairs(key,items):
            o=j[key]; assert len(o)==len(items),(j['id'],key,len(o),len(items))
            res=[]
            for oo,t in zip(o,items):
                if oo[0] is not None and '::' in t: g,t=t.split('::',1)
                else: g=oo[0]
                res.append([g,t])
            return res
        _,title,desc,por,serv,ing,st,hi,fc=r
        assert len(j['food_choices'])==len(fc),(j['id'],'fc')
        out.append({"id":j['id'],"translations":{"hi":{"title":title,"description":desc,"portions":por,"serving_size":serv,"ingredients":pairs('ingredients',ing),"steps":pairs('steps',st),"hints":pairs('hints',hi),"food_choices":fc}}})
    json.dump(out,open(f'/mnt/c/WSL/davita/translations/out_thi1_part{n}.json','w'),ensure_ascii=False,indent=0)
    print('ok',n,len(out))
