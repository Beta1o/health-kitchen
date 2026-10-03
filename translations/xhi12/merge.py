import json
base='/mnt/c/WSL/davita/translations/'
out=[]
for n in range(1,12):
    out+=json.load(open(base+f'out_xhi12_part{n}.json'))
json.dump(out,open(base+'out_xhi12.json','w'),ensure_ascii=False,indent=1)
