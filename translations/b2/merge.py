import json, os
D='/mnt/c/WSL/davita/translations/'
out=[]
for i in range(1,5): out+=json.load(open(f'{D}out_b2_part{i}.json',encoding='utf-8'))
jobs=json.load(open(D+'jobs_b2.json',encoding='utf-8'))
assert [o['id'] for o in out]==[j['id'] for j in jobs]
json.dump(out,open(D+'out_b2.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(out))
