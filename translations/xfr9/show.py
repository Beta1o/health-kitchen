import json,sys
a,b=int(sys.argv[1]),int(sys.argv[2])
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_xfr9.json'))
for k,j in enumerate(d[a:b],a):
    print(k,j['id'])
    print(json.dumps([j[x] if x not in('ingredients','steps','hints') else [b for a,b in j[x]] for x in ['title','description','portions','serving_size','ingredients','steps','hints','food_choices']],ensure_ascii=False))
    L=[(k2,a) for k2 in('ingredients','steps','hints') for a,b in j[k2] if a]
    if L: print("LABELS",L)
