import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_xur9.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for i,j in enumerate(d[a:b],a):
    print(f"## {i} {j['id']}\nT: {j['title']}\nD: {j['description']}\nP: {j['portions']} | S: {j['serving_size']}")
    for k in ('ingredients','steps','hints'):
        for n,(g,t) in enumerate(j[k]): print(f"{k[0].upper()}{n}{'['+g+']' if g else ''}: {t}")
    if j['food_choices']: print("F:",' || '.join(j['food_choices']))
