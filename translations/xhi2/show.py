import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_xhi2.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for x in d[a:b]:
    print('##',x['id'],'|',x['title'],'|',x['description'],'|',x['portions'],'|',x['serving_size'])
    for k in('ingredients','steps','hints','food_choices'):
        v=x[k]
        print(k[0].upper(),'::',' ;; '.join(p if isinstance(p,str) else p[1] for p in v))
