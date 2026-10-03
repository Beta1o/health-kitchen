import json,sys
d=json.load(open('jobs_yfr1.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for i in range(a,b):
    r=d[i]; r.pop('source_lang');r.pop('translate_to')
    print(i,json.dumps(r,ensure_ascii=False))
