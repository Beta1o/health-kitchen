import json,os
b="/mnt/c/WSL/davita/translations/"
out=[]
for i in range(1,5): out+=json.load(open(b+f"out_c13_part{i}.json"))
json.dump(out,open(b+"out_c13.json","w"),ensure_ascii=False,indent=1)
for i in range(1,5): os.remove(b+f"out_c13_part{i}.json")
print(len(out))
