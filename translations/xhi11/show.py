import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_xhi11.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for i in range(a,b):
    r=d[i]
    print('##',i,r['id'],'|',r['title'],'|',r['description'],'|',r['portions'],'|',r['serving_size'])
    for k in('ingredients','steps','hints'):
        print(k[0].upper(),[ (p[1] if p[0] is None else p) for p in r[k]])
    print('FC',r['food_choices'])
