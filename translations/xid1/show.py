import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_xid1.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for r in d[a:b]:
    print("##",r['id'],"|",r['title'],"|",r['description'])
    print("S:",r['serving_size'],"| P:",r['portions'])
    for k in('ingredients','steps','hints'):
        print(k[0].upper()+":", " || ".join((p[0]+"> " if p[0] else "")+p[1] for p in r[k]))
