import json
base='/mnt/c/WSL/davita/translations/'
out=[]
for i in range(1,5):
    out+=json.load(open(f'{base}out_a0_part{i}.json',encoding='utf-8'))
jobs=json.load(open(base+'jobs_a0.json',encoding='utf-8'))
assert [o['id'] for o in out]==[j['id'] for j in jobs]
json.dump(out,open(base+'out_a0.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(out))
