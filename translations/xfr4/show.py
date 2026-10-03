import json,sys
a,b=int(sys.argv[1]),int(sys.argv[2])
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_xfr4.json'))
for j in d[a:b]:
    print(j['id'],'|',j['title'],'|',j['description'],'|',j['portions'],'|',j['serving_size'])
    for k in('ingredients','steps','hints'):
        print(k[0].upper(),[t for g,t in j[k] or []])
    print('FC',j['food_choices'])
