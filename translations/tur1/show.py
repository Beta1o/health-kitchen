import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_tur1.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for i,r in enumerate(d[a:b],a):
    r={k:v for k,v in r.items() if k not in('source_lang','translate_to')}
    print(i,json.dumps(r,ensure_ascii=False))
