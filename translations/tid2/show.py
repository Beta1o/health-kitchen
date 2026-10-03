import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_tid2.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for j in d[a:b]:
    print(json.dumps({k:j[k] for k in ['id','title','description','portions','serving_size','ingredients','steps','hints','food_choices']},ensure_ascii=False))
