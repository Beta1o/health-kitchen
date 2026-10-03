import json,glob
out=[]
for n in range(1,8):
    out+=json.load(open(f'/mnt/c/WSL/davita/translations/out_yhi3_part{n}.json'))
json.dump(out,open('/mnt/c/WSL/davita/translations/out_yhi3.json','w'),ensure_ascii=False,indent=1)
print(len(out))
