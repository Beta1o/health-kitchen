import json,sys
def dump(items,part):
    out=[]
    for id_,t,d,p,s,ing,st in items:
        out.append({"id":id_,"translations":{"fr":{"title":t,"description":d,"portions":p,"serving_size":s,
          "ingredients":[[None,x] for x in ing],"steps":[[None,x] for x in st],"hints":[],"food_choices":[]}}})
    json.dump(out,open(f"../out_xfr27_part{part}.json","w"),ensure_ascii=False,indent=1)
