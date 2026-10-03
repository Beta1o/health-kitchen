import json,sys,importlib.util,os
H=os.path.dirname(os.path.abspath(__file__));T=os.path.dirname(H)
jobs=json.load(open(T+'/jobs_xur2.json',encoding='utf-8'))
n=int(sys.argv[1]);a,b=(n-1)*15,min(n*15,len(jobs))
sp=importlib.util.spec_from_file_location('p',f'{H}/p{n}.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
R=m.R;assert len(R)==b-a,(len(R),b-a)
out=[]
for j,r in zip(jobs[a:b],R):
    id_,t,d,p,s,ing,st,h,fc=r
    assert id_==j['id'],(id_,j['id'])
    for L,k in ((ing,'ingredients'),(st,'steps'),(h,'hints'),(fc,'food_choices')):
        assert len(L)==len(j[k] or []),(id_,k,len(L),len(j[k] or []))
    pr=lambda L:[[None,x] for x in L]
    out.append({"id":id_,"translations":{"ur":{"title":t,"description":d,"portions":p,"serving_size":s,"ingredients":pr(ing),"steps":pr(st),"hints":pr(h),"food_choices":fc}}})
json.dump(out,open(f'{T}/out_xur2_part{n}.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('ok',n,len(out))
