import json,sys
d=json.load(open('jobs_xhi25.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for i in range(a,min(b,len(d))):
    r=d[i]
    print(f"#{i} {r['id']}")
    for k in ['title','description','portions','serving_size']:
        print(k,'|',r[k])
    for k in ['ingredients','steps','hints']:
        print(k,'|',json.dumps(r[k],ensure_ascii=False))
    print('fc |',json.dumps(r['food_choices'],ensure_ascii=False))
