import json
out=[]
for i in range(1,5): out+=json.load(open(f'/mnt/c/WSL/davita/translations/out_c18_part{i}.json'))
json.dump(out,open('/mnt/c/WSL/davita/translations/out_c18.json','w'),ensure_ascii=False,indent=1)
print(len(out))
