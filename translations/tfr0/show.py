import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_tfr0.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for i,j in enumerate(d[a:b],a):
    print(i,j['id'],'|',j['title'],'|',j['description'],'|',j['portions'],'|',j['serving_size'])
    for k in('ingredients','steps','hints'):
        print(' ',k,json.dumps(j[k],ensure_ascii=False))
    print('  fc',json.dumps(j['food_choices'],ensure_ascii=False))
