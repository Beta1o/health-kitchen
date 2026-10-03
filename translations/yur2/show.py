import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_yur2.json'));a,b=int(sys.argv[1]),int(sys.argv[2])
for i,j in enumerate(d[a:b],a):
    print(i,end=' ')
    for k in ('source_lang','translate_to'):j.pop(k)
    print(json.dumps(j,ensure_ascii=False,separators=(',',':')))
