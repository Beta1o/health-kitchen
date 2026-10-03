import json,sys
d=json.load(open('jobs_ur5.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for i in range(a,min(b,len(d))):
    x=d[i]; x.pop('source_lang');x.pop('translate_to')
    print(i,json.dumps(x,ensure_ascii=False))
