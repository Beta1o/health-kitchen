import json
o=[]
for i in range(1,8): o+=json.load(open(f"/mnt/c/WSL/davita/translations/out_xfr3_part{i}.json"))
json.dump(o,open("/mnt/c/WSL/davita/translations/out_xfr3.json","w"),ensure_ascii=False,indent=1)
print(len(o))
