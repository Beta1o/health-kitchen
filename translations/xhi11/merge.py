import json,glob,re
base='/mnt/c/WSL/davita/translations/'
files=sorted(glob.glob(base+'out_xhi11_part*.json'),key=lambda f:int(re.search(r'part(\d+)',f).group(1)))
out=[]
for f in files: out+=json.load(open(f,encoding='utf-8'))
json.dump(out,open(base+'out_xhi11.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(out),len(files))
