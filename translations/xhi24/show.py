import json,sys
d=json.load(open('jobs_xhi24.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for i,r in enumerate(d[a:b],a):
    print(f"#{i} id={r['id']}\nT: {r['title']}\nD: {r['description']}\nP: {r['portions']} | S: {r['serving_size']}")
    for k in('ingredients','steps','hints'):
        print(k[0].upper()+':')
        for j,(g,t) in enumerate(r[k]): print(f"  {j}{'['+g+']' if g else ''} {t}")
