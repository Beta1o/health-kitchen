import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_tar2.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for x in d[a:b]:
    print('##',x['id'],'|',x['title'],'|',x['description'],'|',x['portions'],'|',x['serving_size'])
    for k in('ingredients','steps','hints'):
        print(k,'(%d)'%len(x[k]))
        gs=[]
        for l,t in x[k]:
            if l and l not in gs: gs.append(l)
        if gs: print(' G:',gs)
        for i,(l,t) in enumerate(x[k]): print(' ',i,t)
