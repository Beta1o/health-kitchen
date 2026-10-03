import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_xur0.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for i,j in enumerate(d[a:b],a):
    print('#',i,j['id'],'|',j['title'],'|',j['description'],'|',j['portions'],'|',j['serving_size'])
    for k in('ingredients','steps','hints'):
        for n,(g,t) in enumerate(j[k]): print(' ',k[0]+str(n),(f'[{g}] ' if g else '')+t)
    print('  FC',j['food_choices'])
