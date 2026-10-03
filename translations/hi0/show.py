import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_hi0.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
def pr(k,v):
    print(f"{k}: {v if v is not None else '~NULL~'}")
for j in d[a:b]:
    print(f"#{j['id']}")
    pr('T',j['title']);pr('D',j['description']);pr('P',j['portions']);pr('S',j['serving_size'])
    for k,c in (('ingredients','I'),('steps','R'),('hints','H')):
        for g,t in j[k]:
            print(f"{c}{'['+g+']' if g else ''}: {t}")
    for f in j['food_choices']: print(f"F: {f}")
