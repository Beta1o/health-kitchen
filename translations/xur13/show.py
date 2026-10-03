import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_xur13.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for r in d[a:b]:
    print(r['id'],'|',r['title'],'|',r['description'],'|',r['portions'],'|',r['serving_size'])
    for k in('ingredients','steps','hints'):
        if r[k]: print(k[0].upper(),json.dumps([p[1] for p in r[k]],ensure_ascii=False))
    if r['food_choices']: print('FC',r['food_choices'])
