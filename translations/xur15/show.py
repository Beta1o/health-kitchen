import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_xur15.json'))
for i in range(int(sys.argv[1]),int(sys.argv[2])):
    r=d[i]
    print(i,'|',r['title'],'|',r['description'],'|',r['portions'],'|',r['serving_size'])
    for a,b in r['ingredients']:print('  I:',b)
    for a,b in r['steps']:print('  S:',b)
