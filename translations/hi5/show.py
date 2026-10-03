import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_hi5.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for i,j in enumerate(d[a:b],a):
    print(f"#{i} {j['id']}|T:{j['title']}|D:{j['description']}|P:{j['portions']}|S:{j['serving_size']}")
    for k in('ingredients','steps','hints'):
        print(' ',k[0].upper(),[ (g and '['+g+']') or '' for g,_ in j[k] if g][:1] or '', '')
        for n,(g,t) in enumerate(j[k]): print(f"   {n}{'['+g+']' if g else ''} {t}")
