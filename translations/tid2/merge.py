import json,glob,os
base='/mnt/c/WSL/davita/translations/'
jobs=json.load(open(base+'jobs_tid2.json'))
by={}
for n in range(1,14):
    for o in json.load(open(f'part{n}.json')): by[o['id']]=o
out=[by[j['id']] for j in jobs]
json.dump(out,open(base+'out_tid2.json','w'),ensure_ascii=False,indent=1)
print(len(out),len(by))
