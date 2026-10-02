import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_b4.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for r in d[a:b]:
    print('=====',r['id'],'|',r['title'],'| desc:',r['description'],'| portions:',r['portions'],'| ss:',r['serving_size'])
    for k in ('ingredients','steps','hints'):
        print('--',k)
        for g,t in r[k]: print('  [%s] %s'%(g,t))
    print('-- fc',r['food_choices'])
