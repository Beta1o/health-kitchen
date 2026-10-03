import json,sys
d=json.load(open('jobs_xhi18.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for j in d[a:b]:
    print("=== ",j['id'])
    print("T",j['title']);print("D",j['description']);print("P",j['portions']);print("S",j['serving_size'])
    for k,p in (("I","ingredients"),("ST","steps"),("H","hints"),("F","food_choices")):
        for x in j[p]:
            if k=="F": print(k,x)
            else: print(k,("[%s] "%x[0] if x[0] else "")+x[1])
