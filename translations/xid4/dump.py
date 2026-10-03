import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_xid4.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for r in d[a:b]:
    print('#',r['id'])
    for k,p in (('title','T'),('description','D'),('portions','P'),('serving_size','S')):
        print(p+':',r[k])
    for k,p in (('ingredients','I'),('steps','M'),('hints','H')):
        for g,t in r[k] or []:
            print(p+':',(g+'||' if g else '')+t)
    print('F:',' ;; '.join(r['food_choices'] or []))
