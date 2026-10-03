import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_xfr22.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for i,x in enumerate(d[a:b],a):
    x=dict(x)
    for k in('source_lang','translate_to'):x.pop(k)
    print(i,json.dumps(x,ensure_ascii=False))
