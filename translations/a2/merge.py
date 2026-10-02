import json
from pathlib import Path
H=Path(__file__).resolve().parent.parent
out=[]
for i in range(1,5):
    out+=json.load(open(H/f'out_a2_part{i}.json',encoding='utf-8'))
json.dump(out,open(H/'out_a2.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(out))
