import json,sys
# usage: build.py N start  -> reads xhi9/pN.py (list R), writes out_xhi9_partN.json
n,start=int(sys.argv[1]),int(sys.argv[2])
ns={};exec(open(f'xhi9/p{n}.py',encoding='utf-8').read(),ns)
R=ns['R'];jobs=json.load(open('jobs_xhi9.json'))
out=[]
for k,r in enumerate(R):
    j=jobs[start+k]
    t,d,p,s,ing,st,h,f=r
    assert len(ing)==len(j['ingredients']),(start+k,'ing')
    assert len(st)==len(j['steps']),(start+k,'steps')
    assert len(h)==len(j['hints']),(start+k,'hints')
    assert len(f)==len(j['food_choices']),(start+k,'fc')
    out.append({"id":j['id'],"translations":{"hi":{"title":t,"description":d,"portions":p,"serving_size":s,
      "ingredients":[[None,x] for x in ing],"steps":[[None,x] for x in st],"hints":[[None,x] for x in h],"food_choices":f}}})
json.dump(out,open(f'out_xhi9_part{n}.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(out),'recipes, next start',start+len(out))
