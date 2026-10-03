import json,glob
jobs=json.load(open('/mnt/c/WSL/davita/translations/jobs_tid0.json'))
by={}
for i in range(1,9):
    for o in json.load(open(f'/mnt/c/WSL/davita/translations/tid0/part{i}.json')): by[o['id']]=o
out=[by[j['id']] for j in jobs]
json.dump(out,open('/mnt/c/WSL/davita/translations/out_tid0.json','w'),ensure_ascii=False,indent=1)
print(len(out),len(by))
