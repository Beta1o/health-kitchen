import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_xur12.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for i,r in enumerate(d[a:b],a):
    print(i,json.dumps({k:v for k,v in r.items() if k not in('source_lang','translate_to')},ensure_ascii=False))
