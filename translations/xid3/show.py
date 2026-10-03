import json,sys
n=int(sys.argv[1]);d=json.load(open('/mnt/c/WSL/davita/translations/jobs_xid3.json'))
for j in d[(n-1)*15:n*15]:
    print(j['id'],'|',j['title'],'|',j['description'],'|',j['portions'],'|',j['serving_size'])
    for k in('ingredients','steps','hints'):
        print(' ',k[:2].upper(),json.dumps([t for g,t in (j[k] or [])],ensure_ascii=False))
