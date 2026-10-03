import json
o=[]
for i in range(1,8): o+=json.load(open(f'/mnt/c/WSL/davita/translations/out_xhi23_part{i}.json'))
json.dump(o,open('/mnt/c/WSL/davita/translations/out_xhi23.json','w'),ensure_ascii=False,indent=0)
print(len(o))
