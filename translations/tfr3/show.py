import json,sys
d=json.load(open('/mnt/c/WSL/davita/translations/jobs_tfr3.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for i,j in enumerate(d[a:b],a):
    print(f"#{i} id={j['id']}")
    for k in ("title","description","portions","serving_size","ingredients","steps","hints","food_choices"):
        print(k,json.dumps(j[k],ensure_ascii=False))
