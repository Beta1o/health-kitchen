import json
out=[]
for i in range(1,11):
    out+=json.load(open(f'/mnt/c/WSL/davita/translations/out_xur7_part{i}.json',encoding='utf-8'))
jobs=json.load(open('/mnt/c/WSL/davita/translations/jobs_xur7.json',encoding='utf-8'))
print(len(out),len(jobs))
for k,(o,j) in enumerate(zip(out,jobs)):
    if o['id']!=j['id']: print('ID MISMATCH',k)
json.dump(out,open('/mnt/c/WSL/davita/translations/out_xur7.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
