import json,sys
a,b=int(sys.argv[1]),int(sys.argv[2])
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_xfr12.json'))
for k,j in enumerate(d[a:b],a):
    print(k,j['id'])
    print(json.dumps([j[x] if x not in('ingredients','steps','hints') else [b for a,b in j[x]] for x in ['title','description','portions','serving_size','ingredients','steps','hints','food_choices']],ensure_ascii=False))
