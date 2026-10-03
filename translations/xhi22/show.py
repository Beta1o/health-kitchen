import json,sys
d=json.load(open('jobs_xhi22.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for x in d[a:b]:
    x=dict(x);x.pop('source_lang');x.pop('translate_to')
    print(json.dumps(x,ensure_ascii=False))
