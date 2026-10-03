import json,sys,importlib
n=sys.argv[1]
start=int(sys.argv[2])
mod=importlib.import_module('p'+n)
jobs=json.load(open('../jobs_xhi24.json'))
out=[]
for k,(t,d,p,s,I,S,H) in enumerate(mod.R):
    j=jobs[start+k]
    assert len(I)==len(j['ingredients']),(start+k,'ing',len(I),len(j['ingredients']))
    assert len(S)==len(j['steps']),(start+k,'steps')
    assert len(H)==len(j['hints']),(start+k,'hints')
    z=lambda L,src:[[g,x] for (g,_),x in zip(src,L)]
    out.append({"id":j['id'],"translations":{"hi":{"title":t,"description":d if j['description'] is not None else None,"portions":p if j['portions'] is not None else None,"serving_size":s if j['serving_size'] is not None else None,"ingredients":z(I,j['ingredients']),"steps":z(S,j['steps']),"hints":z(H,j['hints']),"food_choices":[]}}})
assert start+len(mod.R)<=len(jobs)
json.dump(out,open(f'../out_xhi24_part{n}.json','w'),ensure_ascii=False,indent=1)
print(n,len(out))
