import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_xid10.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for j in d[a:b]:
    j=dict(j);j.pop('source_lang');j.pop('translate_to')
    print(json.dumps(j,ensure_ascii=False))
