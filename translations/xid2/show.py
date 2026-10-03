import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_xid2.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for x in d[a:b]:
    x.pop('source_lang');x.pop('translate_to')
    print(json.dumps(x,ensure_ascii=False))
