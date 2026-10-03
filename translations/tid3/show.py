import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_tid3.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for i in range(a,b):
    x=d[i];print('##',i,x['id'],'|',x['title'],'|',x['description'],'|',x['portions'],'|',x['serving_size'])
    for k in('ingredients','steps','hints'):
        print(k[0].upper(),json.dumps([p if p[0] else p[1] for p in x[k]] if x[k] else x[k],ensure_ascii=False))
    print('F',json.dumps(x['food_choices'],ensure_ascii=False))
