import json,sys
j=json.load(open('/mnt/c/WSL/davita/translations/jobs_hi6.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
def f(l):
    return [ (x[1] if x[0] is None else [x[0],x[1]]) for x in (l or [])]
for i,r in enumerate(j[a:b],a):
    print(i,json.dumps([r['id'],r['title'],r['description'],r['portions'],r['serving_size'],f(r['ingredients']),f(r['steps']),f(r['hints']),r['food_choices']],ensure_ascii=False))
