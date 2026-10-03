import json
B='/mnt/c/WSL/davita/translations/'
def P(n,recs,size=15):
    jobs=json.load(open(B+'jobs_xhi1.json'))
    s=(n-1)*size; exp=jobs[s:s+size]
    assert len(recs)==len(exp),(len(recs),len(exp))
    out=[]
    for j,r in zip(exp,recs):
        assert r[0]==j['id'],(r[0],j['id'])
        _,title,desc,por,serv,ing,st,hi,fc=r
        def pairs(key,items):
            o=j[key]; assert len(o)==len(items),(j['id'],key,len(o),len(items))
            return [[oo[0],t] for oo,t in zip(o,items)]
        assert len(j['food_choices'])==len(fc),(j['id'],'fc')
        out.append({"id":j['id'],"translations":{"hi":{"title":title,"description":desc,"portions":por,"serving_size":serv,"ingredients":pairs('ingredients',ing),"steps":pairs('steps',st),"hints":pairs('hints',hi),"food_choices":fc}}})
    json.dump(out,open(B+f'out_xhi1_part{n}.json','w'),ensure_ascii=False,indent=0)
    print('ok',n,len(out))
