import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_shi0.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for i in range(a,b):
    r=d[i];print(i,json.dumps({k:r[k] for k in('id','title','description','portions','serving_size','ingredients','steps','hints','food_choices')},ensure_ascii=False))
