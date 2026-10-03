import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_xhi19.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for i,x in enumerate(d[a:b],a):
    x=dict(x);[x.pop(k) for k in('source_lang','translate_to')]
    print(i,json.dumps(x,ensure_ascii=False))
