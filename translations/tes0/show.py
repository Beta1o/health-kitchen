import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_tes0.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
def f(l):
    return [x if x[0] else x[1] for x in l]
for i,r in enumerate(d[a:b],a):
    print(i,r['id'],'|',r['title'],'|',r['description'],'|',r['portions'],'|',r['serving_size'])
    for k in('ingredients','steps','hints'):
        print(' ',k[0].upper(),json.dumps(f(r[k]),ensure_ascii=False))
    print('  FC',json.dumps(r['food_choices'],ensure_ascii=False))
