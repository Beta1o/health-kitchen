import json,glob
d='/mnt/c/WSL/davita/translations/'
out=[]
for i in range(1,13): out+=json.load(open(f'{d}out_xur4_part{i}.json',encoding='utf-8'))
json.dump(out,open(d+'out_xur4.json','w',encoding='utf-8'),ensure_ascii=False)
print(len(out))
