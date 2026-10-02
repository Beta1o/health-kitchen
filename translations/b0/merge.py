import json
out=[]
for i in range(1,5):
    out+=json.load(open(f'/mnt/c/WSL/davita/translations/out_b0_part{i}.json'))
jobs=json.load(open('/mnt/c/WSL/davita/translations/jobs_b0.json'))
assert [o['id'] for o in out]==[j['id'] for j in jobs]
json.dump(out,open('/mnt/c/WSL/davita/translations/out_b0.json','w'),ensure_ascii=False,indent=1)
print(len(out))
