import json,os
d='/mnt/c/WSL/davita/translations/'
out=[]
for n in range(1,8):
    p=f'{d}out_xhi19_part{n}.json'
    out+=json.load(open(p))
json.dump(out,open(d+'out_xhi19.json','w'),ensure_ascii=False,indent=1)
print(len(out))
for n in range(1,8): os.remove(f'{d}out_xhi19_part{n}.json')
