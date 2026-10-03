import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_xur17.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for r in d[a:b]:
    r={k:v for k,v in r.items() if k not in('source_lang','translate_to')}
    print(json.dumps(r,ensure_ascii=False))
