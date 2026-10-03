import json,sys
J=json.load(open('/mnt/c/WSL/davita/translations/jobs_xhi17.json'))
def build(start,recs,out):
    res=[]
    for k,(t,d,p,s,ing,st) in enumerate(recs):
        j=J[start+k]
        assert len(ing)==len(j['ingredients']),(start+k,'ing',len(ing),len(j['ingredients']))
        assert len(st)==len(j['steps']),(start+k,'steps',len(st),len(j['steps']))
        res.append({"id":j['id'],"translations":{"hi":{"title":t,"description":d,"portions":p,"serving_size":s,
          "ingredients":[[None,x] for x in ing],"steps":[[None,x] for x in st],"hints":[],"food_choices":[]}}})
    json.dump(res,open(out,'w'),ensure_ascii=False,indent=1)
