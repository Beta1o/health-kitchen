# usage: build.py N start end  ; reads hi7/pN.py defining R list of tuples
import json,sys,importlib.util
n,a,b=map(int,sys.argv[1:4])
j=json.load(open('/mnt/c/WSL/davita/translations/jobs_hi7.json'))[a:b]
spec=importlib.util.spec_from_file_location('p',f'/mnt/c/WSL/davita/translations/hi7/p{n}.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
assert len(m.R)==len(j),(len(m.R),len(j))
def pairs(src,tr):
    assert len(src)==len(tr or []),(len(src),len(tr))
    return [[ (x[0] if isinstance(x,tuple) else None), (x[1] if isinstance(x,tuple) else x)] for x in tr]
out=[]
for r,t in zip(j,m.R):
    assert t[0]==r['id'],(t[0],r['id'])
    _,ti,de,po,se,ing,st,hi,fc=t
    assert len(fc)==len(r['food_choices'])
    out.append({"id":r['id'],"translations":{"hi":{"title":ti,"description":de,"portions":po,"serving_size":se,"ingredients":pairs(r['ingredients'],ing),"steps":pairs(r['steps'],st),"hints":pairs(r['hints'],hi),"food_choices":fc}}})
json.dump(out,open(f'/mnt/c/WSL/davita/translations/out_hi7_part{n}.json','w'),ensure_ascii=False)
print('ok',len(out))
