import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_xfr24.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for i in range(a,b):
    j=d[i]
    print(i,'|',j['title'],'|',j['description'],'|',j['portions'],'|',j['serving_size'])
    print(' I:',json.dumps([t for l,t in j['ingredients']],ensure_ascii=False))
    print(' S:',json.dumps([t for l,t in j['steps']],ensure_ascii=False))
