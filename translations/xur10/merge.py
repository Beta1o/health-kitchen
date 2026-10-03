import json,os
D='/mnt/c/WSL/davita/translations/'
out=[]
for i in range(1,8):
    out+=json.load(open(f'{D}out_xur10_part{i}.json'))
json.dump(out,open(D+'out_xur10.json','w'),ensure_ascii=False,indent=1)
print(len(out))
for i in range(1,8): os.remove(f'{D}out_xur10_part{i}.json')
