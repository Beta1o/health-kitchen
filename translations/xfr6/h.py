import json,sys
def build(recs,name):
    out=[]
    for (i,t,d,p,s,ing,st,hi,fc) in recs:
        out.append({"id":i,"translations":{"fr":{"title":t,"description":d,"portions":p,"serving_size":s,
          "ingredients":[[None,x] for x in ing],"steps":[[None,x] for x in st],"hints":[[None,x] for x in hi],"food_choices":fc}}})
    json.dump(out,open(f"/mnt/c/WSL/davita/translations/{name}","w"),ensure_ascii=False,indent=1)
