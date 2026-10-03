import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_xhi4.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for j in d[a:b]:
    print('##',j['id'],'|',j['title'],'|',j['description'],'|',j['portions'],'|',j['serving_size'])
    for k in('ingredients','steps','hints'):
        print(k[0].upper(),[ (x[1] if x[0] is None else x) for x in j[k] or []])
    print('F',j['food_choices'])
