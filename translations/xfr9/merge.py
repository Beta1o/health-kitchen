import json
o=[]
for i in range(1,7): o+=json.load(open(f'/mnt/c/WSL/davita/translations/out_xfr9_part{i}.json'))
json.dump(o,open('/mnt/c/WSL/davita/translations/out_xfr9.json','w'),ensure_ascii=False,indent=1)
print(len(o))
