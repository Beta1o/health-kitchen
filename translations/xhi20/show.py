import json,sys
d=json.load(open('jobs_xhi20.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for i in range(a,b):
    x=dict(d[i]);x.pop('source_lang');x.pop('translate_to');x.pop('id')
    x={k:v for k,v in x.items() if v not in ([],None,"")}
    # compact: drop null groups
    for k in('ingredients','steps','hints'):
        if k in x: x[k]=[p[1] if p[0] is None else p for p in x[k]]
    print(i,json.dumps(x,ensure_ascii=False))
