import json,sys
d=json.load(open('jobs_ur2.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for i,j in enumerate(d[a:b],a):
    print(f"## {i} id={j['id']} T={j['title']} | D={j['description']} | P={j['portions']} | S={j['serving_size']}")
    for k in('ingredients','steps','hints'):
        print(k[0].upper(),json.dumps(j[k],ensure_ascii=False))
    print('F',json.dumps(j['food_choices'],ensure_ascii=False))
