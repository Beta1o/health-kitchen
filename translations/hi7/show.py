import json,sys
j=json.load(open('/mnt/c/WSL/davita/translations/jobs_hi7.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for i,r in enumerate(j[a:b],a):
    print(f"#{i} {r['id']}")
    print("T:",r['title']);print("D:",r['description']);print("P:",r['portions'],"| S:",r['serving_size'])
    for k in('ingredients','steps','hints'):
        print(k[0].upper()+":")
        for g,t in r[k] or []: print("  ",(f"[{g}] " if g else "")+t)
    print("F:",r['food_choices'])
