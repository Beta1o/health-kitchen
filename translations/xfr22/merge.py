import json
o=[]
for i in range(1,8): o+=json.load(open(f'/mnt/c/WSL/davita/translations/out_xfr22_part{i}.json'))
json.dump(o,open('/mnt/c/WSL/davita/translations/out_xfr22.json','w'),ensure_ascii=False)
print(len(o))
