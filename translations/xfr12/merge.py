import json
o=[]
for i in range(1,12): o+=json.load(open(f'/mnt/c/WSL/davita/translations/out_xfr12_part{i}.json'))
json.dump(o,open('/mnt/c/WSL/davita/translations/out_xfr12.json','w'),ensure_ascii=False,indent=1)
print(len(o))
