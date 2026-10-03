import json,sys
j=json.load(open('jobs_xhi9.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for i,r in enumerate(j[a:b],a):
    print(i,r['id'],'|',r['title'],'|',r['description'],'|',r['portions'],'|',r['serving_size'])
    for k in('ingredients','steps','hints'):
        print(k[0].upper(),json.dumps(r[k],ensure_ascii=False))
    print('F',json.dumps(r['food_choices'],ensure_ascii=False));print()
