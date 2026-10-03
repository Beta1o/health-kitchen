import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_tur2.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for k,j in enumerate(d[a:b],a):
    j.pop('source_lang');j.pop('translate_to')
    print(k,json.dumps(j,ensure_ascii=False))
