import json,sys,importlib
sys.path.insert(0,'.')
n=sys.argv[1]
m=importlib.import_module('p'+n)
jobs={j['id']:j for j in json.load(open('../jobs_xur1.json'))}
out=[]
for (i,t,d,p,s,ing,st,h,fc) in m.R:
    j=jobs[i]
    out.append({"id":i,"translations":{"ur":{"title":t,"description":d,"portions":p,"serving_size":s,
      "ingredients":[[None,x] for x in ing],"steps":[[None,x] for x in st],"hints":[[None,x] for x in h],"food_choices":fc}}})
json.dump(out,open(f'../out_xur1_part{n}.json','w'),ensure_ascii=False,indent=1)
print(len(out))
