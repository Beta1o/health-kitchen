import json
out=[]
for i in range(1,11):
    out+=json.load(open(f'out_ur2_part{i}.json'))
json.dump(out,open('out_ur2.json','w'),ensure_ascii=False,indent=1)
