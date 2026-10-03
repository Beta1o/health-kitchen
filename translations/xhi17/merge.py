import json
out=[]
for i in range(1,8): out+=json.load(open(f'/mnt/c/WSL/davita/translations/out_xhi17_part{i}.json'))
json.dump(out,open('/mnt/c/WSL/davita/translations/out_xhi17.json','w'),ensure_ascii=False,indent=1)
print(len(out))
