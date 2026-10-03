import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_tes1.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for r in d[a:b]:
    x=dict(r);x.pop('source_lang');x.pop('translate_to')
    print(json.dumps(x,ensure_ascii=False))
