import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_xfr6.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for j in d[a:b]:
    print(j['id'],'|',j['title'],'|',j['description'],'|',j['portions'],'|',j['serving_size'])
    for k in('ingredients','steps','hints'):
        print(' ',k[:3].upper(),[ (g,t) if g else t for g,t in j[k]])
    print('  FC',j['food_choices'])
