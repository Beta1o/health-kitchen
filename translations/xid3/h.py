import json,re
J='/mnt/c/WSL/davita/translations/'
def fc(s):
    r=s
    for a,b in [('nondairy milk substitute','pengganti susu non-susu'),('milk substitute','pengganti susu'),('high-calorie','kalori tinggi'),('high calorie','kalori tinggi'),('low and medium potassium','kalium rendah dan sedang'),('low potassium','kalium rendah'),('medium potassium','kalium sedang'),('high potassium','kalium tinggi'),('vegetables','sayuran'),('vegetable','sayuran'),('starch','pati'),('fat','lemak'),('meat','daging'),('protein','protein'),('fruit','buah'),('milk','susu')]:
        r=r.replace(a,b)
    return r
def P(n,recs):
    jobs=json.load(open(J+'jobs_xid3.json'))
    exp=jobs[(n-1)*15:n*15]
    assert len(recs)==len(exp),(len(recs),len(exp))
    out=[]
    for j,r in zip(exp,recs):
        assert r[0]==j['id'],(r[0],j['id'])
        def pairs(key,items):
            o=j[key] or []; assert len(o)==len(items),(j['id'],key,len(o),len(items))
            return [[oo[0],t] for oo,t in zip(o,items)]
        _,title,desc,por,serv,ing,st,hi=r
        out.append({"id":j['id'],"translations":{"id":{"title":title,"description":desc,"portions":por,"serving_size":serv,"ingredients":pairs('ingredients',ing),"steps":pairs('steps',st),"hints":pairs('hints',hi),"food_choices":[fc(x) for x in j['food_choices']]}}})
    json.dump(out,open(J+f'out_xid3_part{n}.json','w'),ensure_ascii=False,indent=0)
    print('ok',n,len(out))
