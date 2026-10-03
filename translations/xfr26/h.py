import json,sys
J=json.load(open('/mnt/c/WSL/davita/translations/jobs_xfr26.json'))
def save(part,start,items):
    out=[]
    for i,t in enumerate(items):
        j=J[start+i]
        ti,de,po,se,ing,st=t
        assert len(ing)==len(j['ingredients']),(start+i,'ing',len(ing),len(j['ingredients']))
        assert len(st)==len(j['steps']),(start+i,'steps',len(st),len(j['steps']))
        assert (de is None)==(j['description'] is None),(start+i,'desc')
        out.append({"id":j['id'],"translations":{"fr":{"title":ti,"description":de,"portions":po,"serving_size":se,
          "ingredients":[[None,x] for x in ing],"steps":[[None,x] for x in st],"hints":[],"food_choices":[]}}})
    assert len(out)==len(items)
    json.dump(out,open(f'/mnt/c/WSL/davita/translations/out_xfr26_part{part}.json','w'),ensure_ascii=False,indent=1)
    print('saved',part,len(out))
