import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_sur0.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for i,j in enumerate(d[a:b],a):
    print('##',i,j['id'],'|',j['title'],'|',j['portions'],'|',j['serving_size'])
    print('D:',j['description'])
    print('I:',' || '.join(t for g,t in j['ingredients']))
    print('S:',' || '.join(t for g,t in j['steps']))
    print('H:',' || '.join(t for g,t in j['hints']))
