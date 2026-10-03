import json,glob
out=[]
for i in range(1,14):
    out+=json.load(open(f'out_ur6_part{i}.json',encoding='utf-8'))
jobs=json.load(open('jobs_ur6.json',encoding='utf-8'))
print(len(out),len(jobs))
for k,(o,j) in enumerate(zip(out,jobs)):
    if o['id']!=j['id']: print('ID MISMATCH',k,o['id'],j['id'])
json.dump(out,open('out_ur6.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
