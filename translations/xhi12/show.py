import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_xhi12.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for i,r in enumerate(d[a:b],a):
    print(f"## {i} {r['id']} T:{r['title']} | D:{r['description']} | P:{r['portions']} | S:{r['serving_size']}")
    for k in('ingredients','steps','hints'):
        for g,t in r[k]: print(f" {k[0]}[{g}] {t}")
    print(" FC:",r['food_choices'])
