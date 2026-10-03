import json
out=[]
for i in range(1,10):
    out+=json.load(open(f'/mnt/c/WSL/davita/translations/out_ur3_part{i}.json',encoding='utf-8'))
json.dump(out,open('/mnt/c/WSL/davita/translations/out_ur3.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(out))
