import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_sfr1.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for x in d[a:b]:
    print('##',x['id'],x['title']);print('D:',x['description']);print('P:',x['portions'],'| S:',x['serving_size'])
    for k in('ingredients','steps','hints'):
        print(k[0].upper()+':',json.dumps(x[k],ensure_ascii=False))
