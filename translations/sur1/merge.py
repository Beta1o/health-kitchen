import json,glob
D='/mnt/c/WSL/davita/translations/'
allr=[]
for n in [1,2,3,4,5,6,7,8,9,10]:
    allr+=json.load(open(f'{D}out_sur1_part{n}.json',encoding='utf-8'))
# p1 holds recipes 0-11; reorder per jobs
jobs=json.load(open(D+'jobs_sur1.json'))
by={r['id']:r for r in allr}
print(len(allr),len(by),len(jobs))
out=[by[j['id']] for j in jobs]
json.dump(out,open(D+'out_sur1.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
