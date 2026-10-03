import json,glob,os
out=[]
fs=sorted(glob.glob('../out_yhi0_part*.json'),key=lambda f:int(f.split('part')[1].split('.')[0]))
for f in fs: out+=json.load(open(f,encoding='utf-8'))
json.dump(out,open('../out_yhi0.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(out))
