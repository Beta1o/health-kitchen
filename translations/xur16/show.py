import json,sys
d=json.load(open('jobs_xur16.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for i,r in enumerate(d[a:b],a):
    print(f"#{i} {r['id']} T:{r['title']} | D:{r['description']} | P:{r['portions']} | S:{r['serving_size']}")
    for k in('ingredients','steps','hints'):
        print(k[0].upper(),len(r[k] or []))
        for j,(g,t) in enumerate(r[k] or []): print(f" {j}. {t}")
