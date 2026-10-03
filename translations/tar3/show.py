import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_tar3.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for x in d[a:b]:
    print('###',x['id'],'|',x['title'],'|',x['description'],'|',x['portions'],'|',x['serving_size'],'| FC',x['food_choices'])
    for k in('ingredients','steps','hints'):
        print(k)
        for i,(l,t) in enumerate(x[k]): print(' ',i,l if l else '',':',t)
