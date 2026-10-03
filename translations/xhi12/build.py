import json,sys,importlib.util
n,a,b=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
base='/mnt/c/WSL/davita/translations/'
jobs=json.load(open(base+'jobs_xhi12.json'))[a:b]
sp=importlib.util.spec_from_file_location('p',base+f'xhi12/p{n}.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
R,GL=m.R,m.GL
assert len(R)==len(jobs),(len(R),len(jobs))
out=[]
for j,r in zip(jobs,R):
    def pairs(k,tr):
        assert len(tr)==len(j[k]),(j['id'],k,len(tr),len(j[k]))
        return [[None if g is None else GL[g],t] for (g,_),t in zip(j[k],tr)]
    assert len(r['f'])==len(j['food_choices']),(j['id'],'fc')
    out.append({'id':j['id'],'translations':{'hi':{'title':r['t'],'description':r.get('d') if j['description'] is not None else None,
     'portions':r['p'] if j['portions'] is not None else None,'serving_size':r['s'] if j['serving_size'] is not None else None,
     'ingredients':pairs('ingredients',r['i']),'steps':pairs('steps',r['st']),'hints':pairs('hints',r['h']),'food_choices':r['f']}}})
json.dump(out,open(base+f'out_xhi12_part{n}.json','w'),ensure_ascii=False,indent=1)
print('ok',len(out))
