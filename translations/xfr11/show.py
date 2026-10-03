import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_xfr11.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for j in d[a:b]:
    print(j['id'],'|',j['title'],'|',j['description'],'|',j['portions'],'|',j['serving_size'])
    for k in('ingredients','steps','hints'):
        print(k[:2].upper(),json.dumps(j[k],ensure_ascii=False))
    print('FC',j['food_choices']);print()
