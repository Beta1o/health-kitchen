import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_xfr2.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for j in d[a:b]:
    print(j['id'],'|',j['title'],'|',j['description'],'|P:',j['portions'],'|S:',j['serving_size'])
    for k in('ingredients','steps','hints'):
        print(k[:2].upper(),json.dumps(j[k],ensure_ascii=False))
    print('FC',json.dumps(j['food_choices'],ensure_ascii=False));print()
