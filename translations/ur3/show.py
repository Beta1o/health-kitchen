import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_ur3.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for i in range(a,b):
    j=d[i]
    print(f"## {i} id={j['id']}")
    print("T:",j['title']);print("D:",j['description']);print("P:",j['portions'],"|S:",j['serving_size'])
    for k in('ingredients','steps','hints'):
        for n,(g,t) in enumerate(j[k] or []):
            print(f"{k[0]}{n}:", (f"[{g}] " if g else "")+t)
    print("F:",j['food_choices'])
